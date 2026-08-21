# api/index.py
import os
import json
from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import sys
from pathlib import Path

# Thêm đường dẫn gốc vào sys.path để import được các module khác
sys.path.append(str(Path(__file__).parent.parent))

from orchestrator import AffiliateAgentOrchestrator
from config.settings import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict = None

async def send_telegram_message(chat_id: int, text: str):
    import httpx
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})

@app.post("/webhook")
async def telegram_webhook(update: dict):
    logger.info(f"Received update: {update.get('update_id')}")
    try:
        message = update.get('message', {})
        if not message:
            return {"status": "ignored"}
        
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        
        if 'shopee.vn' in text or 'shopee' in text:
            logger.info(f"Received product link from {chat_id}: {text}")
            await send_telegram_message(chat_id, "🔍 Đang xử lý link sản phẩm của bạn...")
            
            # TODO: Gọi orchestrator xử lý link
            # orchestrator = AffiliateAgentOrchestrator()
            # await orchestrator.process_manual_link(text, chat_id)
            
            return {"status": "processing"}
        elif text == '/start':
            await send_telegram_message(chat_id, "Chào mừng bạn đến với AI Affiliate Agent Bot! Gửi link Shopee để tôi xử lý.")
            return {"status": "started"}
        else:
            await send_telegram_message(chat_id, "Vui lòng gửi link sản phẩm Shopee để tôi hỗ trợ.")
            return {"status": "ignored"}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"message": "AI Affiliate Agent is running on Vercel!"}
