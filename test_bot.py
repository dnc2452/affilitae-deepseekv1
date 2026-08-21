#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Telegram Bot (with real token)
"""

import asyncio
import logging
import sys
import os

# Thêm đường dẫn hiện tại vào sys.path
sys.path.insert(0, os.getcwd())

# Đọc token từ .env nếu có
from dotenv import load_dotenv
load_dotenv()

from sub_agents.telegram_agent import TelegramSubAgent
from mcp.context_protocol import ModelContextProtocol

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_bot():
    print("\n" + "="*60)
    print("🤖 AI AFFILIATE AGENT - TELEGRAM BOT (REAL)")
    print("="*60 + "\n")
    
    # Kiểm tra token từ biến môi trường hoặc dùng token mặc định
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if bot_token:
        print(f"✅ Đọc token từ .env: {bot_token[:10]}...")
    else:
        print("⚠️ Không tìm thấy token trong .env, dùng token mặc định.")
        bot_token = "8927455608:AAHd_w4JF2KUFYMmTMi5Ir-RVMv6quHndh0"
        print(f"   Token: {bot_token[:10]}...")
    
    # Khởi tạo MCP
    mcp = ModelContextProtocol()
    
    # Khởi tạo bot với token thật
    bot = TelegramSubAgent(mcp, bot_token=bot_token)
    bot.admin_ids = [os.getenv("TELEGRAM_ADMIN_IDS", "")]
    
    # Khởi động bot
    await bot.start_bot()
    
    print("\n✅ Bot đang chạy và lắng nghe tin nhắn...")
    print("📱 Mở Telegram và tìm @Dncagentbot")
    print("💬 Gửi tin nhắn /start để bắt đầu")
    print("\n🛑 Nhấn Ctrl+C để dừng bot\n")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng bot...")
        await bot.stop_bot()
        print("✅ Bot đã dừng")

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
        sys.exit(0)