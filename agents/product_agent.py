#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Discovery Agent - MOCK DATA ONLY (No real API calls)
"""

import logging
import pandas as pd
import os
import random

logger = logging.getLogger(__name__)

class ProductDiscoveryAgent:
    """AI Agent tìm sản phẩm hot - Chỉ dùng mock data"""
    
    def __init__(self):
        self.criteria = {
            'min_commission_rate': 15.0,
            'min_sales': 500,
            'min_rating': 4.5,
        }
        logger.info("ProductDiscoveryAgent initialized (MOCK ONLY)")
    
    async def scan_trending_products(self, limit: int = 20):
        """Trả về mock data - KHÔNG gọi API thật"""
        logger.info(f"Generating {limit} mock products...")
        
        # Tạo sản phẩm với commission_rate đạt tiêu chí
        mock_products = []
        for i in range(limit):
            # Đảm bảo commission_rate luôn >= 15%
            commission_rate = random.uniform(16, 30)
            mock_products.append({
                'item_id': str(random.randint(100000, 999999)),
                'shop_id': str(random.randint(1000, 9999)),
                'product_name': f'Product {i+1}',
                'price': random.randint(100000, 5000000),
                'commission_rate': round(commission_rate, 1),
                'sales_count': random.randint(500, 5000),
                'rating': round(random.uniform(4.0, 5.0), 1),
                'category': 'Electronics',
                'image': 'https://via.placeholder.com/300',
                'url': 'https://shopee.vn/product',
                'discount': random.randint(5, 20)
            })
        
        logger.info(f"Generated {len(mock_products)} mock products")
        return mock_products
    
    def _passes_criteria(self, product):
        """Check if product meets criteria"""
        return (
            product.get('commission_rate', 0) >= self.criteria['min_commission_rate'] and
            product.get('sales_count', 0) >= self.criteria['min_sales'] and
            product.get('rating', 0) >= self.criteria['min_rating']
        )
    
    async def generate_affiliate_links(self, products):
        """Generate affiliate links - MOCK"""
        logger.info(f"Generating affiliate links for {len(products)} products...")
        for product in products:
            product['affiliate_link'] = f"https://shopee.vn/product/{product['shop_id']}/{product['item_id']}"
        return products
    
    def export_to_excel(self, products, filename='affiliate_products.xlsx'):
        """Export to Excel"""
        if not products:
            logger.warning("No products to export")
            return None
        
        data = []
        for p in products:
            data.append({
                'Product Name': p.get('product_name', ''),
                'Price': p.get('price', 0),
                'Commission %': p.get('commission_rate', 0),
                'Sales': p.get('sales_count', 0),
                'Rating': p.get('rating', 0),
                'Category': p.get('category', ''),
                'Affiliate Link': p.get('affiliate_link', ''),
                'Discount': p.get('discount', 0)
            })
        
        df = pd.DataFrame(data)
        os.makedirs('./data/reports', exist_ok=True)
        filepath = f"./data/reports/{filename}"
        df.to_excel(filepath, index=False)
        logger.info(f"Exported to: {filepath}")
        return filepath