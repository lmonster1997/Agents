# 01-llm-basics/02_stream_httpx.py
"""
Day3 — 手写 httpx SSE（修正：真正逐字流式）
"""

import os
import json
import httpx
from config.load_key import get_key

API_KEY = get_key()
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-turbo"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "text/event-stream",  # ✅ 关键：告诉服务器要 SSE
}

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "你是一个简洁的助手。"},
        {"role": "user", "content": "用 3 句话解释 SSE 是什么？"},
    ],
    "stream": True,
    "temperature": 0.7,  # ✅ 提高一点，更容易触发分块
    "max_tokens": 300,
}

print(">> 开始流式输出...\n")

with httpx.Client(timeout=60) as client:
    with client.stream(
        "POST",
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
    ) as response:
        response.raise_for_status()
        
        buffer = ""
        for chunk in response.iter_text():  # ✅ iter_text 而不是 iter_lines
            buffer += chunk
            
            # 按行分割（SSE 用 \n\n 分隔事件）
            while "\n\n" in buffer:
                event, buffer = buffer.split("\n\n", 1)
                
                for line in event.split("\n"):
                    if line.startswith("data: "):
                        data_str = line[6:]
                        
                        if data_str.strip() == "[DONE]":
                            print("\n\n[流式结束]")
                            break
                        
                        try:
                            data = json.loads(data_str)
                        except json.JSONDecodeError:
                            continue
                        
                        choices = data.get("choices", [])
                        if not choices:
                            continue
                        
                        delta = choices[0].get("delta", {})
                        content = delta.get("content")
                        if content:
                            print(content, end="", flush=True)