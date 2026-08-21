import logging
import asyncio
from typing import List, Dict

logger = logging.getLogger(__name__)

class ShopeeSkills:
    """Shopee-related skills for agents"""
    
    def __init__(self):
        logger.info("ShopeeSkills loaded")
    
    async def search_products_by_keyword(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Search products by keyword"""
        logger.info(f"Searching products: {keyword}")
        
        # Mock data
        products = [
            {
                'id': '123456',
                'name': f'{keyword} - Premium',
                'price': 1000000,
                'commission': 18.5,
                'sales': 2500,
                'rating': 4.8
            },
            {
                'id': '234567',
                'name': f'{keyword} - Standard',
                'price': 500000,
                'commission': 20.0,
                'sales': 3200,
                'rating': 4.7
            },
        ]
        
        return products[:limit]
    
    async def get_product_details(self, product_id: str) -> Dict:
        """Get detailed product information"""
        logger.info(f"Getting details for product: {product_id}")
        
        details = {
            'id': product_id,
            'name': 'Sample Product',
            'price': 1000000,
            'description': 'High quality product',
            'images': ['img1.jpg', 'img2.jpg'],
            'commission_rate': 18.5,
            'sales_count': 2500,
            'rating': 4.8,
            'reviews_count': 500,
            'shop_name': 'Official Shop',
            'shop_rating': 4.9,
            'discount_info': '15% off'
        }
        
        return details
    
    async def get_trending_products(self, category: str = 'Electronics') -> List[Dict]:
        """Get trending products by category"""
        logger.info(f"Fetching trending products in {category}")
        
        trending = [
            {
                'id': '111111',
                'name': 'iPhone 15 Pro',
                'price': 35990000,
                'trend_score': 95,
                'commission': 18.5,
                'sales_trend': 'UP'
            },
            {
                'id': '222222',
                'name': 'Samsung S24',
                'price': 24990000,
                'trend_score': 92,
                'commission': 20.0,
                'sales_trend': 'UP'
            },
        ]
        
        return trending
    
    async def filter_high_commission_products(self, products: List[Dict], 
                                             min_commission: float = 15.0) -> List[Dict]:
        """Filter products with high commission"""
        logger.info(f"Filtering products with commission >= {min_commission}%")
        
        filtered = [p for p in products if p.get('commission', 0) >= min_commission]
        return filtered
    
    async def create_short_affiliate_link(self, product_id: str, shop_id: str) -> str:
        """Create short affiliate link"""
        logger.info(f"Creating affiliate link for product {product_id}")
        
        link = f"https://shopee.vn/product/{shop_id}/{product_id}?aff=1"
        return link
    
    async def get_product_conversion_rate(self, product_id: str) -> float:
        """Get estimated conversion rate"""
        logger.info(f"Getting conversion rate for {product_id}")
        
        # Mock conversion rate
        return 2.5  # 2.5% conversion rate