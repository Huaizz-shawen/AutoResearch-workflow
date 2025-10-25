---
title: 启智平台 openapi
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"

---

# 启智平台 openapi

Base URLs:

* <a href="https://qz.sii.edu.cn">正式环境: https://qz.sii.edu.cn</a>

# Authentication

# 认证

## POST 获取当前身份的 Access Token

POST /auth/token

> Body 请求参数

```json
{
  "password": "string",
  "username": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[pkg_openapi_controller_auth.GetAuthTokenReq](#schemapkg_openapi_controller_auth.getauthtokenreq)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "access_token": "string",
  "expires_in": 0,
  "token_type": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[pkg_openapi_controller_auth.GetAuthTokenResp](#schemapkg_openapi_controller_auth.getauthtokenresp)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|none|string|

# 分布式训练

## POST 创建分布式训练任务

POST /openapi/v1/train_job/create

> Body 请求参数

```json
{
  "auto_fault_tolerance": true,
  "command": "string",
  "dataset_info": [
    {
      "dataset_id": "string",
      "path": "string",
      "version_id": "string"
    }
  ],
  "enable_notification": true,
  "enable_troubleshoot": true,
  "envs": [
    {
      "name": "string",
      "value": "string"
    }
  ],
  "framework": "string",
  "framework_config": [
    {
      "image": "string",
      "image_type": "string",
      "instance_count": 0,
      "shm_gi": 0,
      "spec_id": "string"
    }
  ],
  "logic_compute_group_id": "string",
  "max_running_time_ms": "string",
  "name": "string",
  "project_id": "string",
  "reserve_on_fail_ms": "string",
  "reserve_on_success_ms": "string",
  "task_priority": 0,
  "tb_summary_path": "string",
  "workspace_id": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[pkg_openapi_controller_train.JobOpenapi](#schemapkg_openapi_controller_train.jobopenapi)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "auto_fault_tolerance": true,
  "auto_fault_tolerance_params": "string",
  "command": "string",
  "config_mode": 0,
  "created_at": "string",
  "created_by": {
    "avatar_url": "string",
    "created_at": "string",
    "email": "string",
    "extra_info": {
      "institution_id": "string",
      "login_name": "string"
    },
    "global_role": 0,
    "id": "string",
    "name": "string",
    "name_en": "string"
  },
  "current_running_round": 0,
  "dataset_info": [
    {
      "dataset_id": "string",
      "path": "string",
      "version_id": "string"
    }
  ],
  "enable_notification": true,
  "enable_troubleshoot": true,
  "envs": [
    {
      "name": "string",
      "value": "string"
    }
  ],
  "fault_tolerance_max_retry": 0,
  "fault_tolerance_retry_interval_sec": 0,
  "finished_at": "string",
  "framework": "string",
  "framework_config": [
    {
      "cpu": 0,
      "gpu_count": 0,
      "image": "string",
      "image_type": "string",
      "instance_count": 0,
      "instance_spec_price_info": {
        "cpu_count": 0,
        "cpu_info": {},
        "cpu_price": 0,
        "cpu_price_id": "string",
        "cpu_price_version_id": 0,
        "gpu_count": 0,
        "gpu_info": {},
        "gpu_price": 0,
        "gpu_price_id": "string",
        "gpu_price_version_id": 0,
        "memory_price": 0,
        "memory_price_id": "string",
        "memory_price_version_id": 0,
        "memory_size_gib": 0,
        "quota_id": "string",
        "total_price_per_hour": 0
      },
      "mem_gi": 0,
      "predef_id": "string",
      "replicas_type": 0,
      "resource_spec_price": {
        "cpu_count": 0,
        "cpu_type": "string",
        "gpu_count": 0,
        "gpu_type": "string",
        "logic_compute_group_id": "string",
        "memory_size_gib": 0,
        "quota_id": "string"
      },
      "shm_gi": 0
    }
  ],
  "job_id": "string",
  "logic_compute_group_id": "string",
  "logic_compute_group_name": "string",
  "max_running_time_ms": "string",
  "mounts": [
    {
      "mount_path": "string",
      "real_path": "string",
      "volume": "string"
    }
  ],
  "name": "string",
  "node_count": 0,
  "node_infos": [
    {
      "node_name": "string"
    }
  ],
  "priority": 0,
  "priority_level": 0,
  "priority_name": "string",
  "project_en_name": "string",
  "project_id": "string",
  "project_name": "string",
  "queue_id": "string",
  "queue_name": "string",
  "reserve_on_fail_ms": "string",
  "reserve_on_success_ms": "string",
  "running_time_ms": "string",
  "status": "string",
  "sub_code": 0,
  "sub_msg": "string",
  "sub_status": 0,
  "task_priority": 0,
  "tb_id": "string",
  "tb_summary_path": "string",
  "timeline": {
    "created": "string",
    "finished": "string",
    "resource_prepared": "string",
    "run": "string"
  },
  "workspace_id": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[pkg_openapi_controller_train.Job](#schemapkg_openapi_controller_train.job)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|none|string|

## POST 获取分布式训练任务详情

POST /openapi/v1/train_job/detail

> Body 请求参数

```json
{
  "job_id": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[pkg_openapi_controller_train.DetailReq](#schemapkg_openapi_controller_train.detailreq)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "auto_fault_tolerance": true,
  "auto_fault_tolerance_params": "string",
  "command": "string",
  "config_mode": 0,
  "created_at": "string",
  "created_by": {
    "avatar_url": "string",
    "created_at": "string",
    "email": "string",
    "extra_info": {
      "institution_id": "string",
      "login_name": "string"
    },
    "global_role": 0,
    "id": "string",
    "name": "string",
    "name_en": "string"
  },
  "current_running_round": 0,
  "dataset_info": [
    {
      "dataset_id": "string",
      "path": "string",
      "version_id": "string"
    }
  ],
  "enable_notification": true,
  "enable_troubleshoot": true,
  "envs": [
    {
      "name": "string",
      "value": "string"
    }
  ],
  "fault_tolerance_max_retry": 0,
  "fault_tolerance_retry_interval_sec": 0,
  "finished_at": "string",
  "framework": "string",
  "framework_config": [
    {
      "cpu": 0,
      "gpu_count": 0,
      "image": "string",
      "image_type": "string",
      "instance_count": 0,
      "instance_spec_price_info": {
        "cpu_count": 0,
        "cpu_info": {},
        "cpu_price": 0,
        "cpu_price_id": "string",
        "cpu_price_version_id": 0,
        "gpu_count": 0,
        "gpu_info": {},
        "gpu_price": 0,
        "gpu_price_id": "string",
        "gpu_price_version_id": 0,
        "memory_price": 0,
        "memory_price_id": "string",
        "memory_price_version_id": 0,
        "memory_size_gib": 0,
        "quota_id": "string",
        "total_price_per_hour": 0
      },
      "mem_gi": 0,
      "predef_id": "string",
      "replicas_type": 0,
      "resource_spec_price": {
        "cpu_count": 0,
        "cpu_type": "string",
        "gpu_count": 0,
        "gpu_type": "string",
        "logic_compute_group_id": "string",
        "memory_size_gib": 0,
        "quota_id": "string"
      },
      "shm_gi": 0
    }
  ],
  "job_id": "string",
  "logic_compute_group_id": "string",
  "logic_compute_group_name": "string",
  "max_running_time_ms": "string",
  "mounts": [
    {
      "mount_path": "string",
      "real_path": "string",
      "volume": "string"
    }
  ],
  "name": "string",
  "node_count": 0,
  "node_infos": [
    {
      "node_name": "string"
    }
  ],
  "priority": 0,
  "priority_level": 0,
  "priority_name": "string",
  "project_en_name": "string",
  "project_id": "string",
  "project_name": "string",
  "queue_id": "string",
  "queue_name": "string",
  "reserve_on_fail_ms": "string",
  "reserve_on_success_ms": "string",
  "running_time_ms": "string",
  "status": "string",
  "sub_code": 0,
  "sub_msg": "string",
  "sub_status": 0,
  "task_priority": 0,
  "tb_id": "string",
  "tb_summary_path": "string",
  "timeline": {
    "created": "string",
    "finished": "string",
    "resource_prepared": "string",
    "run": "string"
  },
  "workspace_id": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[pkg_openapi_controller_train.Job](#schemapkg_openapi_controller_train.job)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|none|string|

## POST 停止分布式训练任务

POST /openapi/v1/train_job/stop

> Body 请求参数

```json
{
  "job_id": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[pkg_openapi_controller_train.StopReq](#schemapkg_openapi_controller_train.stopreq)| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|none|string|

### 返回数据结构

# 数据模型

<h2 id="tocS_common.JobSubStatus">common.JobSubStatus</h2>

<a id="schemacommon.jobsubstatus"></a>
<a id="schema_common.JobSubStatus"></a>
<a id="tocScommon.jobsubstatus"></a>
<a id="tocscommon.jobsubstatus"></a>

```json
0

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|integer|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|*anonymous*|0|
|*anonymous*|1|

<h2 id="tocS_common.MountPath">common.MountPath</h2>

<a id="schemacommon.mountpath"></a>
<a id="schema_common.MountPath"></a>
<a id="tocScommon.mountpath"></a>
<a id="tocscommon.mountpath"></a>

```json
{
  "mount_path": "string",
  "real_path": "string",
  "volume": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|mount_path|string|false|none||none|
|real_path|string|false|none||none|
|volume|string|false|none||标识用哪个存储，当前只有一个存储，不需要填|

<h2 id="tocS_node.CpuInfo">node.CpuInfo</h2>

<a id="schemanode.cpuinfo"></a>
<a id="schema_node.CpuInfo"></a>
<a id="tocSnode.cpuinfo"></a>
<a id="tocsnode.cpuinfo"></a>

```json
{
  "brand": "string",
  "cpu_product_simple": "string",
  "cpu_type": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|brand|string|false|none||示例: Intel|
|cpu_product_simple|string|false|none||示例: Xeon 6330|
|cpu_type|string|false|none||示例: Intel_Xeon_6330|

<h2 id="tocS_node.GpuInfo">node.GpuInfo</h2>

<a id="schemanode.gpuinfo"></a>
<a id="schema_node.GpuInfo"></a>
<a id="tocSnode.gpuinfo"></a>
<a id="tocsnode.gpuinfo"></a>

```json
{
  "brand": "string",
  "brand_name": "string",
  "gpu_memory_size_gb": 0,
  "gpu_product_simple": "string",
  "gpu_type": "string",
  "gpu_type_display": "string",
  "price": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|brand|string|false|none||示例: NVIDIA|
|brand_name|string|false|none||示例: 英伟达|
|gpu_memory_size_gb|number|false|none||示例: 80|
|gpu_product_simple|string|false|none||示例: H100|
|gpu_type|string|false|none||示例: NVIDIA_A100_SXM_80G|
|gpu_type_display|string|false|none||示例: NVIDIA A100 (80G)|
|price|string|false|none||示例: 1.0|

<h2 id="tocS_pkg_openapi_controller_auth.GetAuthTokenReq">pkg_openapi_controller_auth.GetAuthTokenReq</h2>

<a id="schemapkg_openapi_controller_auth.getauthtokenreq"></a>
<a id="schema_pkg_openapi_controller_auth.GetAuthTokenReq"></a>
<a id="tocSpkg_openapi_controller_auth.getauthtokenreq"></a>
<a id="tocspkg_openapi_controller_auth.getauthtokenreq"></a>

```json
{
  "password": "string",
  "username": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|password|string|false|none||none|
|username|string|false|none||none|

<h2 id="tocS_pkg_openapi_controller_auth.GetAuthTokenResp">pkg_openapi_controller_auth.GetAuthTokenResp</h2>

<a id="schemapkg_openapi_controller_auth.getauthtokenresp"></a>
<a id="schema_pkg_openapi_controller_auth.GetAuthTokenResp"></a>
<a id="tocSpkg_openapi_controller_auth.getauthtokenresp"></a>
<a id="tocspkg_openapi_controller_auth.getauthtokenresp"></a>

```json
{
  "access_token": "string",
  "expires_in": 0,
  "token_type": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|access_token|string|false|none||none|
|expires_in|integer|false|none||none|
|token_type|string|false|none||none|

<h2 id="tocS_pkg_openapi_controller_train.DetailReq">pkg_openapi_controller_train.DetailReq</h2>

<a id="schemapkg_openapi_controller_train.detailreq"></a>
<a id="schema_pkg_openapi_controller_train.DetailReq"></a>
<a id="tocSpkg_openapi_controller_train.detailreq"></a>
<a id="tocspkg_openapi_controller_train.detailreq"></a>

```json
{
  "job_id": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|job_id|string|false|none||none|

<h2 id="tocS_pkg_openapi_controller_train.Job">pkg_openapi_controller_train.Job</h2>

<a id="schemapkg_openapi_controller_train.job"></a>
<a id="schema_pkg_openapi_controller_train.Job"></a>
<a id="tocSpkg_openapi_controller_train.job"></a>
<a id="tocspkg_openapi_controller_train.job"></a>

```json
{
  "auto_fault_tolerance": true,
  "auto_fault_tolerance_params": "string",
  "command": "string",
  "config_mode": 0,
  "created_at": "string",
  "created_by": {
    "avatar_url": "string",
    "created_at": "string",
    "email": "string",
    "extra_info": {
      "institution_id": "string",
      "login_name": "string"
    },
    "global_role": 0,
    "id": "string",
    "name": "string",
    "name_en": "string"
  },
  "current_running_round": 0,
  "dataset_info": [
    {
      "dataset_id": "string",
      "path": "string",
      "version_id": "string"
    }
  ],
  "enable_notification": true,
  "enable_troubleshoot": true,
  "envs": [
    {
      "name": "string",
      "value": "string"
    }
  ],
  "fault_tolerance_max_retry": 0,
  "fault_tolerance_retry_interval_sec": 0,
  "finished_at": "string",
  "framework": "string",
  "framework_config": [
    {
      "cpu": 0,
      "gpu_count": 0,
      "image": "string",
      "image_type": "string",
      "instance_count": 0,
      "instance_spec_price_info": {
        "cpu_count": 0,
        "cpu_info": {},
        "cpu_price": 0,
        "cpu_price_id": "string",
        "cpu_price_version_id": 0,
        "gpu_count": 0,
        "gpu_info": {},
        "gpu_price": 0,
        "gpu_price_id": "string",
        "gpu_price_version_id": 0,
        "memory_price": 0,
        "memory_price_id": "string",
        "memory_price_version_id": 0,
        "memory_size_gib": 0,
        "quota_id": "string",
        "total_price_per_hour": 0
      },
      "mem_gi": 0,
      "predef_id": "string",
      "replicas_type": 0,
      "resource_spec_price": {
        "cpu_count": 0,
        "cpu_type": "string",
        "gpu_count": 0,
        "gpu_type": "string",
        "logic_compute_group_id": "string",
        "memory_size_gib": 0,
        "quota_id": "string"
      },
      "shm_gi": 0
    }
  ],
  "job_id": "string",
  "logic_compute_group_id": "string",
  "logic_compute_group_name": "string",
  "max_running_time_ms": "string",
  "mounts": [
    {
      "mount_path": "string",
      "real_path": "string",
      "volume": "string"
    }
  ],
  "name": "string",
  "node_count": 0,
  "node_infos": [
    {
      "node_name": "string"
    }
  ],
  "priority": 0,
  "priority_level": 0,
  "priority_name": "string",
  "project_en_name": "string",
  "project_id": "string",
  "project_name": "string",
  "queue_id": "string",
  "queue_name": "string",
  "reserve_on_fail_ms": "string",
  "reserve_on_success_ms": "string",
  "running_time_ms": "string",
  "status": "string",
  "sub_code": 0,
  "sub_msg": "string",
  "sub_status": 0,
  "task_priority": 0,
  "tb_id": "string",
  "tb_summary_path": "string",
  "timeline": {
    "created": "string",
    "finished": "string",
    "resource_prepared": "string",
    "run": "string"
  },
  "workspace_id": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|auto_fault_tolerance|boolean|false|none||是否自动容错|
|auto_fault_tolerance_params|string|false|none||额外参数 废弃字段|
|command|string|false|none||none|
|config_mode|[train.ConfigMode](#schematrain.configmode)|false|none||ConfigMode|
|created_at|string|false|none||创建时间 ms级时间戳|
|created_by|[user.UserBase](#schemauser.userbase)|false|none||none|
|current_running_round|integer|false|none||当前运行轮次|
|dataset_info|[[train.DatasetInfo](#schematrain.datasetinfo)]|false|none||none|
|enable_notification|boolean|false|none||none|
|enable_troubleshoot|boolean|false|none||none|
|envs|[[train.Env](#schematrain.env)]|false|none||环境变量|
|fault_tolerance_max_retry|integer|false|none||容错的最大重试次数|
|fault_tolerance_retry_interval_sec|integer|false|none||重试间隔 秒|
|finished_at|string|false|none||结束时间 ms级时间戳|
|framework|string|false|none||枚举值参见 Framework|
|framework_config|[[train.FrameworkConfigStandard](#schematrain.frameworkconfigstandard)]|false|none||不同framework的config可能不同 json格式字符串|
|job_id|string|false|none||以下为列表和详情的数据，创建时不传|
|logic_compute_group_id|string|false|none||none|
|logic_compute_group_name|string|false|none||none|
|max_running_time_ms|string|false|none||最大运行时间 单位ms|
|mounts|[[common.MountPath](#schemacommon.mountpath)]|false|none||挂载信息 废弃字段|
|name|string|false|none||none|
|node_count|integer|false|none||none|
|node_infos|[[train.NodeInfo](#schematrain.nodeinfo)]|false|none||none|
|priority|[project.ProjectPriority](#schemaproject.projectpriority)|false|none||none|
|priority_level|[project.ProjectPriority](#schemaproject.projectpriority)|false|none||none|
|priority_name|string|false|none||none|
|project_en_name|string|false|none||none|
|project_id|string|false|none||none|
|project_name|string|false|none||none|
|queue_id|string|false|none||none|
|queue_name|string|false|none||none|
|reserve_on_fail_ms|string|false|none||失败时保留时间|
|reserve_on_success_ms|string|false|none||成功时保留时间|
|running_time_ms|string|false|none||执行时长 单位ms|
|status|string|false|none||jobStatus|
|sub_code|integer|false|none||none|
|sub_msg|string|false|none||创建时排队会返回|
|sub_status|[common.JobSubStatus](#schemacommon.jobsubstatus)|false|none||none|
|task_priority|integer|false|none||none|
|tb_id|string|false|none||是否存在关联的tb, 有的时候才会这个字段|
|tb_summary_path|string|false|none||none|
|timeline|[train.Timeline](#schematrain.timeline)|false|none||以下为详情数据<br />时间线|
|workspace_id|string|false|none||none|

<h2 id="tocS_pkg_openapi_controller_train.JobOpenapi">pkg_openapi_controller_train.JobOpenapi</h2>

<a id="schemapkg_openapi_controller_train.jobopenapi"></a>
<a id="schema_pkg_openapi_controller_train.JobOpenapi"></a>
<a id="tocSpkg_openapi_controller_train.jobopenapi"></a>
<a id="tocspkg_openapi_controller_train.jobopenapi"></a>

```json
{
  "auto_fault_tolerance": true,
  "command": "string",
  "dataset_info": [
    {
      "dataset_id": "string",
      "path": "string",
      "version_id": "string"
    }
  ],
  "enable_notification": true,
  "enable_troubleshoot": true,
  "envs": [
    {
      "name": "string",
      "value": "string"
    }
  ],
  "framework": "string",
  "framework_config": [
    {
      "image": "string",
      "image_type": "string",
      "instance_count": 0,
      "shm_gi": 0,
      "spec_id": "string"
    }
  ],
  "logic_compute_group_id": "string",
  "max_running_time_ms": "string",
  "name": "string",
  "project_id": "string",
  "reserve_on_fail_ms": "string",
  "reserve_on_success_ms": "string",
  "task_priority": 0,
  "tb_summary_path": "string",
  "workspace_id": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|auto_fault_tolerance|boolean|false|none||可选字段|
|command|string|false|none||none|
|dataset_info|[[train.DatasetInfo](#schematrain.datasetinfo)]|false|none||none|
|enable_notification|boolean|false|none||none|
|enable_troubleshoot|boolean|false|none||none|
|envs|[[train.Env](#schematrain.env)]|false|none||none|
|framework|string|false|none||none|
|framework_config|[[train.FrameworkConfigOpenAPI](#schematrain.frameworkconfigopenapi)]|false|none||使用 OpenAPI 精简配置|
|logic_compute_group_id|string|false|none||none|
|max_running_time_ms|string|false|none||none|
|name|string|false|none||none|
|project_id|string|false|none||none|
|reserve_on_fail_ms|string|false|none||none|
|reserve_on_success_ms|string|false|none||none|
|task_priority|integer|false|none||none|
|tb_summary_path|string|false|none||none|
|workspace_id|string|false|none||none|

<h2 id="tocS_pkg_openapi_controller_train.StopReq">pkg_openapi_controller_train.StopReq</h2>

<a id="schemapkg_openapi_controller_train.stopreq"></a>
<a id="schema_pkg_openapi_controller_train.StopReq"></a>
<a id="tocSpkg_openapi_controller_train.stopreq"></a>
<a id="tocspkg_openapi_controller_train.stopreq"></a>

```json
{
  "job_id": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|job_id|string|false|none||none|

<h2 id="tocS_project.ProjectPriority">project.ProjectPriority</h2>

<a id="schemaproject.projectpriority"></a>
<a id="schema_project.ProjectPriority"></a>
<a id="tocSproject.projectpriority"></a>
<a id="tocsproject.projectpriority"></a>

```json
0

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|integer|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|*anonymous*|0|
|*anonymous*|1|
|*anonymous*|2|

<h2 id="tocS_resource_price.InstanceSpecPriceInfo">resource_price.InstanceSpecPriceInfo</h2>

<a id="schemaresource_price.instancespecpriceinfo"></a>
<a id="schema_resource_price.InstanceSpecPriceInfo"></a>
<a id="tocSresource_price.instancespecpriceinfo"></a>
<a id="tocsresource_price.instancespecpriceinfo"></a>

```json
{
  "cpu_count": 0,
  "cpu_info": {
    "brand": "string",
    "cpu_product_simple": "string",
    "cpu_type": "string"
  },
  "cpu_price": 0,
  "cpu_price_id": "string",
  "cpu_price_version_id": 0,
  "gpu_count": 0,
  "gpu_info": {
    "brand": "string",
    "brand_name": "string",
    "gpu_memory_size_gb": 0,
    "gpu_product_simple": "string",
    "gpu_type": "string",
    "gpu_type_display": "string",
    "price": "string"
  },
  "gpu_price": 0,
  "gpu_price_id": "string",
  "gpu_price_version_id": 0,
  "memory_price": 0,
  "memory_price_id": "string",
  "memory_price_version_id": 0,
  "memory_size_gib": 0,
  "quota_id": "string",
  "total_price_per_hour": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|cpu_count|number|false|none||none|
|cpu_info|[node.CpuInfo](#schemanode.cpuinfo)|false|none||none|
|cpu_price|number|false|none||none|
|cpu_price_id|string|false|none||none|
|cpu_price_version_id|integer|false|none||none|
|gpu_count|number|false|none||none|
|gpu_info|[node.GpuInfo](#schemanode.gpuinfo)|false|none||none|
|gpu_price|number|false|none||none|
|gpu_price_id|string|false|none||none|
|gpu_price_version_id|integer|false|none||none|
|memory_price|number|false|none||none|
|memory_price_id|string|false|none||none|
|memory_price_version_id|integer|false|none||none|
|memory_size_gib|number|false|none||none|
|quota_id|string|false|none||none|
|total_price_per_hour|number|false|none||none|

<h2 id="tocS_resource_price.LcgResourceSpecPriceConfirmationReq">resource_price.LcgResourceSpecPriceConfirmationReq</h2>

<a id="schemaresource_price.lcgresourcespecpriceconfirmationreq"></a>
<a id="schema_resource_price.LcgResourceSpecPriceConfirmationReq"></a>
<a id="tocSresource_price.lcgresourcespecpriceconfirmationreq"></a>
<a id="tocsresource_price.lcgresourcespecpriceconfirmationreq"></a>

```json
{
  "cpu_count": 0,
  "cpu_type": "string",
  "gpu_count": 0,
  "gpu_type": "string",
  "logic_compute_group_id": "string",
  "memory_size_gib": 0,
  "quota_id": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|cpu_count|number|false|none||none|
|cpu_type|string|false|none||none|
|gpu_count|number|false|none||none|
|gpu_type|string|false|none||none|
|logic_compute_group_id|string|false|none||none|
|memory_size_gib|number|false|none||none|
|quota_id|string|false|none||none|

<h2 id="tocS_train.ConfigMode">train.ConfigMode</h2>

<a id="schematrain.configmode"></a>
<a id="schema_train.ConfigMode"></a>
<a id="tocStrain.configmode"></a>
<a id="tocstrain.configmode"></a>

```json
0

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|integer|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|*anonymous*|0|
|*anonymous*|1|

<h2 id="tocS_train.DatasetInfo">train.DatasetInfo</h2>

<a id="schematrain.datasetinfo"></a>
<a id="schema_train.DatasetInfo"></a>
<a id="tocStrain.datasetinfo"></a>
<a id="tocstrain.datasetinfo"></a>

```json
{
  "dataset_id": "string",
  "path": "string",
  "version_id": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|dataset_id|string|false|none||none|
|path|string|false|none||none|
|version_id|string|false|none||none|

<h2 id="tocS_train.Env">train.Env</h2>

<a id="schematrain.env"></a>
<a id="schema_train.Env"></a>
<a id="tocStrain.env"></a>
<a id="tocstrain.env"></a>

```json
{
  "name": "string",
  "value": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|name|string|false|none||none|
|value|string|false|none||none|

<h2 id="tocS_train.FrameworkConfigOpenAPI">train.FrameworkConfigOpenAPI</h2>

<a id="schematrain.frameworkconfigopenapi"></a>
<a id="schema_train.FrameworkConfigOpenAPI"></a>
<a id="tocStrain.frameworkconfigopenapi"></a>
<a id="tocstrain.frameworkconfigopenapi"></a>

```json
{
  "image": "string",
  "image_type": "string",
  "instance_count": 0,
  "shm_gi": 0,
  "spec_id": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|image|string|false|none||镜像地址|
|image_type|string|false|none||镜像类型|
|instance_count|integer|false|none||实例数量|
|shm_gi|number|false|none||共享内存 单位Gi|
|spec_id|string|false|none||资源规格 ID|

<h2 id="tocS_train.FrameworkConfigStandard">train.FrameworkConfigStandard</h2>

<a id="schematrain.frameworkconfigstandard"></a>
<a id="schema_train.FrameworkConfigStandard"></a>
<a id="tocStrain.frameworkconfigstandard"></a>
<a id="tocstrain.frameworkconfigstandard"></a>

```json
{
  "cpu": 0,
  "gpu_count": 0,
  "image": "string",
  "image_type": "string",
  "instance_count": 0,
  "instance_spec_price_info": {
    "cpu_count": 0,
    "cpu_info": {
      "brand": "string",
      "cpu_product_simple": "string",
      "cpu_type": "string"
    },
    "cpu_price": 0,
    "cpu_price_id": "string",
    "cpu_price_version_id": 0,
    "gpu_count": 0,
    "gpu_info": {
      "brand": "string",
      "brand_name": "string",
      "gpu_memory_size_gb": 0,
      "gpu_product_simple": "string",
      "gpu_type": "string",
      "gpu_type_display": "string",
      "price": "string"
    },
    "gpu_price": 0,
    "gpu_price_id": "string",
    "gpu_price_version_id": 0,
    "memory_price": 0,
    "memory_price_id": "string",
    "memory_price_version_id": 0,
    "memory_size_gib": 0,
    "quota_id": "string",
    "total_price_per_hour": 0
  },
  "mem_gi": 0,
  "predef_id": "string",
  "replicas_type": 0,
  "resource_spec_price": {
    "cpu_count": 0,
    "cpu_type": "string",
    "gpu_count": 0,
    "gpu_type": "string",
    "logic_compute_group_id": "string",
    "memory_size_gib": 0,
    "quota_id": "string"
  },
  "shm_gi": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|cpu|number|false|none||none|
|gpu_count|integer|false|none||gpu卡数|
|image|string|false|none||none|
|image_type|string|false|none||镜像类型|
|instance_count|integer|false|none||none|
|instance_spec_price_info|[resource_price.InstanceSpecPriceInfo](#schemaresource_price.instancespecpriceinfo)|false|none||响应时返回价格信息|
|mem_gi|number|false|none||内存 单位Gi|
|predef_id|string|false|none||预设资源规格之 ID|
|replicas_type|[train.ReplicasType](#schematrain.replicastype)|false|none||ReplicasType|
|resource_spec_price|[resource_price.LcgResourceSpecPriceConfirmationReq](#schemaresource_price.lcgresourcespecpriceconfirmationreq)|false|none||none|
|shm_gi|number|false|none||共享内存 单位Gi|

<h2 id="tocS_train.NodeInfo">train.NodeInfo</h2>

<a id="schematrain.nodeinfo"></a>
<a id="schema_train.NodeInfo"></a>
<a id="tocStrain.nodeinfo"></a>
<a id="tocstrain.nodeinfo"></a>

```json
{
  "node_name": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|node_name|string|false|none||none|

<h2 id="tocS_train.ReplicasType">train.ReplicasType</h2>

<a id="schematrain.replicastype"></a>
<a id="schema_train.ReplicasType"></a>
<a id="tocStrain.replicastype"></a>
<a id="tocstrain.replicastype"></a>

```json
0

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|integer|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|*anonymous*|0|
|*anonymous*|1|

<h2 id="tocS_train.Timeline">train.Timeline</h2>

<a id="schematrain.timeline"></a>
<a id="schema_train.Timeline"></a>
<a id="tocStrain.timeline"></a>
<a id="tocstrain.timeline"></a>

```json
{
  "created": "string",
  "finished": "string",
  "resource_prepared": "string",
  "run": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|created|string|false|none||各阶段的结束时间，如果没开始，那么字段则不存在，时间戳 毫秒级<br />创建完成时间|
|finished|string|false|none||结束时间|
|resource_prepared|string|false|none||资源准备好的时间|
|run|string|false|none||开始运行的时间|

<h2 id="tocS_user.ExtraInfo">user.ExtraInfo</h2>

<a id="schemauser.extrainfo"></a>
<a id="schema_user.ExtraInfo"></a>
<a id="tocSuser.extrainfo"></a>
<a id="tocsuser.extrainfo"></a>

```json
{
  "institution_id": "string",
  "login_name": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|institution_id|string|false|none||none|
|login_name|string|false|none||none|

<h2 id="tocS_user.GlobalRole">user.GlobalRole</h2>

<a id="schemauser.globalrole"></a>
<a id="schema_user.GlobalRole"></a>
<a id="tocSuser.globalrole"></a>
<a id="tocsuser.globalrole"></a>

```json
0

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|integer|false|none||none|

#### 枚举值

|属性|值|
|---|---|
|*anonymous*|0|
|*anonymous*|1|
|*anonymous*|2|

<h2 id="tocS_user.UserBase">user.UserBase</h2>

<a id="schemauser.userbase"></a>
<a id="schema_user.UserBase"></a>
<a id="tocSuser.userbase"></a>
<a id="tocsuser.userbase"></a>

```json
{
  "avatar_url": "string",
  "created_at": "string",
  "email": "string",
  "extra_info": {
    "institution_id": "string",
    "login_name": "string"
  },
  "global_role": 0,
  "id": "string",
  "name": "string",
  "name_en": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|avatar_url|string|false|none||none|
|created_at|string|false|none||none|
|email|string|false|none||none|
|extra_info|[user.ExtraInfo](#schemauser.extrainfo)|false|none||none|
|global_role|[user.GlobalRole](#schemauser.globalrole)|false|none||none|
|id|string|false|none||none|
|name|string|false|none||none|
|name_en|string|false|none||none|

