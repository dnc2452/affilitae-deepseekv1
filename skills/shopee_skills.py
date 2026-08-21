#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Skills - Kỹ năng tương tác với Shopee (Mock Data)
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ShopeeSkills:
    """Shopee-related skills cho agents"""
    
    def __init__(self):
        logger.info("ShopeeSkills loaded")
    
    async def search_products_by_keyword(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Search products by keyword - MOCK DATA"""
        logger.info(f"Searching products: {keyword}")
        return []
    
    async def get_product_details(self, product_id: str) -> Dict:
        """Get detailed product information - MOCK"""
        return {'id': product_id, 'name': 'Sample Product'}
    
    async def get_trending_products(self, category: str = 'Electronics') -> List[Dict]:
        """Get trending products - MOCK"""
        return []
    
    async def filter_high_commission_products(self, products: List[Dict], min_commission: float = 15.0) -> List[Dict]:
        """Filter products with high commission - ĐÃ SỬA LỖI"""
        logger.info(f"Filtering products with commission >= {min_commission}%")
        filtered = []
        for p in products:
            # ⚠️ QUAN TRỌNG: Lấy commission_rate thay vì commission
            rate = p.get('commission_rate', 0)
            if rate >= min_commission:
                filtered.append(p)
        logger.info(f"✅ {len(filtered)} products passed filter")
        return filtered
    
    async def create_short_affiliate_link(self, product_id: str, shop_id: str) -> str:
        """Create short affiliate link"""
        return f"https://shopee.vn/product/{shop_id}/{product_id}?aff=1"
    
    async def get_product_conversion_rate(self, product_id: str) -> float:
        """Get estimated conversion rate - MOCK"""
        return 2.5