# app/main.py
from fastapi import FastAPI
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import LLMService

app = FastAPI(title="Agent Service")
llm = LLMService()

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    messages = [
        {"role": "system", "content": "你是严谨助手。"},
        {"role": "user", "content": req.message},
    ]
    reply = llm.chat(messages)
    return ChatResponse(reply=reply)