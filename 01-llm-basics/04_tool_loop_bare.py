def get_weather(city: str) -> str:
    """获取指定城市的天气（模拟）"""
    # 实际项目中这里可能调用真实的天气API
    return f"{city} 晴天，气温 22°C"

import os
import json
from config.load_key import get_key
from openai import OpenAI

# 初始化客户端
os.environ["DASHSCOPE_API_KEY"] = get_key()
client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 初始消息
messages = [
    {"role": "system", "content": "你是一个有用的助手，可以调用工具获取信息。"},
    {"role": "user", "content": "上海今天天气怎么样？"}
]

# 工具定义（同上）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 循环
while True:
    # 调用模型
    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # 让模型自动决定是否调用工具
    )
    
    # 获取模型返回的消息
    message = response.choices[0].message
    
    # 如果模型有工具调用请求
    if message.tool_calls:
        # 将助手消息（包含tool_calls）加入历史
        messages.append(message.model_dump(exclude_none=True))
        
        # 处理每一个工具调用
        for tool_call in message.tool_calls:
            # 解析参数
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            # 执行工具
            if function_name == "get_weather":
                city = arguments.get("city")
                result = get_weather(city)
            else:
                result = f"未知工具: {function_name}"
            
            # 将工具执行结果加入消息历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result
            })
        # 继续循环，让模型根据工具结果生成回答
        continue
    else:
        # 没有工具调用，输出最终答案并退出循环
        print("最终回答：", message.content)
        break