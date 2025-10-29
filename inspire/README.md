# 启智分布式训练任务创建工具

这是一个用于在启智平台上创建和管理分布式训练任务的Python工具。

## 功能

- 获取启智平台访问令牌
- 创建分布式训练任务
- 查询训练任务详情
- 停止训练任务
- 列出集群节点信息

## 环境要求

- Python 3.6+
- requests库

## 安装依赖

```bash
pip install requests
```

## 配置认证信息

在使用前，需要配置启智平台的认证信息。可以通过以下方式之一：

1. 环境变量：
```bash
export INSPIRE_USERNAME='你的用户名'
export INSPIRE_PASSWORD='你的密码'
```

2. 命令行参数：
```bash
--username '你的用户名' --password '你的密码'
```

## 使用方法

### 命令行使用

#### 创建分布式训练任务

# 使用默认值的简单命令 (需要先设置环境变量或使用脚本中的默认值)
```bash
python inspire_api_control.py create \
  --name 'hzz-api-training-test' \
  --start-command 'cd util-scripts && python video_check.py'
```

# 启智平台中的计算资源（如CPU、GPU、内存等）只能以一些固定的组合形式选定
不支持自定义，可以通过表格查看可用规格及spec_id/compute-group-id：
目前经验：不同节点 不同计算类型组 相同资源组合id相同（H100和H200的quota id相同）
| 配置类型 | CPU核数 | 内存 | GPU配置 | quota-ID |
|---------|---------|------|---------|----------|
| 单个节点 | 15核 | 200GB | 1 × NVIDIA H200 (141GB) | 4dd0e854-e2a4-4253-95e6-64c13f0b5117 |
| 单个节点 | 60核 | 800GB | 4 × NVIDIA H200 (141GB) | 45ab2351-fc8a-4d50-a30b-b39a5306c906 |
| 单个节点 | 120核 | 1600GB | 8 × NVIDIA H200 (141GB) | b618f5cb-c119-4422-937e-f39131853076 |


| 计算类型组 | compute-group-id |
|---------|-------------------|
| cuda12.8版本H100 | lcg-79b2ad0e-a375-43f3-a0b1-b4ce79710fd7 |
| H200-1号机房 | lcg-df089db8-817a-4aa8-a164-eb1a32948564 |
| H200-2号机房 | lcg-303ac8c6-aa19-4284-af03-2296592326e5 |
| H200-3号机房 | lcg-a91ad10b-415d-4abd-8170-828a2feae5d2 |



#### 查询任务详情
```bash
python inspire_api_control.py detail \
  --job-id 'job-3d35234d-e716-4872-9ce9-ce00222342d0'
```

#### 停止训练任务
```bash
python inspire_api_control.py stop \
  --job-id 'job-abc123'
```

#### 列出集群节点
```bash
python inspire_api_control.py list-nodes \
  --size 20
```

### Python API 使用

```python
from inspire_api_control import InspireAPI

# 创建API客户端
api = InspireAPI()

# 认证
if api.authenticate('username', 'password'):
    # 创建训练任务
    result = api.create_training_job(
        name="example-job",
        logic_compute_group_id="group-123",
        project_id="project-123",
        workspace_id="workspace-123",
        framework="pytorch",
        command="python train.py --epochs 10",
        cpu=4,
        gpu_count=1,
        mem_gi=8,
        instance_count=2
    )
    
    if result:
        print("任务创建成功")
```

## 参数说明

### 创建训练任务参数

- `--name`: 训练任务名称（必需）
- `--compute-group-id`: 计算资源组ID（必需）
- `--project-id`: 项目ID（必需）
- `--workspace-id`: 工作空间ID（必需）
- `--framework`: 训练框架（如pytorch, tensorflow等）（必需）
- `--command`: 启动命令（必需）
- `--priority`: 任务优先级（默认: 4）
- `--spec-id`: 计算资源规格ID（默认: H200*1）
- `--image`: 镜像名称（可选）
- `--instances`: 实例数量（默认: 1）

### 列出节点参数

- `--page`: 页码（默认: 1）
- `--size`: 每页数量（默认: 10）
- `--pool`: 资源池过滤（online, backup, fault, unknown）

## 示例

运行示例脚本查看使用方法：
```bash
python example_usage.py
```

## API说明

此工具基于启智OpenAPI文档实现，包括：

- Token认证
- 分布式训练任务创建
- 任务详情查询
- 任务停止
- 节点列表查询

参考文档：`inspire/inspire_Openapi.md`

## 注意事项

1. 在创建训练任务前，请确保你知道正确的计算资源组ID、项目ID和工作空间ID
2. 检查可用的计算资源以确保任务可以成功调度
3. 合理配置任务资源（CPU、GPU、内存），避免资源冲突
4. 任务创建后，可以通过任务ID查询和管理任务
