#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Affiliate Skills - Tích hợp openaffiliate.dev API
Nguồn: https://github.com/Affitor/affiliate-skills
"""

import logging
import httpx
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AffiliateSkills:
    """
    Skill tích hợp với Open Affiliate API
    Tìm kiếm và lấy thông tin các chương trình affiliate
    """
    
    def __init__(self):
        self.base_url = "https://openaffiliate.dev/api"
        self.timeout = 30.0
        logger.info("✅ AffiliateSkills initialized")
        logger.info("   📡 API: https://openaffiliate.dev")
        logger.info("   🔓 No API key required (fully public)")
    
    async def search_programs(self, query: str, sort: str = "top", limit: int = 10) -> List[Dict]:
        """
        Tìm kiếm chương trình affiliate
        
        Args:
            query: Từ khóa tìm kiếm (VD: "AI", "video", "hosting")
            sort: Sắp xếp theo "relevance", "trending", "new", "top"
            limit: Số lượng kết quả (mặc định 10)
        
        Returns:
            List[Dict]: Danh sách chương trình affiliate
        """
        logger.info(f"🔍 Searching affiliate programs: '{query}' (sort: {sort})")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/programs",
                    params={
                        "q": query,
                        "sort": sort,
                        "limit": limit
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    programs = data.get('programs', [])
                    logger.info(f"✅ Found {len(programs)} programs")
                    
                    # Chuẩn hóa dữ liệu để dùng chung
                    normalized = []
                    for prog in programs:
                        normalized.append(self._normalize_program(prog))
                    
                    return normalized
                else:
                    logger.error(f"❌ API error: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ Search error: {e}")
            return []
    
    async def get_program_details(self, slug: str) -> Optional[Dict]:
        """
        Lấy chi tiết 1 chương trình affiliate theo slug
        
        Args:
            slug: ID của chương trình (VD: "heygen")
        
        Returns:
            Dict: Thông tin chi tiết hoặc None nếu không tìm thấy
        """
        logger.info(f"📋 Getting details for: {slug}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/programs/{slug}")
                
                if response.status_code == 200:
                    program = response.json()
                    logger.info(f"✅ Found program: {program.get('name')}")
                    return self._normalize_program(program)
                elif response.status_code == 404:
                    logger.warning(f"⚠️  Program not found: {slug}")
                    return None
                else:
                    logger.error(f"❌ API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Get details error: {e}")
            return None
    
    def _normalize_program(self, program: Dict) -> Dict:
        """
        Chuẩn hóa dữ liệu từ API về format chung
        """
        commission = program.get('commission', {})
        payout = program.get('payout', {})
        
        return {
            'id': program.get('slug'),
            'name': program.get('name', 'N/A'),
            'url': program.get('url', ''),
            'logo': program.get('logo', ''),
            'category': program.get('category', ''),
            'description': program.get('description', ''),
            'short_description': program.get('shortDescription', ''),
            'tags': program.get('tags', []),
            'commission_rate': commission.get('rate', ''),
            'commission_type': commission.get('type', ''),
            'commission_currency': commission.get('currency', 'USD'),
            'commission_duration': commission.get('duration', ''),
            'cookie_days': program.get('cookieDays', 0),
            'payout_minimum': payout.get('minimum', 0),
            'payout_currency': payout.get('currency', 'USD'),
            'payout_frequency': payout.get('frequency', ''),
            'payout_methods': payout.get('methods', []),
            'stars': program.get('stars', 0),
            'verified': program.get('verified', False),
            'agent_prompt': program.get('agentPrompt', ''),
            'source': 'openaffiliate.dev',
            'fetched_at': datetime.now().isoformat()
        }
    
    async def get_high_commission_programs(self, min_commission: float = 20, limit: int = 10) -> List[Dict]:
        """
        Lọc các chương trình có hoa hồng cao
        
        Args:
            min_commission: Tối thiểu % hoa hồng (mặc định 20%)
            limit: Số lượng tối đa
        
        Returns:
            List[Dict]: Danh sách chương trình có hoa hồng cao
        """
        logger.info(f"💰 Filtering programs with commission >= {min_commission}%")
        
        # Tìm kiếm tất cả chương trình
        all_programs = await self.search_programs(query="", sort="top", limit=50)
        
        # Lọc theo hoa hồng
        high_comm = []
        for prog in all_programs:
            rate_str = prog.get('commission_rate', '0')
            # Parse số từ chuỗi (VD: "30%" -> 30)
            try:
                rate = float(rate_str.replace('%', '').replace('$', '').strip())
                if rate >= min_commission:
                    high_comm.append(prog)
            except:
                continue
            
            if len(high_comm) >= limit:
                break
        
        logger.info(f"✅ Found {len(high_comm)} high-commission programs")
        return high_comm
    
    async def search_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """
        Tìm kiếm chương trình theo danh mục
        
        Args:
            category: Danh mục (VD: "ai-tools", "hosting", "ecommerce")
            limit: Số lượng kết quả
        
        Returns:
            List[Dict]: Danh sách chương trình
        """
        logger.info(f"📂 Searching by category: {category}")
        
        programs = await self.search_programs(query=category, sort="top", limit=limit)
        return programs
    
    def format_for_report(self, programs: List[Dict]) -> List[Dict]:
        """
        Format dữ liệu để xuất ra báo cáo Excel
        """
        data = []
        for p in programs:
            data.append({
                'Program Name': p.get('name', ''),
                'Category': p.get('category', ''),
                'Commission': p.get('commission_rate', ''),
                'Commission Type': p.get('commission_type', ''),
                'Cookie Days': p.get('cookie_days', 0),
                'Payout Min': p.get('payout_minimum', 0),
                'Payout Currency': p.get('payout_currency', 'USD'),
                'Rating': p.get('stars', 0),
                'Verified': '✅' if p.get('verified') else '❌',
                'URL': p.get('url', ''),
                'Description': p.get('short_description', '')
            })
        
        return data