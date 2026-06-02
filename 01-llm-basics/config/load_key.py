# config/load_key.py
import os
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """
    显式加载项目根目录的 .env
    不管从哪里启动（终端 / VS Code / Docker）
    """
    # 当前文件路径
    current = Path(__file__).resolve()
    # 项目根目录（根据你的目录结构调整）
    root = current.parent.parent  # 01-llm-basics -> ai-agent-learning
    env_path = root / ".env"

    if not env_path.exists():
        raise FileNotFoundError(f".env not found at {env_path}")

    load_dotenv(dotenv_path=env_path)

def get_key(env_var: str = "DASHSCOPE_API_KEY") -> str:
    load_env()
    key = os.getenv(env_var)
    if not key:
        raise RuntimeError(f"{env_var} is not set")
    return key