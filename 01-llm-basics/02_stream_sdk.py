# 01-llm-basics/02_stream_sdk.py
"""
Day3 — SDK 流式（推荐工程写法）
"""

from config.load_key import get_key
import os
from openai import OpenAI

os.environ["DASHSCOPE_API_KEY"] = get_key()

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [
    {"role": "system", "content": "你是一个简洁的助手。"},
    {"role": "user", "content": "用 3 句话解释 SSE 是什么？"},
]

print(">> streaming...\n")

full_content = ""
for chunk in client.chat.completions.create(
    model="qwen-turbo",
    messages=messages,
    stream=True,
    temperature=0.2,
    max_tokens=300,
):
    delta = chunk.choices[0].delta
    if delta and delta.content:
        full_content += delta.content
        print(delta.content, end="", flush=True)

print("\n\n---\n")

# ✅ 关键：流式结束后的 usage（很多初学者会漏）
if hasattr(chunk, "usage") and chunk.usage:
    u = chunk.usage
    print(f"💰 Tokens | prompt={u.prompt_tokens} | completion={u.completion_tokens}")