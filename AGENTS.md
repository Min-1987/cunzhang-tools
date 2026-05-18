# AGENTS.md - 智能体协作架构

_双智能体协作 + 自我进化 | 定义于 2026-05-19_

---

## 架构总览

```
用户输入 ──▶ Hermes（决策规划层）
                 │
                 ▼
          OpenClaw（执行守护层）
                 │
                 ▼
             输出层
```

## 双智能体协作

| 角色 | 职责 |
|------|------|
| 🧠 **Hermes** | 视觉识别、计算引擎、任务拆解、健康监控 OpenClaw |
| 🦞 **OpenClaw** | 文件操作、脚本执行、技能调用、健康监控 Hermes |

## 互保机制

- **每30秒**互相心跳检测
- 异常 → 记录到 `health/incident.md`
- 自动调用 `recovery/fix-*.ps1`
- 无法自愈 → 向村长报告

---

## ♻️ 自我进化（Self-Improving Agent）

每次纠错、报错、学到新东西，自动记录到 `.learnings/`：

| 文件 | 记录内容 | 升级目标 |
|------|----------|----------|
| `LEARNINGS.md` | 修正、洞察、知识缺口 | 通用经验 → 升级到 SOUL.md / AGENTS.md |
| `ERRORS.md` | 命令失败、集成错误 | 反复出现 → 提取为修复脚本 |
| `FEATURE_REQUESTS.md` | 村长想要但还没有的能力 | 重要需求 → 升级到 RULES.md |

---

## 目录导航

```
workspace/
├── 📄 身份层      IDENTITY.md, SOUL.md, USER.md, AGENTS.md
├── 📄 规则层      RULES.md
├── 🧠 记忆层      memory/{openclaw,hermes,shared}/
├── 📥 输入层      images/, pasted-text/, clipboard/
├── ⚙️ 处理层      ocr-results/, parsed-data/, calculations/
├── 📤 输出层      drafts/lottery/, exports/, reports/
├── 🔧 健康层      health/, recovery/
├── 🔌 技能层      skills/, scripts/, templates/
├── ♻️ 进化层      .learnings/
└── 📋 日志层      logs/
```
