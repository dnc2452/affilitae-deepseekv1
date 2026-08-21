#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Affiliate Research Sub-Agent - Tìm kiếm chương trình affiliate
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class AffiliateResearchSubAgent:
    """
    Sub-agent chuyên nghiên cứu chương trình affiliate
    - Tìm kiếm chương trình từ Open Affiliate API
    - Phân tích chương trình tiềm năng
    - Lọc theo hoa hồng, category
    """
    
    def __init__(self, mcp):
        self.mcp = mcp
        self.name = "AffiliateResearchSubAgent"
        self.capabilities = [
            'search_programs',
            'analyze_program',
            'filter_by_commission',
            'get_trending'
        ]
        logger.info(f"✅ {self.name} initialized")
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi task nghiên cứu"""
        logger.info(f"🔍 {self.name} executing: {task.get('type')}")
        
        task_type = task.get('type')
        
        if task_type == 'search_programs':
            return await self._search_programs(task)
        elif task_type == 'analyze_program':
            return await self._analyze_program(task)
        elif task_type == 'filter_by_commission':
            return await self._filter_by_commission(task)
        elif task_type == 'get_trending':
            return await self._get_trending(task)
        else:
            return {
                'status': 'error',
                'message': f'Unknown task type: {task_type}'
            }
    
    async def _search_programs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Tìm kiếm chương trình affiliate"""
        query = task.get('query', '')
        sort = task.get('sort', 'top')
        limit = task.get('limit', 10)
        
        logger.info(f"🔎 Searching programs: '{query}'")
        
        # Mock data - thực tế sẽ gọi API
        programs = [
            {
                'id': 'heygen',
                'name': 'HeyGen',
                'category': 'ai-tools',
                'commission_rate': '30%',
                'commission_type': 'cps_recurring',
                'cookie_days': 60,
                'verified': True,
                'stars': 42,
                'url': 'https://heygen.com',
                'description': 'AI video generation platform'
            },
            {
                'id': 'shopee',
                'name': 'Shopee Affiliate',
                'category': 'ecommerce',
                'commission_rate': '15-25%',
                'commission_type': 'cps',
                'cookie_days': 30,
                'verified': True,
                'stars': 95,
                'url': 'https://affiliate.shopee.vn',
                'description': 'Sàn thương mại điện tử hàng đầu Việt Nam'
            },
            {
                'id': 'lazada',
                'name': 'Lazada Affiliate',
                'category': 'ecommerce',
                'commission_rate': '10-20%',
                'commission_type': 'cps',
                'cookie_days': 30,
                'verified': True,
                'stars': 88,
                'url': 'https://affiliate.lazada.vn',
                'description': 'Nền tảng mua sắm trực tuyến lớn'
            }
        ]
        
        # Lọc theo query nếu có
        if query:
            filtered = [p for p in programs if query.lower() in p['name'].lower() or query.lower() in p['category'].lower()]
        else:
            filtered = programs
        
        # Sắp xếp
        if sort == 'top':
            filtered = sorted(filtered, key=lambda x: x.get('stars', 0), reverse=True)
        elif sort == 'trending':
            filtered = filtered  # Mock trending
        
        # Giới hạn
        result = filtered[:limit]
        
        # Lưu vào MCP
        self.mcp.save_to_memory('affiliate_programs', result)
        
        return {
            'status': 'success',
            'count': len(result),
            'programs': result,
            'query': query,
            'sort': sort
        }
    
    async def _analyze_program(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích 1 chương trình cụ thể"""
        program_id = task.get('program_id') or task.get('slug')
        
        if not program_id:
            return {'status': 'error', 'message': 'Program ID required'}
        
        logger.info(f"📊 Analyzing program: {program_id}")
        
        # Mock program detail
        program = {
            'id': program_id,
            'name': 'Sample Program',
            'commission_rate': '20%',
            'cookie_days': 45,
            'verified': True,
            'stars': 75,
            'analysis': {
                'score': 85,
                'potential': 'high',
                'recommendation': '✅ Recommended - High commission and good reputation',
                'pros': ['High commission rate', 'Good cookie duration', 'Verified program'],
                'cons': ['Competitive niche']
            }
        }
        
        return {
            'status': 'success',
            'program': program,
            'analysis': program.get('analysis', {})
        }
    
    async def _filter_by_commission(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Lọc chương trình theo hoa hồng tối thiểu"""
        min_commission = task.get('min_commission', 15)
        programs = task.get('programs', [])
        
        if not programs:
            # Lấy từ MCP nếu không có
            programs = self.mcp.get_from_memory('affiliate_programs') or []
        
        logger.info(f"💰 Filtering programs with commission >= {min_commission}%")
        
        filtered = []
        for p in programs:
            rate = p.get('commission_rate', '0%')
            try:
                # Parse số từ chuỗi (VD: "30%" -> 30)
                num = float(''.join(filter(str.isdigit, rate)) or '0')
                if num >= min_commission:
                    filtered.append(p)
            except:
                continue
        
        return {
            'status': 'success',
            'count': len(filtered),
            'programs': filtered,
            'min_commission': min_commission
        }
    
    async def _get_trending(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Lấy các chương trình đang trending"""
        limit = task.get('limit', 5)
        category = task.get('category', 'all')
        
        logger.info(f"📈 Getting trending programs in {category}")
        
        # Mock trending programs
        trending = [
            {'name': 'HeyGen', 'trend_score': 95, 'growth': '+45%'},
            {'name': 'Shopee', 'trend_score': 92, 'growth': '+30%'},
            {'name': 'Lazada', 'trend_score': 88, 'growth': '+25%'},
            {'name': 'TikTok Shop', 'trend_score': 85, 'growth': '+40%'},
        ][:limit]
        
        return {
            'status': 'success',
            'count': len(trending),
            'trending': trending,
            'category': category
        }