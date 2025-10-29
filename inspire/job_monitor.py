#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启智(Inspire)分布式训练任务状态监控脚本
Inspire Distributed Training Job Status Monitor

This script provides functionality to:
- Monitor training job status through polling
- Track status changes and timeline
- Export monitoring data
- Send notifications on status changes

Usage:
    python job_monitor.py monitor --job-id <job_id>
    python job_monitor.py monitor --job-id <job_id> --interval 30 --timeout 3600
    python job_monitor.py status --job-id <job_id>
"""

import os
import json
import logging
import requests
import argparse
import time
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """任务状态枚举"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


@dataclass
class StatusSnapshot:
    """状态快照数据类"""
    timestamp: str
    job_id: str
    status: str
    sub_status: int
    sub_msg: str
    running_time_ms: str
    created_at: str
    finished_at: Optional[str] = None
    timeline: Optional[Dict] = None
    node_count: int = 0
    priority: int = 0


@dataclass
class MonitorConfig:
    """监控配置类"""
    base_url: str = "https://qz.sii.edu.cn"
    poll_interval: int = 10  # 轮询间隔(秒)
    timeout: int = 3600  # 监控超时时间(秒)
    max_retries: int = 3
    retry_delay: float = 1.0
    export_file: Optional[str] = None
    enable_notifications: bool = False
    github_config: Optional[Dict[str, str]] = None  # GitHub配置


class JobMonitor:
    """
    启智训练任务监控器
    """
    
    def __init__(self, config: MonitorConfig):
        """
        初始化监控器
        
        Args:
            config: 监控配置
        """
        self.config = config
        self.base_url = config.base_url.rstrip('/')
        self.token = None
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.session = requests.Session()
        self.snapshots: List[StatusSnapshot] = []
        self.running = False
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        logger.info("Received interrupt signal, stopping monitor...")
        self.running = False
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        认证获取token
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            认证是否成功
        """
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/token",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') == 0:
                self.token = result['data']['access_token']
                self.headers['Authorization'] = f"Bearer {self.token}"
                logger.info("Authentication successful")
                return True
            else:
                logger.error(f"Authentication failed: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication request failed: {str(e)}")
            return False
    
    def get_job_status(self, job_id: str) -> Optional[StatusSnapshot]:
        """
        获取任务状态
        
        Args:
            job_id: 任务ID
            
        Returns:
            状态快照，失败时返回None
        """
        if not self.token:
            logger.error("Not authenticated")
            return None
        
        payload = {"job_id": job_id}
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.session.post(
                    f"{self.base_url}/openapi/v1/train_job/detail",
                    json=payload,
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get('code') == 0:
                    job_data = result['data']
                    snapshot = StatusSnapshot(
                        timestamp=datetime.now().isoformat(),
                        job_id=job_id,
                        status=job_data.get('status', 'UNKNOWN'),
                        sub_status=job_data.get('sub_status', 0),
                        sub_msg=job_data.get('sub_msg', ''),
                        running_time_ms=job_data.get('running_time_ms', '0'),
                        created_at=job_data.get('created_at', ''),
                        finished_at=job_data.get('finished_at'),
                        timeline=job_data.get('timeline'),
                        node_count=job_data.get('node_count', 0),
                        priority=job_data.get('priority', 0)
                    )
                    return snapshot
                else:
                    logger.error(f"API error: {result.get('message', 'Unknown error')}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.config.max_retries - 1:
                    logger.warning(f"Request failed (attempt {attempt + 1}), retrying: {str(e)}")
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    logger.error(f"Failed to get job status after {self.config.max_retries} attempts: {str(e)}")
                    return None
        
        return None
    
    def _format_duration(self, ms: str) -> str:
        """
        格式化运行时长
        
        Args:
            ms: 毫秒数字符串
            
        Returns:
            格式化的时长字符串
        """
        try:
            milliseconds = int(ms)
            seconds = milliseconds // 1000
            minutes = seconds // 60
            hours = minutes // 60
            
            if hours > 0:
                return f"{hours}h {minutes % 60}m {seconds % 60}s"
            elif minutes > 0:
                return f"{minutes}m {seconds % 60}s"
            else:
                return f"{seconds}s"
        except (ValueError, TypeError):
            return "Unknown"
    
    def _format_timestamp(self, timestamp_ms: str) -> str:
        """
        格式化时间戳
        
        Args:
            timestamp_ms: 毫秒时间戳字符串
            
        Returns:
            格式化的时间字符串
        """
        try:
            timestamp = int(timestamp_ms) / 1000
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            return "Unknown"
    
    def print_status_summary(self, snapshot: StatusSnapshot) -> None:
        """
        打印状态摘要
        
        Args:
            snapshot: 状态快照
        """
        print(f"\n{'='*60}")
        print(f"Job Status Summary - {snapshot.timestamp[:19]}")
        print(f"{'='*60}")
        print(f"Job ID:        {snapshot.job_id}")
        print(f"Status:        {snapshot.status}")
        print(f"Sub Status:    {snapshot.sub_status}")
        print(f"Sub Message:   {snapshot.sub_msg}")
        print(f"Running Time:  {self._format_duration(snapshot.running_time_ms)}")
        print(f"Created At:    {self._format_timestamp(snapshot.created_at)}")
        
        if snapshot.finished_at:
            print(f"Finished At:   {self._format_timestamp(snapshot.finished_at)}")
        
        print(f"Node Count:    {snapshot.node_count}")
        print(f"Priority:      {snapshot.priority}")
        
        if snapshot.timeline:
            print(f"\nTimeline:")
            timeline = snapshot.timeline
            if timeline.get('created'):
                print(f"  Created:     {self._format_timestamp(timeline['created'])}")
            if timeline.get('resource_prepared'):
                print(f"  Resource:    {self._format_timestamp(timeline['resource_prepared'])}")
            if timeline.get('run'):
                print(f"  Started:     {self._format_timestamp(timeline['run'])}")
            if timeline.get('finished'):
                print(f"  Finished:    {self._format_timestamp(timeline['finished'])}")
    
    def _detect_status_change(self, current: StatusSnapshot, previous: Optional[StatusSnapshot]) -> bool:
        """
        检测状态是否发生变化
        
        Args:
            current: 当前状态
            previous: 上一次状态
            
        Returns:
            是否发生变化
        """
        if previous is None:
            return True
        
        return (current.status != previous.status or 
                current.sub_status != previous.sub_status)
    
    def _is_terminal_status(self, status: str) -> bool:
        """
        判断是否为终端状态
        
        Args:
            status: 状态字符串
            
        Returns:
            是否为终端状态
        """
        terminal_statuses = ['SUCCEEDED', 'FAILED', 'CANCELLED']
        return status in terminal_statuses
    
    def monitor_job(self, job_id: str) -> bool:
        """
        监控任务状态
        
        Args:
            job_id: 任务ID
            
        Returns:
            监控是否成功完成
        """
        logger.info(f"Starting to monitor job: {job_id}")
        logger.info(f"Poll interval: {self.config.poll_interval}s, Timeout: {self.config.timeout}s")
        
        start_time = time.time()
        self.running = True
        previous_snapshot = None
        
        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # 检查超时
            if elapsed_time > self.config.timeout:
                logger.warning(f"Monitoring timeout after {self.config.timeout} seconds")
                break
            
            # 获取当前状态
            snapshot = self.get_job_status(job_id)
            if snapshot is None:
                logger.error("Failed to get job status, continuing...")
                time.sleep(self.config.poll_interval)
                continue
            
            # 保存快照
            self.snapshots.append(snapshot)
            
            # 检测状态变化
            status_changed = self._detect_status_change(snapshot, previous_snapshot)
            
            if status_changed:
                logger.info(f"Status changed: {snapshot.status} (sub_status: {snapshot.sub_status})")
                self.print_status_summary(snapshot)
                
                # 发送通知（如果启用）
                if self.config.enable_notifications:
                    self._send_notification(snapshot, previous_snapshot)
            else:
                # 简化输出
                elapsed_str = str(timedelta(seconds=int(elapsed_time)))
                print(f"\r[{elapsed_str}] Status: {snapshot.status} | "
                      f"Running: {self._format_duration(snapshot.running_time_ms)}", end='')
            
            # 检查是否到达终端状态
            if self._is_terminal_status(snapshot.status):
                logger.info(f"Job reached terminal status: {snapshot.status}")
                self.print_status_summary(snapshot)
                break
            
            previous_snapshot = snapshot
            
            # 等待下次轮询
            time.sleep(self.config.poll_interval)
        
        # 导出数据
        if self.config.export_file:
            self.export_monitoring_data(self.config.export_file)
        
        logger.info("Monitoring completed")
        return True
    
    def _send_notification(self, current: StatusSnapshot, previous: Optional[StatusSnapshot]) -> None:
        """
        发送状态变化通知
        
        Args:
            current: 当前状态
            previous: 上一次状态
        """
        logger.info(f"Notification: Job {current.job_id} status changed to {current.status}")
        
        # 发送GitHub PR通知
        if hasattr(self.config, 'github_config') and self.config.github_config:
            self._send_github_notification(current, previous)
    
    def _send_github_notification(self, current: StatusSnapshot, previous: Optional[StatusSnapshot]) -> None:
        """
        发送GitHub PR通知
        
        Args:
            current: 当前状态
            previous: 上一次状态
        """
        try:
            github_config = self.config.github_config
            
            # 构建状态消息
            status_emoji = self._get_status_emoji(current.status)
            change_type = "Initial Status" if previous is None else "Status Changed"
            
            # 状态变化信息
            status_info = f"{status_emoji} **{change_type}**\n\n"
            status_info += f"- **Job ID:** `{current.job_id}`\n"
            status_info += f"- **Status:** {current.status}\n"
            
            if current.sub_msg:
                status_info += f"- **Message:** {current.sub_msg}\n"
            
            status_info += f"- **Running Time:** {self._format_duration(current.running_time_ms)}\n"
            
            if current.node_count > 0:
                status_info += f"- **Nodes:** {current.node_count}\n"
            
            # 时间线信息
            if current.timeline:
                timeline = current.timeline
                if timeline.get('created'):
                    status_info += f"- **Created:** {self._format_timestamp(timeline['created'])}\n"
                if timeline.get('resource_prepared'):
                    status_info += f"- **Resource Ready:** {self._format_timestamp(timeline['resource_prepared'])}\n"
                if timeline.get('run'):
                    status_info += f"- **Started:** {self._format_timestamp(timeline['run'])}\n"
                if timeline.get('finished'):
                    status_info += f"- **Finished:** {self._format_timestamp(timeline['finished'])}\n"
            
            # 如果是终端状态，添加额外信息
            if self._is_terminal_status(current.status):
                if current.status == 'SUCCEEDED':
                    status_info += f"\n🎉 **Training completed successfully!**"
                elif current.status == 'FAILED':
                    status_info += f"\n💥 **Training failed.** Check the logs for details."
                elif current.status == 'CANCELLED':
                    status_info += f"\n🛑 **Training was cancelled.**"
            
            status_info += f"\n\n*Updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            
            # 发送GitHub API请求
            headers = {
                'Authorization': f'token {github_config["token"]}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'body': status_info
            }
            
            url = f"https://api.github.com/repos/{github_config['repo']}/issues/{github_config['issue_number']}/comments"
            
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            logger.info(f"GitHub notification sent successfully to PR #{github_config['issue_number']}")
            
        except Exception as e:
            logger.error(f"Failed to send GitHub notification: {str(e)}")
    
    def _get_status_emoji(self, status: str) -> str:
        """
        获取状态对应的emoji
        
        Args:
            status: 任务状态
            
        Returns:
            对应的emoji
        """
        status_emojis = {
            'PENDING': '⏳',
            'RUNNING': '🏃',
            'SUCCEEDED': '✅',
            'FAILED': '❌',
            'CANCELLED': '🛑',
            'UNKNOWN': '❓'
        }
        return status_emojis.get(status, '📊')
    
    def export_monitoring_data(self, filename: str) -> None:
        """
        导出监控数据
        
        Args:
            filename: 导出文件名
        """
        try:
            data = {
                'monitoring_config': asdict(self.config),
                'snapshots': [asdict(snapshot) for snapshot in self.snapshots],
                'summary': {
                    'total_snapshots': len(self.snapshots),
                    'monitoring_duration': self.snapshots[-1].timestamp if self.snapshots else None,
                    'final_status': self.snapshots[-1].status if self.snapshots else None
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Monitoring data exported to: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to export monitoring data: {str(e)}")


def get_credentials() -> tuple[str, str]:
    """
    从环境变量获取凭证
    
    Returns:
        (username, password) 元组
        
    Raises:
        ValueError: 凭证不可用时
    """
    username = os.getenv('INSPIRE_USERNAME')
    password = os.getenv('INSPIRE_PASSWORD')
    
    if not username:
        raise ValueError(
            "Username not found. Please set INSPIRE_USERNAME environment variable.\n"
            "Example: export INSPIRE_USERNAME='your_username'"
        )
    
    if not password:
        raise ValueError(
            "Password not found. Please set INSPIRE_PASSWORD environment variable.\n"
            "Example: export INSPIRE_PASSWORD='your_password'"
        )
    
    return username, password


def main():
    """
    主函数，提供命令行接口
    """
    parser = argparse.ArgumentParser(
        description='启智平台分布式训练任务状态监控工具',
        epilog='凭证通过环境变量提供: INSPIRE_USERNAME 和 INSPIRE_PASSWORD'
    )
    
    # 全局选项
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--base-url', type=str, default="https://qz.sii.edu.cn", 
                       help='API基础URL (默认: https://qz.sii.edu.cn)')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 监控命令
    monitor_parser = subparsers.add_parser('monitor', help='监控任务状态')
    monitor_parser.add_argument('--job-id', required=True, type=str, help='任务ID')
    monitor_parser.add_argument('--interval', type=int, default=10, 
                               help='轮询间隔(秒) (默认: 10)')
    monitor_parser.add_argument('--timeout', type=int, default=3600, 
                               help='监控超时时间(秒) (默认: 3600)')
    monitor_parser.add_argument('--export', type=str, 
                               help='导出监控数据到文件')
    monitor_parser.add_argument('--notifications', action='store_true', 
                               help='启用状态变化通知')
    
    # GitHub通知相关参数
    monitor_parser.add_argument('--github-token', type=str, 
                               help='GitHub访问令牌 (也可通过环境变量GITHUB_TOKEN设置)')
    monitor_parser.add_argument('--github-repo', type=str, 
                               help='GitHub仓库 (格式: owner/repo)')
    monitor_parser.add_argument('--github-issue', type=int, 
                               help='GitHub Issue/PR号码')
    
    # 状态查询命令
    status_parser = subparsers.add_parser('status', help='查询当前任务状态')
    status_parser.add_argument('--job-id', required=True, type=str, help='任务ID')
    status_parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    try:
        # 从环境变量获取凭证
        username, password = get_credentials()
        
        # 准备GitHub配置
        github_config = None
        if args.command == 'monitor' and args.notifications:
            # 从命令行参数或环境变量获取GitHub配置
            github_token = args.github_token or os.getenv('GITHUB_TOKEN')
            github_repo = args.github_repo or os.getenv('GITHUB_REPOSITORY')
            github_issue = args.github_issue or os.getenv('GITHUB_ISSUE_NUMBER')
            
            if github_token and github_repo and github_issue:
                github_config = {
                    'token': github_token,
                    'repo': github_repo,
                    'issue_number': str(github_issue)
                }
                logger.info(f"GitHub notifications enabled for {github_repo}#{github_issue}")
            elif args.notifications:
                logger.warning("GitHub notification requested but missing configuration")
                logger.warning("Required: --github-token, --github-repo, --github-issue")
                logger.warning("Or set environment variables: GITHUB_TOKEN, GITHUB_REPOSITORY, GITHUB_ISSUE_NUMBER")
        
        # 创建监控配置
        config = MonitorConfig(
            base_url=args.base_url,
            poll_interval=getattr(args, 'interval', 10),
            timeout=getattr(args, 'timeout', 3600),
            export_file=getattr(args, 'export', None),
            enable_notifications=getattr(args, 'notifications', False),
            github_config=github_config
        )
        
        # 创建监控器
        monitor = JobMonitor(config)
        
        # 认证
        logger.info("Authenticating with Inspire API...")
        if not monitor.authenticate(username, password):
            logger.error("Authentication failed")
            return 1
        
        # 根据命令执行相应操作
        if args.command == 'monitor':
            success = monitor.monitor_job(args.job_id)
            return 0 if success else 1
        
        elif args.command == 'status':
            snapshot = monitor.get_job_status(args.job_id)
            if snapshot is None:
                logger.error("Failed to get job status")
                return 1
            
            if args.json:
                print(json.dumps(asdict(snapshot), indent=2, ensure_ascii=False))
            else:
                monitor.print_status_summary(snapshot)
            return 0
        
        else:
            parser.print_help()
            return 1
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        return 1
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
