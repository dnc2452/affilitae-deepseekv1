#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caption Skills - Kỹ năng tạo và tối ưu caption
"""

import logging
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

class CaptionSkills:
    """Kỹ năng xử lý caption cho các nền tảng"""
    
    def __init__(self):
        logger.info("✅ CaptionSkills loaded")
    
    async def generate_tiktok_caption(self, product_name: str, price: str, commission: float) -> List[str]:
        """Tạo caption cho TikTok"""
        logger.info(f"Generating TikTok captions for {product_name}")
        
        captions = [
            f"🔥 {product_name} - Only {price}! Amazing deal #foryou #shopping #trending",
            f"💰 Best price for {product_name} right now! Link in bio #deals #viral",
            f"⚡ Don't miss this! {product_name} at {price} - Limited time! #musthave",
        ]
        return captions
    
    async def generate_facebook_caption(self, product_name: str, price: str) -> List[str]:
        """Tạo caption cho Facebook"""
        logger.info(f"Generating Facebook captions for {product_name}")
        
        captions = [
            f"🎁 Amazing {product_name} just arrived!\n✅ {price}\n💙 Great quality\n👇 Link in comments!",
            f"Don't you just love {product_name}? \n🛍️ {price}\n📦 Fast shipping\n💬 Comment for link!",
            f"Introducing {product_name}!\n💝 Special price: {price}\n🌟 5-star reviews\n👇 Get yours now!",
        ]
        return captions
    
    async def generate_hashtags(self, product_category: str) -> List[str]:
        """Tạo hashtags theo category"""
        logger.info(f"Generating hashtags for {product_category}")
        
        hashtags = {
            'Electronics': ['#tech', '#gadgets', '#shopping', '#deals', '#techreview'],
            'Fashion': ['#fashion', '#style', '#ootd', '#shopping', '#trending'],
            'Home': ['#homedecor', '#home', '#lifestyle', '#interior', '#diy'],
        }
        return hashtags.get(product_category, ['#shopping', '#deals', '#trending'])
    
    async def optimize_caption_for_platform(self, caption: str, platform: str) -> str:
        """Tối ưu caption cho từng nền tảng"""
        logger.info(f"Optimizing caption for {platform}")
        
        if platform == 'tiktok':
            optimized = caption[:150] + " #foryou #trending"
        elif platform == 'facebook':
            optimized = caption + "\n👇 Comment for link!"
        else:
            optimized = caption
        return optimized
    
    async def check_caption_compliance(self, caption: str, platform: str) -> Dict[str, Any]:
        """Kiểm tra caption có vi phạm chính sách không"""
        logger.info(f"Checking compliance for {platform}")
        
        violations = []
        banned_words = {
            'tiktok': ['earn money', 'get rich', 'buy now', 'spam'],
            'facebook': ['guaranteed', 'click here', 'act fast'],
        }
        
        caption_lower = caption.lower()
        for word in banned_words.get(platform, []):
            if word in caption_lower:
                violations.append(f"Banned word: {word}")
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations,
            'confidence': 95
        }