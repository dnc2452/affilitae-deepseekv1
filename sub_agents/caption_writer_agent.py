#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caption Writer Sub-Agent - Chuyên tạo và tối ưu caption
"""

import logging
import random
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class CaptionWriterSubAgent:
    """
    Sub-agent chuyên viết caption
    - Tạo caption cho TikTok, Facebook
    - Tối ưu caption theo platform
    - Kiểm tra compliance
    - Tạo hashtags
    """
    
    def __init__(self, mcp):
        self.mcp = mcp
        self.name = "CaptionWriterSubAgent"
        self.capabilities = [
            'generate_caption',
            'optimize_caption',
            'check_compliance',
            'generate_hashtags'
        ]
        logger.info(f"✅ {self.name} initialized")
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi task viết caption"""
        logger.info(f"✍️ {self.name} executing: {task.get('type')}")
        
        task_type = task.get('type')
        
        if task_type == 'generate_caption':
            return await self._generate_caption(task)
        elif task_type == 'optimize_caption':
            return await self._optimize_caption(task)
        elif task_type == 'check_compliance':
            return await self._check_compliance(task)
        elif task_type == 'generate_hashtags':
            return await self._generate_hashtags(task)
        else:
            return {
                'status': 'error',
                'message': f'Unknown task type: {task_type}'
            }
    
    async def _generate_caption(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo caption cho sản phẩm"""
        product_name = task.get('product_name', 'Sản phẩm')
        price = task.get('price', 'Liên hệ')
        platform = task.get('platform', 'tiktok')
        category = task.get('category', 'general')
        
        logger.info(f"📝 Generating caption for: {product_name} on {platform}")
        
        # Mẫu caption cho TikTok
        tiktok_templates = [
            f"🔥 {product_name} - chỉ {price}!\n💯 Chất lượng đỉnh cao\n#fyp #shopping #deals #trending",
            f"💰 Săn deal {product_name} giá tốt nhất!\n📦 Free ship toàn quốc\n#sale #foryou #musthave",
            f"⚡ {product_name} - xu hướng mới!\n🛍️ Mua ngay kẻo hết\n#viral #shopping #review",
            f"🎯 {product_name} giá sốc chỉ {price}\n✅ 100% chính hãng\n#fyp #deals #shopping",
            f"💥 Bất ngờ với {product_name}!\n✨ Siêu phẩm công nghệ\n#review #tech #foryou"
        ]
        
        # Mẫu caption cho Facebook
        facebook_templates = [
            f"🛍️ **{product_name}** - Sản phẩm hot nhất hiện nay!\n\n✅ Chất lượng vượt trội\n💯 Giá: {price}\n📦 Giao hàng nhanh chóng\n\n👇 Link mua hàng trong comment!",
            f"🌟 **{product_name}** - Bạn đã thử chưa?\n\n💎 Thiết kế hiện đại, sang trọng\n💰 Giá cực kỳ hợp lý: {price}\n🎁 Quà tặng hấp dẫn kèm theo\n\n🔗 Click link comment để đặt hàng!",
            f"🔥 **SIÊU PHẨM {product_name.upper()}** 🔥\n\n📌 Chỉ với {price}\n💪 Đáp ứng mọi nhu cầu\n⭐ 5 sao từ hàng ngàn khách hàng\n\n👇 Link mua hàng bên dưới!"
        ]
        
        # Chọn caption phù hợp với platform
        if platform == 'tiktok':
            captions = tiktok_templates
        elif platform == 'facebook':
            captions = facebook_templates
        else:
            captions = tiktok_templates + facebook_templates
        
        # Lưu vào MCP
        self.mcp.save_to_memory(f'captions_{product_name}', captions)
        
        return {
            'status': 'success',
            'captions': captions,
            'count': len(captions),
            'platform': platform,
            'product': product_name
        }
    
    async def _optimize_caption(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Tối ưu caption cho platform"""
        caption = task.get('caption', '')
        platform = task.get('platform', 'tiktok')
        
        logger.info(f"🔧 Optimizing caption for {platform}")
        
        if platform == 'tiktok':
            # TikTok: max 150 ký tự, thêm hashtags
            if len(caption) > 150:
                caption = caption[:147] + '...'
            if not any(h in caption for h in ['#fyp', '#foryou']):
                caption += ' #fyp #foryou #trending'
        elif platform == 'facebook':
            # Facebook: thêm emoji và formatting
            if not any(e in caption for e in ['🌟', '🔥', '💯']):
                caption = '🔥 ' + caption
            caption += '\n\n👇 Click link comment để mua ngay!'
        
        return {
            'status': 'success',
            'original': task.get('caption', ''),
            'optimized': caption,
            'platform': platform
        }
    
    async def _check_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Kiểm tra caption có vi phạm chính sách không"""
        caption = task.get('caption', '').lower()
        platform = task.get('platform', 'tiktok')
        
        logger.info(f"🔍 Checking compliance for {platform}")
        
        banned_words = {
            'tiktok': ['earn money', 'get rich', 'guarantee', 'scam', 'spam', 'click link', 'buy now'],
            'facebook': ['guaranteed', 'click here', 'act fast', 'limited time', 'scam']
        }
        
        violations = []
        words_to_check = banned_words.get(platform, [])
        
        for word in words_to_check:
            if word in caption:
                violations.append(word)
        
        return {
            'status': 'success',
            'compliant': len(violations) == 0,
            'violations': violations,
            'confidence': 95 if len(violations) == 0 else 70,
            'platform': platform
        }
    
    async def _generate_hashtags(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo hashtags theo category"""
        category = task.get('category', 'general')
        count = task.get('count', 10)
        
        logger.info(f"🏷️ Generating hashtags for: {category}")
        
        hashtags_by_category = {
            'electronics': ['#tech', '#gadgets', '#electronics', '#smartphone', '#laptop', '#accessories', '#review', '#unboxing', '#techreview', '#newtech'],
            'fashion': ['#fashion', '#style', '#outfit', '#fashionista', '#trendy', '#ootd', '#shopping', '#fashionstyle', '#streetwear', '#luxury'],
            'home': ['#homedecor', '#interior', '#home', '#lifestyle', '#furniture', '#decor', '#homedesign', '#livingroom', '#bedroom', '#hometour'],
            'beauty': ['#beauty', '#skincare', '#makeup', '#cosmetics', '#glowup', '#selfcare', '#beautytips', '#skincareroutine', '#makeuptutorial', '#beautyhack'],
            'general': ['#shopping', '#deals', '#trending', '#viral', '#foryou', '#fyp', '#musthave', '#review', '#product', '#sale']
        }
        
        hashtags = hashtags_by_category.get(category, hashtags_by_category['general'])
        
        # Chọn ngẫu nhiên count hashtags
        selected = random.sample(hashtags, min(count, len(hashtags)))
        
        return {
            'status': 'success',
            'hashtags': selected,
            'count': len(selected),
            'category': category,
            'hashtags_string': ' '.join(selected)
        }