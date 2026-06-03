## Day5 — Agent as a Service

### 核心认知
- Agent 应用 = FastAPI + LLM Service + Tools
- FastAPI 负责：HTTP / 校验 / 并发
- LLM Service 负责：Agent Loop / 工具调度
- 工具 = 纯 Python 函数（与框架无关）

### 工程结构
- config.py：集中管理配置（Pydantic Settings）
- schemas/：请求/响应模型（类型安全）
- services/：业务逻辑（Agent Loop）
- tools/：工具实现（可独立测试）

### 面试一句话
“我把 Agent 实现为一个无状态 HTTP 服务，
通过 FastAPI 对外暴露接口，内部用 Tool Call Loop 调度外部能力。”