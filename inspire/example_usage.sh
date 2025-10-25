#!/bin/bash
# 使用修复后的启智训练任务创建脚本的示例

echo "=== 启智训练任务创建示例 ==="

# 现在spec-id有默认值了，使用起来更简单！

echo "1. 基础用法（使用默认的H200规格）："
python inspire_api_control.py create \
  --name 'hzz-api-training-test-fixed' \
  --start-command 'cd util-scripts && python video_check.py'

echo ""
echo "2. 查看可用规格（可选）："
python inspire_api_control.py list-specs \
  --compute-group-id "lcg-303ac8c6-aa19-4284-af03-2296592326e5"

需要探索一下各种规格的ID。

echo ""
echo "3. 使用其他规格（可选）："
python inspire_api_control.py create \
  --name 'hzz-api-training-test-custom' \
  --start-command 'cd util-scripts && python video_check.py' \
  --spec-id 'OTHER_SPEC_ID_IF_NEEDED'

echo ""
echo "=== 参数说明 ==="
echo "- spec-id: 现在默认使用H200规格 (4dd0e854-e2a4-4253-95e6-64c13f0b5117)"
echo "- 大多数情况下不需要手动指定spec-id了"
echo ""
echo "=== 其他可用命令 ==="
echo "查看任务详情: python inspire_api_control.py detail --job-id 'JOB_ID'"
echo "停止任务: python inspire_api_control.py stop --job-id 'JOB_ID'"
echo "列出节点: python inspire_api_control.py list-nodes"
echo "列出规格: python inspire_api_control.py list-specs"