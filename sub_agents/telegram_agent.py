#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Sub-Agent - Điều khiển và phân phối nội dung qua Telegram
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class TelegramSubAgent:
    """Sub-agent chuyên xử lý tương tác với Telegram"""
    
    def __init__(self, mcp):
        self.mcp = mcp
        self.name = "TelegramSubAgent"
        self.is_running = False
        self.admin_ids = []
        self.bot_token = None
        
        try:
            from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_IDS
            self.bot_token = TELEGRAM_BOT_TOKEN
            if TELEGRAM_ADMIN_IDS:
                self.admin_ids = [int(x.strip()) for x in TELEGRAM_ADMIN_IDS.split(',') if x.strip()]
        except:
            self.admin_ids = []
            logger.warning("⚠️ Telegram config not found, using mock mode")
        
        logger.info(f"✅ {self.name} initialized (Mock mode)")
        logger.info(f"   Admin IDs: {self.admin_ids}")
    
    async def start_bot(self):
        logger.info("🤖 Telegram Bot starting (MOCK MODE)")
        self.is_running = True
        return True
    
    async def stop_bot(self):
        logger.info("🛑 Telegram Bot stopping (MOCK MODE)")
        self.is_running = False
        return True
    
    def _is_admin(self, user_id: int) -> bool:
        return user_id in self.admin_ids
    
    async def send_message(self, chat_id: Optional[str] = None, text: str = "", keyboard: Optional[Any] = None, photo_path: Optional[str] = None, video_path: Optional[str] = None):
        logger.info(f"📤 [MOCK] Sending message: {text[:100]}...")
        return {'status': 'success', 'mock': True}
    
    async def send_daily_deals(self, deals: List[Dict]):
        logger.info(f"📤 [MOCK] Sending {len(deals)} daily deals")
        return {'status': 'success', 'mock': True, 'count': len(deals)}
    
    async def send_analytics_report(self, report: Dict):
        logger.info(f"📤 [MOCK] Sending analytics report")
        return {'status': 'success', 'mock': True, 'report': report}