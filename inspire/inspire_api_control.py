#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启智(Inspire)分布式训练任务创建脚本 - 兼容性修复版本
Create distributed training tasks in the Inspire platform - Compatibility Fixed Version

This script provides functionality to:
- Authenticate with the Inspire API
- Create distributed training jobs
- Query training job details
- Stop training jobs
- List cluster nodes

API Documentation: https://qz.sii.edu.cn/openapi/

兼容性修复内容：
- 修复urllib3版本兼容性问题
- 简化重试机制
- 保持所有安全改进
"""

import os
import json
import logging
import requests
import argparse
import time
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class InspireConfig:
    """Inspire API 配置类"""
    base_url: str = "https://qz.sii.edu.cn"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0  # Simplified retry delay


class APIEndpoints:
    """API 端点常量"""
    AUTH_TOKEN = "/auth/token"
    TRAIN_JOB_CREATE = "/openapi/v1/train_job/create"
    TRAIN_JOB_DETAIL = "/openapi/v1/train_job/detail"
    TRAIN_JOB_STOP = "/openapi/v1/train_job/stop"
    SPECS_LIST = "/openapi/v1/specs/list"
    CLUSTER_NODES_LIST = "/openapi/v1/cluster_nodes/list"


class InspireAPIError(Exception):
    """Inspire API 基础异常"""
    pass


class AuthenticationError(InspireAPIError):
    """认证失败异常"""
    pass


class JobCreationError(InspireAPIError):
    """任务创建失败异常"""
    pass


class ValidationError(InspireAPIError):
    """输入验证失败异常"""
    pass


class InspireAPI:
    """
    启智API客户端 - 兼容性修复版
    Inspire API Client - Compatibility Fixed Version
    """
    
    # 默认值常量
    DEFAULT_TASK_PRIORITY = 4
    DEFAULT_INSTANCE_COUNT = 1
    DEFAULT_SHM_SIZE = 1
    DEFAULT_MAX_RUNNING_TIME = "3600000"  # 1小时
    DEFAULT_IMAGE_TYPE = "SOURCE_OFFICIAL"
    
    def __init__(self, config: Optional[InspireConfig] = None):
        """
        初始化API客户端
        
        Args:
            config: API配置对象，如果为None则使用默认配置
        """
        self.config = config or InspireConfig()
        self.base_url = self.config.base_url.rstrip('/')
        self.token = None
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 使用简单的requests session，避免urllib3兼容性问题
        self.session = requests.Session()
    
    def _validate_required_params(self, **kwargs) -> None:
        """验证必需参数"""
        for param_name, param_value in kwargs.items():
            if param_value is None or (isinstance(param_value, str) and not param_value.strip()):
                raise ValidationError(f"Required parameter '{param_name}' cannot be empty")
    
    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        带重试机制的请求方法
        
        Args:
            method: HTTP方法
            url: 请求URL
            **kwargs: requests参数
            
        Returns:
            Response对象
            
        Raises:
            InspireAPIError: 请求失败时
        """
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if method.upper() == 'POST':
                    response = self.session.post(url, timeout=self.config.timeout, **kwargs)
                else:
                    response = self.session.get(url, timeout=self.config.timeout, **kwargs)
                
                # 检查HTTP状态码
                if response.status_code < 500:
                    # 非服务器错误，不重试
                    return response
                else:
                    # 服务器错误，可能重试
                    if attempt < self.config.max_retries:
                        logger.warning(f"Server error {response.status_code}, retrying in {self.config.retry_delay}s...")
                        time.sleep(self.config.retry_delay * (attempt + 1))
                        continue
                    else:
                        response.raise_for_status()
                        
            except requests.exceptions.Timeout as e:
                last_exception = e
                if attempt < self.config.max_retries:
                    logger.warning(f"Request timeout, retrying in {self.config.retry_delay}s...")
                    time.sleep(self.config.retry_delay * (attempt + 1))
                    continue
                else:
                    raise InspireAPIError(f"Request timeout after {self.config.max_retries} retries")
                    
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                if attempt < self.config.max_retries:
                    logger.warning(f"Connection error, retrying in {self.config.retry_delay}s...")
                    time.sleep(self.config.retry_delay * (attempt + 1))
                    continue
                else:
                    raise InspireAPIError(f"Connection error after {self.config.max_retries} retries: {str(e)}")
                    
            except requests.exceptions.RequestException as e:
                # 其他请求异常，不重试
                raise InspireAPIError(f"Request failed: {str(e)}")
        
        # 如果到这里，说明所有重试都失败了
        if last_exception:
            raise InspireAPIError(f"All retry attempts failed. Last error: {str(last_exception)}")
        else:
            raise InspireAPIError("All retry attempts failed")
    
    def _make_request(self, method: str, endpoint: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送HTTP请求的通用方法
        
        Args:
            method: HTTP方法
            endpoint: API端点
            payload: 请求负载
            
        Returns:
            API响应数据
            
        Raises:
            InspireAPIError: 请求失败时
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            kwargs = {'headers': self.headers}
            if payload is not None:
                kwargs['json'] = payload
            
            response = self._make_request_with_retry(method, url, **kwargs)
            
            logger.debug(f"Request: {method} {url}")
            logger.debug(f"Response status: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            if not isinstance(result, dict) or 'code' not in result:
                raise InspireAPIError("Invalid API response format")
                
            return result
            
        except json.JSONDecodeError:
            raise InspireAPIError("Invalid JSON response from API")
        except requests.exceptions.RequestException as e:
            # 这里的异常应该已经被_make_request_with_retry处理了
            raise InspireAPIError(f"Request failed: {str(e)}")
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        使用用户名和密码获取访问令牌
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            成功返回True，否则抛出异常
            
        Raises:
            AuthenticationError: 认证失败时
            ValidationError: 参数验证失败时
        """
        self._validate_required_params(username=username, password=password)
        
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            result = self._make_request('POST', APIEndpoints.AUTH_TOKEN, payload)
            
            if result.get('code') == 0:
                self.token = result['data']['access_token']
                self.headers['Authorization'] = f"Bearer {self.token}"
                expires_in = result['data'].get('expires_in', 'unknown')
                logger.info(f"Authentication successful. Token expires in {expires_in} seconds.")
                return True
            else:
                error_msg = result.get('message', 'Unknown authentication error')
                raise AuthenticationError(f"Authentication failed: {error_msg}")
                
        except InspireAPIError as e:
            if "Authentication failed" in str(e):
                raise
            raise AuthenticationError(f"Authentication request failed: {str(e)}")
    
    def _check_authentication(self) -> None:
        """检查是否已认证"""
        if not self.token:
            raise AuthenticationError("Not authenticated. Please authenticate first.")
    
    def create_training_job(self, 
                           name: str, 
                           logic_compute_group_id: str, 
                           project_id: str,
                           workspace_id: str,
                           framework: str,
                           command: str,
                           spec_id: str,
                           task_priority: int = DEFAULT_TASK_PRIORITY,
                           auto_fault_tolerance: bool = False,
                           enable_notification: bool = False,
                           enable_troubleshoot: bool = False,
                           image: str = "",
                           image_type: str = DEFAULT_IMAGE_TYPE,
                           instance_count: int = DEFAULT_INSTANCE_COUNT,
                           shm_gi: int = DEFAULT_SHM_SIZE,
                           max_running_time_ms: str = DEFAULT_MAX_RUNNING_TIME,
                           reserve_on_fail_ms: str = "0",
                           reserve_on_success_ms: str = "0",
                           tb_summary_path: str = "",
                           dataset_info: Optional[list] = None,
                           envs: Optional[list] = None) -> Dict[str, Any]:
        """
        创建分布式训练任务
        
        Args:
            name: 训练任务名称
            logic_compute_group_id: 计算资源组ID
            project_id: 项目ID
            workspace_id: 工作空间ID
            framework: 训练框架 (如: tensorflow, pytorch等)
            command: 启动命令
            spec_id: 规格ID (用于指定CPU、GPU、内存等资源配置)
            task_priority: 任务优先级 (默认: 4)
            auto_fault_tolerance: 是否开启容错 (默认: False)
            enable_notification: 是否启用通知 (默认: False)
            enable_troubleshoot: 是否启用故障排除 (默认: False)
            image: 镜像名称
            image_type: 镜像类型 (默认: SOURCE_OFFICIAL)
            instance_count: 实例数量 (默认: 1)
            shm_gi: 共享内存大小 (默认: 1)
            max_running_time_ms: 最大运行时间(毫秒) (默认: 3600000 = 1小时)
            reserve_on_fail_ms: 失败时保留时间(毫秒) (默认: 0)
            reserve_on_success_ms: 成功时保留时间(毫秒) (默认: 0)
            tb_summary_path: TensorBoard摘要路径 (默认: "")
            dataset_info: 数据集信息列表 (默认: None)
            envs: 环境变量列表 (默认: None)
            
        Returns:
            API响应数据
            
        Raises:
            ValidationError: 参数验证失败时
            JobCreationError: 任务创建失败时
            AuthenticationError: 未认证时
        """
        self._check_authentication()
        
        # 验证必需参数
        self._validate_required_params(
            name=name,
            logic_compute_group_id=logic_compute_group_id,
            project_id=project_id,
            workspace_id=workspace_id,
            framework=framework,
            command=command,
            spec_id=spec_id
        )
        
        # 验证数值参数
        if instance_count < 1:
            raise ValidationError("Instance count must be at least 1")
        if shm_gi < 1:
            raise ValidationError("Shared memory size must be at least 1")
        if task_priority < 1 or task_priority > 10:
            raise ValidationError("Task priority must be between 1 and 10")
        
        # 构建请求负载
        payload = {
            "name": name,
            "logic_compute_group_id": logic_compute_group_id,
            "project_id": project_id,
            "workspace_id": workspace_id,
            "framework": framework,
            "command": command,
            "task_priority": task_priority,
            "auto_fault_tolerance": auto_fault_tolerance,
            "enable_notification": enable_notification,
            "enable_troubleshoot": enable_troubleshoot,
            "max_running_time_ms": max_running_time_ms,
            "reserve_on_fail_ms": reserve_on_fail_ms,
            "reserve_on_success_ms": reserve_on_success_ms,
            "tb_summary_path": tb_summary_path,
            "framework_config": [{
                "image": image,
                "image_type": image_type,
                "instance_count": instance_count,
                "shm_gi": shm_gi,
                "spec_id": spec_id
            }],
            "dataset_info": dataset_info or [],
            "envs": envs or []
        }
        
        logger.debug("Creating training job with payload structure defined")
        
        try:
            result = self._make_request('POST', APIEndpoints.TRAIN_JOB_CREATE, payload)
            
            if result.get('code') == 0:
                logger.info(f"Training job '{name}' created successfully.")
                return result
            else:
                error_msg = result.get('message', 'Unknown error')
                raise JobCreationError(f"Failed to create training job: {error_msg}")
                
        except InspireAPIError as e:
            if "Failed to create training job" in str(e):
                raise
            raise JobCreationError(f"Training job creation request failed: {str(e)}")
    
    def get_job_detail(self, job_id: str) -> Dict[str, Any]:
        """
        获取训练任务详情
        
        Args:
            job_id: 任务ID
            
        Returns:
            任务详情数据
            
        Raises:
            ValidationError: 参数验证失败时
            InspireAPIError: 请求失败时
            AuthenticationError: 未认证时
        """
        self._check_authentication()
        self._validate_required_params(job_id=job_id)
        
        payload = {"job_id": job_id}
        
        result = self._make_request('POST', APIEndpoints.TRAIN_JOB_DETAIL, payload)
        
        if result.get('code') == 0:
            logger.info(f"Retrieved details for job {job_id}")
            return result
        else:
            error_msg = result.get('message', 'Unknown error')
            raise InspireAPIError(f"Failed to get job details: {error_msg}")
    
    def stop_training_job(self, job_id: str) -> bool:
        """
        停止训练任务
        
        Args:
            job_id: 任务ID
            
        Returns:
            成功返回True
            
        Raises:
            ValidationError: 参数验证失败时
            InspireAPIError: 请求失败时
            AuthenticationError: 未认证时
        """
        self._check_authentication()
        self._validate_required_params(job_id=job_id)
        
        payload = {"job_id": job_id}
        
        result = self._make_request('POST', APIEndpoints.TRAIN_JOB_STOP, payload)
        
        if result.get('code') == 0:
            logger.info(f"Training job {job_id} stopped successfully.")
            return True
        else:
            error_msg = result.get('message', 'Unknown error')
            raise InspireAPIError(f"Failed to stop training job: {error_msg}")
    
    def list_available_specs(self, logic_compute_group_id: str) -> Dict[str, Any]:
        """
        获取可用的规格列表
        
        Args:
            logic_compute_group_id: 计算资源组ID
            
        Returns:
            规格列表数据
            
        Raises:
            ValidationError: 参数验证失败时
            InspireAPIError: 请求失败时
            AuthenticationError: 未认证时
        """
        self._check_authentication()
        self._validate_required_params(logic_compute_group_id=logic_compute_group_id)
        
        payload = {"logic_compute_group_id": logic_compute_group_id}
        
        result = self._make_request('POST', APIEndpoints.SPECS_LIST, payload)
        
        if result.get('code') == 0:
            logger.info("Retrieved available specs successfully.")
            return result
        else:
            error_msg = result.get('message', 'Unknown error')
            raise InspireAPIError(f"Failed to get specs: {error_msg}")

    def list_cluster_nodes(self,
                          page_num: int = 1, 
                          page_size: int = 10,
                          resource_pool: Optional[str] = None) -> Dict[str, Any]:
        """
        获取集群节点列表
        
        Args:
            page_num: 页码 (默认: 1)
            page_size: 每页数量 (默认: 10)
            resource_pool: 资源池过滤 (online, backup, fault, unknown)
            
        Returns:
            节点列表数据
            
        Raises:
            ValidationError: 参数验证失败时
            InspireAPIError: 请求失败时
            AuthenticationError: 未认证时
        """
        self._check_authentication()
        
        if page_num < 1:
            raise ValidationError("Page number must be at least 1")
        if page_size < 1 or page_size > 100:
            raise ValidationError("Page size must be between 1 and 100")
        
        valid_pools = ['online', 'backup', 'fault', 'unknown']
        if resource_pool and resource_pool not in valid_pools:
            raise ValidationError(f"Resource pool must be one of: {valid_pools}")
        
        payload = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if resource_pool:
            payload["filter"] = {"resource_pool": resource_pool}
        
        result = self._make_request('POST', APIEndpoints.CLUSTER_NODES_LIST, payload)
        
        if result.get('code') == 0:
            node_count = len(result['data'].get('nodes', []))
            logger.info(f"Retrieved {node_count} nodes successfully.")
            return result
        else:
            error_msg = result.get('message', 'Unknown error')
            raise InspireAPIError(f"Failed to get node list: {error_msg}")


def get_credentials() -> tuple[str, str]:
    """
    从环境变量获取凭证
    
    Returns:
        (username, password) 元组
        
    Raises:
        ValidationError: 凭证不可用时
    """
    username = os.getenv('INSPIRE_USERNAME')
    password = os.getenv('INSPIRE_PASSWORD')
    
    if not username:
        raise ValidationError(
            "Username not found. Please set INSPIRE_USERNAME environment variable.\n"
            "Example: export INSPIRE_USERNAME='your_username'"
        )
    
    if not password:
        raise ValidationError(
            "Password not found. Please set INSPIRE_PASSWORD environment variable.\n"
            "Example: export INSPIRE_PASSWORD='your_password'"
        )
    
    return username, password


def main():
    """
    主函数，提供命令行接口
    """
    parser = argparse.ArgumentParser(
        description='启智平台分布式训练任务管理工具',
        epilog='凭证通过环境变量提供: INSPIRE_USERNAME 和 INSPIRE_PASSWORD'
    )
    
    # 全局选项
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--base-url', type=str, default="https://qz.sii.edu.cn", 
                       help='API基础URL (默认: https://qz.sii.edu.cn)')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 创建训练任务
    create_parser = subparsers.add_parser('create', help='创建分布式训练任务')
    create_parser.add_argument('--name', required=True, type=str, help='训练任务名称')
    create_parser.add_argument('--compute-group-id', type=str, 
                              default="lcg-303ac8c6-aa19-4284-af03-2296592326e5", 
                              help='计算资源组ID')
    create_parser.add_argument('--project-id', type=str, 
                              default="project-c67c548f-f02c-453b-ba5b-8745db6886e7", 
                              help='项目ID')
    create_parser.add_argument('--workspace-id', type=str, 
                              default="ws-9dcc0e1f-80a4-4af2-bc2f-0e352e7b17e6", 
                              help='工作空间ID')
    create_parser.add_argument('--framework', type=str, default="pytorch", help='训练框架')
    create_parser.add_argument('--start-command', required=True, type=str, help='启动命令')
    create_parser.add_argument('--spec-id', type=str, 
                              default="4dd0e854-e2a4-4253-95e6-64c13f0b5117", 
                              help='规格ID (默认: H200 GPU规格)。使用 list-specs 命令可查看其他可用规格')
    create_parser.add_argument('--priority', type=int, default=8, help='任务优先级 (默认: 8)')
    create_parser.add_argument('--image', type=str, 
                              default="docker.sii.shaipower.online/inspire-studio/ngc-cuda12.4-base:1.0", 
                              help='镜像名称')
    create_parser.add_argument('--instances', type=int, default=1, help='实例数量 (默认: 1)')
    create_parser.add_argument('--shm-size', type=int, default=1, help='共享内存大小(Gi) (默认: 1)')
    create_parser.add_argument('--max-time', type=str, default="3600000", 
                              help='最大运行时间(毫秒) (默认: 3600000)')
    create_parser.add_argument('--auto-fault-tolerance', action='store_true', help='开启自动容错')
    create_parser.add_argument('--enable-notification', action='store_true', help='启用通知')
    create_parser.add_argument('--enable-troubleshoot', action='store_true', help='启用故障排除')
    
    # 查询任务详情
    detail_parser = subparsers.add_parser('detail', help='查询训练任务详情')
    detail_parser.add_argument('--job-id', required=True, type=str, help='任务ID')
    
    # 停止训练任务
    stop_parser = subparsers.add_parser('stop', help='停止训练任务')
    stop_parser.add_argument('--job-id', required=True, type=str, help='任务ID')
    
    # 列出可用规格
    specs_parser = subparsers.add_parser('list-specs', help='列出可用的计算规格')
    specs_parser.add_argument('--compute-group-id', type=str, 
                             default="lcg-303ac8c6-aa19-4284-af03-2296592326e5", 
                             help='计算资源组ID')
    
    # 列出集群节点
    list_parser = subparsers.add_parser('list-nodes', help='列出集群节点')
    list_parser.add_argument('--page', type=int, default=1, help='页码 (默认: 1)')
    list_parser.add_argument('--size', type=int, default=10, help='每页数量 (默认: 10)')
    list_parser.add_argument('--pool', type=str, choices=['online', 'backup', 'fault', 'unknown'], 
                            help='资源池过滤')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    try:
        # 从环境变量获取凭证
        username, password = get_credentials()
        
        # 创建API客户端
        config = InspireConfig(base_url=args.base_url)
        api = InspireAPI(config)
        
        # 认证
        logger.info("Authenticating with Inspire API...")
        api.authenticate(username, password)
        
        # 根据命令执行相应操作
        if args.command == 'create':
            result = api.create_training_job(
                name=args.name,
                logic_compute_group_id=args.compute_group_id,
                project_id=args.project_id,
                workspace_id=args.workspace_id,
                framework=args.framework,
                command=args.start_command,
                spec_id=args.spec_id,
                task_priority=args.priority,
                auto_fault_tolerance=args.auto_fault_tolerance,
                enable_notification=args.enable_notification,
                enable_troubleshoot=args.enable_troubleshoot,
                image=args.image,
                instance_count=args.instances,
                shm_gi=args.shm_size,
                max_running_time_ms=args.max_time
            )
            
            print("创建结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'detail':
            result = api.get_job_detail(args.job_id)
            print("任务详情:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'stop':
            api.stop_training_job(args.job_id)
            print("任务已停止")
        
        elif args.command == 'list-specs':
            result = api.list_available_specs(args.compute_group_id)
            print("可用规格:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'list-nodes':
            result = api.list_cluster_nodes(
                page_num=args.page,
                page_size=args.size,
                resource_pool=args.pool
            )
            print("节点列表:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            parser.print_help()
            return 1
        
        return 0
        
    except (ValidationError, AuthenticationError, JobCreationError, InspireAPIError) as e:
        logger.error(f"Error: {str(e)}")
        return 1
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())