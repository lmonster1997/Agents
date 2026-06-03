# app/services/llm_service.py
"""
把 Day4 的裸 Tool Call Loop 封装成 Service
"""
import json
from openai import OpenAI
from app.config import settings
from app.tools import weather

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.dashscope_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定城市的天气",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                    },
                },
            }
        ]

    def chat(self, messages: list[dict]) -> str:
        """同步调用（先简单，后面再改流式）"""
        for _ in range(settings.max_tool_calls):
            resp = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
            )
            msg = resp.choices[0].message

            if msg.tool_calls:
                messages.append(msg.model_dump(exclude_none=True))
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    if tc.function.name == "get_weather":
                        result = weather.get_weather(args.get("city", ""))
                    else:
                        result = "unknown tool"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tc.function.name,
                        "content": result,
                    })
                continue
            return msg.content
        return "已达到最大工具调用次数"