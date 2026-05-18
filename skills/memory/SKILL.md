---
name: memory
description: 双智能体共享语义记忆系统。OpenClaw 和 Hermes 共享的轻量级记忆层，基于 sentence-transformers 语义嵌入 + SQLite 存储。支持 add/search/get_all 接口，用户级隔离（system/openclaw/hermes）。
---

# 共享记忆系统 (Shared Memory)

## 架构

```
memory/shared/
├── memory_wrapper.py    # 记忆引擎 API
├── shared_memory.db     # SQLite 存储文件
└── memory_wrapper.py → MCP 接口供 OpenClaw / Hermes 调用
```

- **嵌入模型**: `sentence-transformers/all-MiniLM-L6-v2` (384维)
- **向量存储**: SQLite + 余弦相似度全量检索
- **存储路径**: `{workspace}/memory/shared/`
- **用户隔离**: `user_id` 字段区分 system / openclaw / hermes

## API 参考

```python
from memory_wrapper import get_memory

mem = get_memory()

# 写入记忆
mem.add("内容文字", user_id="system", category="general")

# 语义检索 (返回 top-5)
results = mem.search("查询关键词", user_id="system")
# → [{"id": 1, "content": "...", "category": "...", "score": 0.92, ...}]

# 列出全部
all = mem.get_all(user_id="system")

# 按 ID 删除
mem.delete(mem_id=1)
```

## 初始化

```python
from memory_wrapper import get_memory
mem = get_memory()

mem.add("系统描述信息", user_id="system", category="system")
```

## 注意事项

- 首次加载需加载 sentence-transformers 模型（~100ms）
- 记忆库文件 `shared_memory.db` 已 git 追踪，推送到远程仓库
- 建议定期清理过期记忆（`get_all` → 逐条 `delete`）
- API 调用者在脚本层面直接导入，无需 HTTP / RPC 开销
