from openai import OpenAI
import os
from config.load_key import get_key

os.environ["DASHSCOPE_API_KEY"] = get_key()

# ---------- 1. 客户端 ----------
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ---------- 2. messages（这节课的灵魂） ----------
SYSTEM_MSG = {
    "role": "system",
    "content":("你是高级应用工程专家助手。"
        "回答要简洁、结构化；如果不确定就说不确定，不要编造。"
    ),
}

USER_MSG = {
    "role": "user",
    "content": "用 3 句话以内解释：LLM 的 token 是什么？",
}

messages = [SYSTEM_MSG, USER_MSG]

# # ---------- 3. 调用接口 ----------
# response = client.chat.completions.create(
#     model="qwen-turbo",
#     messages=messages,
#     temperature=0.2,
#     max_tokens=256,
# )

# # ---------- 4. 看看结果 ----------
# print(response.choices[0].message.content)

# --- 多轮实验（理解 messages 是个"增长数组"）---
messages_multi = [
    {"role": "system", "content": "你是个简洁的Python导师。"},
    {"role": "user", "content": "什么是 list comprehension？"},
]

r1 = client.chat.completions.create(
    model="qwen-turbo", 
    messages=messages_multi
)
a1 = r1.choices[0].message.content
print("A1:", a1)

# 把 assistant 的回复压回 messages
messages_multi.append(r1.choices[0].message)  # ← 关键：类型是 assistant message
messages_multi.append({"role": "user", "content": "写个例子，遍历 1..5 平方"})

r2 = client.chat.completions.create(model="qwen-turbo", messages=messages_multi)
print("A2:", r2.choices[0].message.content)