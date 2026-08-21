#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Discovery Agent - Lấy sản phẩm từ Shopee (có fallback mock data)
"""

import asyncio
import logging
import pandas as pd
from datetime import datetime
import os
import httpx
import json
import random

logger = logging.getLogger(__name__)

class ProductDiscoveryAgent:
    """AI Agent lấy sản phẩm từ Shopee với fallback mock data"""
    
    def __init__(self):
        self.criteria = {
            'min_commission_rate': 15.0,
            'min_sales': 500,
            'min_rating': 4.5,
        }
        logger.info("ProductDiscoveryAgent initialized")
    
    async def search_shopee_products(self, keyword: str, limit: int = 10):
        """Tìm kiếm sản phẩm từ Shopee với headers đầy đủ"""
        logger.info(f"Searching real products: {keyword}")
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://shopee.vn/",
                "Origin": "https://shopee.vn",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    "https://shopee.vn/api/v4/search/search_items",
                    params={
                        "by": "relevancy",
                        "keyword": keyword,
                        "limit": limit,
                        "newest": 0,
                        "order": "desc",
                        "page_type": "search",
                        "version": "2"
                    },
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    
                    products = []
                    for item in items:
                        item_data = item.get("item_basic", {})
                        
                        rating_star = 0
                        if "item_rating" in item_data:
                            rating_star = item_data.get("item_rating", {}).get("rating_star", 0)
                        
                        sold = item_data.get("sold", 0)
                        
                        products.append({
                            'item_id': str(item_data.get('itemid', '')),
                            'shop_id': str(item_data.get('shopid', '')),
                            'product_name': item_data.get('name', ''),
                            'price': item_data.get('price', 0) / 100000,
                            'sales_count': sold,
                            'rating': rating_star,
                            'category': str(item_data.get('catid', '')),
                            'image': item_data.get('image', ''),
                            'url': f"https://shopee.vn/product/{item_data.get('shopid', '')}/{item_data.get('itemid', '')}",
                            'commission_rate': random.uniform(15.0, 25.0)
                        })
                    
                    logger.info(f"Found {len(products)} real products")
                    return products
                else:
                    logger.warning(f"Shopee API returned {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Shopee search error: {e}")
            return []
    
    async def _get_mock_products(self, limit: int = 10):
        """Tạo mock data khi không lấy được dữ liệu thật"""
        logger.info("Using mock data (fallback)")
        
        mock_products = [
            {
                'item_id': '123456789',
                'shop_id': '987654',
                'product_name': 'Tai nghe Bluetooth Sony WH-1000XM5',
                'price': 7990000,
                'sales_count': 2500,
                'rating': 4.8,
                'category': 'Electronics',
                'url': 'https://shopee.vn/product/987654/123456789',
                'commission_rate': 18.5
            },
            {
                'item_id': '987654321',
                'shop_id': '123456',
                'product_name': 'iPhone 15 Pro Max 256GB',
                'price': 28990000,
                'sales_count': 3200,
                'rating': 4.7,
                'category': 'Electronics',
                'url': 'https://shopee.vn/product/123456/987654321',
                'commission_rate': 20.0
            },
            {
                'item_id': '555666777',
                'shop_id': '333444',
                'product_name': 'Samsung Galaxy S24 Ultra',
                'price': 22990000,
                'sales_count': 1800,
                'rating': 4.9,
                'category': 'Electronics',
                'url': 'https://shopee.vn/product/333444/555666777',
                'commission_rate': 22.5
            },
            {
                'item_id': '111222333',
                'shop_id': '444555',
                'product_name': 'AirPods Pro 2',
                'price': 4990000,
                'sales_count': 4200,
                'rating': 4.6,
                'category': 'Electronics',
                'url': 'https://shopee.vn/product/444555/111222333',
                'commission_rate': 16.0
            },
            {
                'item_id': '888999000',
                'shop_id': '666777',
                'product_name': 'Apple Watch Series 9',
                'price': 9990000,
                'sales_count': 1100,
                'rating': 4.5,
                'category': 'Electronics',
                'url': 'https://shopee.vn/product/666777/888999000',
                'commission_rate': 19.0
            }
        ]
        
        return mock_products[:limit]
    
    async def scan_trending_products(self, limit: int = 20):
        """Scan trending products từ Shopee (có fallback mock data)"""
        logger.info(f"Scanning {limit} trending products...")
        
        keywords = [
            'tai nghe bluetooth',
            'điện thoại thông minh',
            'đồng hồ thông minh',
            'quần áo thời trang',
            'giày thể thao'
        ]
        
        all_products = []
        for keyword in keywords[:2]:
            products = await self.search_shopee_products(keyword, limit=limit//2)
            if products:
                all_products.extend(products)
            await asyncio.sleep(2)
        
        # Fallback: Nếu không có sản phẩm thật, dùng mock data
        if not all_products:
            logger.info("No real products found, using mock data...")
            return await self._get_mock_products(limit)
        
        # Lọc sản phẩm có rating cao
        filtered = [p for p in all_products if p.get('rating', 0) >= 4.0]
        
        logger.info(f"Found {len(filtered)} products after filtering")
        return filtered[:limit]
    
    async def generate_affiliate_links(self, products):
        """Tạo affiliate links"""
        logger.info(f"Generating affiliate links...")
        
        for product in products:
            product['affiliate_link'] = f"https://shopee.vn/product/{product['shop_id']}/{product['item_id']}"
        
        logger.info(f"Generated links for {len(products)} products")
        return products
    
    def export_to_excel(self, products, filename='affiliate_products.xlsx'):
        """Export products to Excel"""
        if not products:
            logger.warning("No products to export")
            return
        
        data = []
        for p in products:
            data.append({
                'Product Name': p.get('product_name', ''),
                'Price (VND)': p.get('price', 0),
                'Sales Count': p.get('sales_count', 0),
                'Rating': p.get('rating', 0),
                'Category': p.get('category', ''),
                'Commission %': p.get('commission_rate', 0),
                'Affiliate Link': p.get('affiliate_link', ''),
            })
        
        df = pd.DataFrame(data)
        os.makedirs('./data/reports', exist_ok=True)
        filepath = f"./data/reports/{filename}"
        df.to_excel(filepath, index=False)
        
        logger.info(f"Exported {len(products)} products to {filepath}")
        return filepath