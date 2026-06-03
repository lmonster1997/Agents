# Day1
## API Key 管理原则（学习期 vs 企业级）

### 铁律
1. Key 永不进 Git（.env / key.json / *.pem 全部 gitignore）
2. Key 永不拼进 URL / 永不全文日志（只允许打 mask 前缀用于调试）
3. 学习期：env var / .env（本地）+ docker --env-file（部署）
4. 企业级：Secret 由 Secret Manager（KMS/Secrets Manager）托管 → 运行时通过最小权限身份拉取 → 只存在于内存配置
5. 可轮换：secret 设计要有版本/可刷新，不能硬编码单点绑死

### 我用到的变量
- DASHSCOPE_API_KEY
- （未来）LLM_MODEL / BASE_URL / RATE_LIMIT_*

# Day2

### 知识点
1. LLM 无状态——对话历史靠维护 messages 数组
2. system role 用来锚定行为边界（"简洁、不编造"）
3. finish_reason=stop 表示正常结束；如果是 length 说明撞了 max_tokens
4. token 用量 = 成本意识起点（prompt_tokens + completion_tokens）

## Token 认知
- prompt_tokens = 输入（可控性高）
- completion_tokens = 输出（可控性低）
- 成本 = prompt × 便宜 + completion × 贵

# Day3

"SSE = 长连接 + data:帧；DashScope 粒度到句/半句级；工程上用 SDK stream=True 就够，手写 httpx 只为了确认协议本质"

## Day4 — 裸 Tool Call Loop

### 核心认知
- Agent = while 循环 + messages 状态
- tool_calls 只是模型输出的结构化 JSON
- tool 消息必须带 tool_call_id，才能和 assistant 消息对应

### 代码骨架（记住这个）
1. 定义 tools（函数 + schema）
2. messages = [system, user]
3. while True:
   - 调模型（带 tools）
   - 有 tool_calls → 执行 → append tool 消息
   - 无 tool_calls → 输出答案 → break

### 面试一句话
“Agent 的 tool calling 本质是一个循环：
模型输出结构化调用请求 → 系统执行 → 结果塞回上下文 → 模型继续推理。”