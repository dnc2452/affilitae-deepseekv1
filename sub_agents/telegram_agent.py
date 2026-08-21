#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Sub-Agent - Điều khiển và phân phối nội dung qua Telegram
"""

import os
import logging
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# ============================================================
# DANH SÁCH LỆNH CHO BOT
# ============================================================
COMMANDS = {
    '/start': 'Bắt đầu bot',
    '/help': 'Hướng dẫn sử dụng',
    '/scan': 'Quét sản phẩm hot',
    '/post': 'Đăng bài lên các nền tảng',
    '/status': 'Kiểm tra trạng thái hệ thống',
    '/analytics': 'Xem báo cáo doanh thu',
    '/link': 'Chuyển link thành affiliate link'
}

class TelegramSubAgent:
    """
    Sub-agent chuyên xử lý tương tác với Telegram
    """
    
    def __init__(self, mcp, bot_token: str = None):
        self.mcp = mcp
        self.name = "TelegramSubAgent"
        
        # Đọc token từ tham số hoặc từ biến môi trường
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "8927455608:AAHd_w4JF2KUFYMmTMi5Ir-RVMv6quHndh0")
        self.admin_ids = []  # Sẽ được set từ .env
        self.is_running = False
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.last_update_id = 0
        
        logger.info(f"✅ {self.name} initialized")
        logger.info(f"   🤖 Bot token: {self.bot_token[:10]}...")
    
    async def start_bot(self):
        """Khởi động Telegram Bot và bắt đầu lắng nghe lệnh"""
        logger.info("🤖 Starting Telegram Bot...")
        
        # Kiểm tra bot hoạt động
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/getMe")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        logger.info(f"✅ Bot online: @{data['result']['username']}")
                        self.is_running = True
                        
                        # Đăng ký các lệnh cho bot
                        await self._set_commands()
                    else:
                        logger.error(f"❌ Bot error: {data}")
                        return False
                else:
                    logger.error(f"❌ HTTP error: {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"❌ Bot start error: {e}")
            return False
        
        # Bắt đầu polling để nhận tin nhắn
        if self.is_running:
            await self._poll_updates()
        
        return self.is_running
    
    async def _set_commands(self):
        """Đăng ký danh sách lệnh cho bot"""
        commands_list = [{"command": cmd[1:], "description": desc} 
                         for cmd, desc in COMMANDS.items()]
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/setMyCommands",
                    json={"commands": commands_list}
                )
                if response.status_code == 200:
                    logger.info(f"✅ Registered {len(commands_list)} commands")
        except Exception as e:
            logger.error(f"❌ Set commands error: {e}")
    
    async def _poll_updates(self):
        """Lắng nghe tin nhắn từ người dùng"""
        logger.info("👂 Listening for updates...")
        
        while self.is_running:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(
                        f"{self.base_url}/getUpdates",
                        params={
                            "offset": self.last_update_id + 1,
                            "timeout": 30,
                            "allowed_updates": ["message"]
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('ok'):
                            for update in data.get('result', []):
                                self.last_update_id = update.get('update_id', 0)
                                await self._handle_update(update)
            except Exception as e:
                logger.debug(f"Polling error: {e}")
                import asyncio
                await asyncio.sleep(1)
    
    async def _handle_update(self, update: Dict):
        """Xử lý từng tin nhắn nhận được"""
        message = update.get('message')
        if not message:
            return
        
        chat_id = message.get('chat', {}).get('id')
        user_id = message.get('from', {}).get('id')
        text = message.get('text', '').strip()
        
        # Kiểm tra nếu là lệnh
        if text.startswith('/'):
            await self._handle_command(chat_id, user_id, text)
        else:
            # Xử lý tin nhắn thường
            await self._handle_text_message(chat_id, user_id, text)
    
    async def _handle_command(self, chat_id: int, user_id: int, text: str):
        """Xử lý các lệnh từ người dùng"""
        
        # Kiểm tra admin (trừ /start và /help)
        is_admin = str(user_id) in self.admin_ids
        if not is_admin and text not in ['/start', '/help']:
            await self._send_message(chat_id, "❌ Bạn không có quyền sử dụng lệnh này.")
            return
        
        # Xử lý từng lệnh
        if text == '/start':
            await self._cmd_start(chat_id)
        elif text == '/help':
            await self._cmd_help(chat_id)
        elif text == '/scan':
            await self._cmd_scan(chat_id)
        elif text == '/post':
            await self._cmd_post(chat_id)
        elif text == '/status':
            await self._cmd_status(chat_id)
        elif text == '/analytics':
            await self._cmd_analytics(chat_id)
        elif text == '/link':
            await self._cmd_link(chat_id)
        else:
            await self._send_message(chat_id, f"❌ Không hiểu lệnh: {text}\nGửi /help để xem danh sách lệnh.")
    
    # ============================================================
    # CÁC HÀM XỬ LÝ LỆNH
    # ============================================================
    
    async def _cmd_start(self, chat_id: int):
        """Xử lý lệnh /start"""
        msg = """
🤖 **Chào mừng bạn đến với Dncagentbot!**

Tôi là trợ lý tiếp thị liên kết tự động.

📌 **Các lệnh có sẵn:**
• /help - Hiển thị hướng dẫn
• /scan - Quét sản phẩm hot
• /post - Đăng bài lên các nền tảng
• /status - Kiểm tra trạng thái hệ thống
• /analytics - Xem báo cáo doanh thu
• /link - Chuyển link thành affiliate link

💡 **Nhanh hơn:** Gửi trực tiếp link Shopee/Lazada/TikTok vào đây, tôi sẽ tự động tạo link affiliate cho bạn!
"""
        await self._send_message(chat_id, msg)
    
    async def _cmd_help(self, chat_id: int):
        """Xử lý lệnh /help"""
        msg = """
📖 **HƯỚNG DẪN SỬ DỤNG**

🔹 **Chuyển đổi link nhanh:**
Gửi link sản phẩm Shopee/Lazada/TikTok, bot sẽ tự động:
• Cào ảnh sản phẩm
• Tạo link affiliate
• Viết caption bán hàng
• Trả về kết quả đẹp mắt

🔹 **Quét sản phẩm hot:**
/scan - Quét sản phẩm hot từ Shopee

🔹 **Đăng bài tự động:**
/post - Đăng lên tất cả nền tảng

🔹 **Báo cáo:**
/analytics - Báo cáo doanh thu hôm nay

🔹 **Trạng thái:**
/status - Kiểm tra trạng thái hệ thống
"""
        await self._send_message(chat_id, msg)
    
    async def _cmd_scan(self, chat_id: int):
        """Xử lý lệnh /scan - Quét sản phẩm hot"""
        await self._send_message(chat_id, "🔍 Đang quét sản phẩm hot...")
        
        try:
            orchestrator = self.mcp.get_from_memory('orchestrator')
            if orchestrator:
                products = await orchestrator.phase_1_discover_products(use_browser=False)
                
                if products:
                    msg = "📊 **Danh sách sản phẩm hot:**\n\n"
                    for i, p in enumerate(products[:5], 1):
                        msg += f"{i}. **{p.get('product_name', 'N/A')}**\n"
                        msg += f"   💰 Giá: {p.get('price', 'N/A')}\n"
                        msg += f"   📈 Hoa hồng: {p.get('commission_rate', 'N/A')}%\n\n"
                    
                    await self._send_message(chat_id, msg)
                else:
                    await self._send_message(chat_id, "❌ Không tìm thấy sản phẩm nào.")
            else:
                await self._send_message(chat_id, "❌ Hệ thống chưa sẵn sàng.")
        except Exception as e:
            await self._send_message(chat_id, f"❌ Lỗi: {str(e)}")
    
    async def _cmd_post(self, chat_id: int):
        """Xử lý lệnh /post - Đăng bài tự động"""
        await self._send_message(chat_id, "📤 Đang đăng bài lên các nền tảng...")
        
        try:
            orchestrator = self.mcp.get_from_memory('orchestrator')
            if orchestrator:
                contents = self.mcp.get_from_memory('created_contents')
                if contents:
                    result = await orchestrator.phase_3_auto_posting(contents)
                    await self._send_message(chat_id, f"✅ Đã đăng {len(result)} bài thành công!")
                else:
                    await self._send_message(chat_id, "❌ Không có nội dung để đăng.")
            else:
                await self._send_message(chat_id, "❌ Hệ thống chưa sẵn sàng.")
        except Exception as e:
            await self._send_message(chat_id, f"❌ Lỗi: {str(e)}")
    
    async def _cmd_status(self, chat_id: int):
        """Xử lý lệnh /status - Kiểm tra trạng thái"""
        try:
            session = self.mcp.get_session_summary() if self.mcp else {}
            products = self.mcp.get_from_memory('discovered_products') if self.mcp else []
            contents = self.mcp.get_from_memory('created_contents') if self.mcp else []
            posts = self.mcp.get_from_memory('posted_items') if self.mcp else []
            
            msg = f"""
📊 **TRẠNG THÁI HỆ THỐNG**

🟢 **Bot:** Đang hoạt động
📅 **Session:** {session.get('session_id', 'N/A')}
📦 **Sản phẩm:** {len(products) if products else 0}
🎬 **Nội dung:** {len(contents) if contents else 0}
📤 **Bài đã đăng:** {len(posts) if posts else 0}

⏰ **Cập nhật:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            await self._send_message(chat_id, msg)
        except Exception as e:
            await self._send_message(chat_id, f"❌ Lỗi: {str(e)}")
    
    async def _cmd_analytics(self, chat_id: int):
        """Xử lý lệnh /analytics - Báo cáo doanh thu"""
        await self._send_message(chat_id, "📈 Đang tổng hợp báo cáo...")
        
        # Mock báo cáo (thực tế sẽ lấy từ database)
        msg = """
📈 **BÁO CÁO DOANH THU HÔM NAY**

📊 **Tổng quan:**
• Lượt xem: 1,234
• Click: 56
• Đơn hàng: 12
• Doanh thu: 6,500,000 VND
• Hoa hồng: 975,000 VND

🏆 **Top sản phẩm:**
1. iPhone 15 Pro - 12 đơn
2. Tai nghe Sony - 8 đơn
3. Đồng hồ thông minh - 5 đơn
"""
        await self._send_message(chat_id, msg)
    
    async def _cmd_link(self, chat_id: int):
        """Xử lý lệnh /link - Hướng dẫn chuyển link"""
        msg = """
🔗 **CHUYỂN ĐỔI LINK AFFILIATE**

📌 **Cách sử dụng:**
Gửi trực tiếp link sản phẩm từ:
• Shopee: https://shopee.vn/...
• Lazada: https://lazada.vn/...
• TikTok: https://tiktok.com/...

Bot sẽ tự động:
1️⃣ Cào thông tin sản phẩm
2️⃣ Tạo link affiliate
3️⃣ Viết caption hấp dẫn
4️⃣ Trả về kết quả

💡 **Ví dụ:** Gửi link Shopee, bot sẽ trả về link affiliate kèm caption.
"""
        await self._send_message(chat_id, msg)
    
    async def _handle_text_message(self, chat_id: int, user_id: int, text: str):
        """Xử lý tin nhắn thường (không phải lệnh)"""
        # Kiểm tra nếu là link Shopee/Lazada/TikTok
        if self._is_affiliate_link(text):
            await self._send_message(chat_id, "🔗 Đang xử lý link...")
            
            # TODO: Gọi orchestrator để xử lý link thành affiliate
            result = await self._process_affiliate_link(text)
            await self._send_message(chat_id, result)
        else:
            await self._send_message(chat_id, 
                "👋 Chào bạn! Tôi là Dncagentbot.\n"
                "Gửi link sản phẩm Shopee/Lazada/TikTok để tôi tạo link affiliate.\n"
                "Gửi /help để xem hướng dẫn chi tiết."
            )
    
    def _is_affiliate_link(self, text: str) -> bool:
        """Kiểm tra link có phải Shopee/Lazada/TikTok không"""
        domains = ['shopee.vn', 'shopee.com', 'lazada.vn', 'lazada.com', 'tiktok.com']
        return any(domain in text.lower() for domain in domains)
    
    async def _process_affiliate_link(self, link: str) -> str:
        """Xử lý link thành affiliate link (Mock)"""
        # TODO: Tích hợp thật với Shopee/Lazada API
        return f"""
🔗 **Link Affiliate đã tạo!**

🛒 Sản phẩm: [Tên sản phẩm từ link]
💰 Giá gốc: X,XXX,XXX VND
💵 Giá sau giảm: X,XXX,XXX VND
📈 Hoa hồng: 18.5%

🔗 Link: {link}

💡 Nhấn vào link để mua ngay!
"""
    
    async def _send_message(self, chat_id: int, text: str):
        """Gửi tin nhắn từ bot đến người dùng"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": "Markdown"
                    }
                )
                if response.status_code != 200:
                    logger.error(f"Send message error: {response.text}")
        except Exception as e:
            logger.error(f"Send message exception: {e}")
    
    async def send_message_to_admin(self, text: str):
        """Gửi tin nhắn đến Admin"""
        for admin_id in self.admin_ids:
            await self._send_message(int(admin_id), text)
    
    async def stop_bot(self):
        """Dừng bot"""
        self.is_running = False
        logger.info("🛑 Telegram Bot stopped")