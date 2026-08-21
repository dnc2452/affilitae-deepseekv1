#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator - Điều phối tất cả Agents, Sub-Agents, Skills và MCP
"""

import logging
import asyncio
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import Main Agents
from agents.product_agent import ProductDiscoveryAgent
from agents.content_agent import ContentCreationAgent
from agents.posting_agent import AutoPostingAgent
from agents.analytics_agent import AnalyticsAgent

# Import Sub-Agents
from sub_agents.video_editor_agent import VideoEditorSubAgent
from sub_agents.caption_writer_agent import CaptionWriterSubAgent
from sub_agents.posting_agent import PostingSubAgent
from sub_agents.affiliate_research_agent import AffiliateResearchSubAgent

# Import MCP
from mcp.context_protocol import ModelContextProtocol

# Import Skills
from skills.shopee_skills import ShopeeSkills
from skills.video_skills import VideoSkills
from skills.caption_skills import CaptionSkills
from skills.affiliate_skills import AffiliateSkills
from skills.browser_controller import BrowserController

# Import Config
from config.settings import (
    HEADLESS_MODE,
    N8N_ENABLED,
    N8N_URL
)

# Telegram - optional, try import
try:
    from sub_agents.telegram_agent import TelegramSubAgent
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    TelegramSubAgent = None
    logging.warning("⚠️ TelegramSubAgent not available")

logger = logging.getLogger(__name__)


class AffiliateAgentOrchestrator:
    """
    Main Orchestrator - Điều phối toàn bộ hệ thống
    """
    
    def __init__(self):
        logger.info("=" * 70)
        logger.info("🚀 Initializing Affiliate Agent Orchestrator")
        logger.info("=" * 70)
        
        # Initialize MCP
        self.mcp = ModelContextProtocol()
        
        # ============================================================
        # MAIN AGENTS
        # ============================================================
        self.product_agent = ProductDiscoveryAgent()
        self.content_agent = ContentCreationAgent()
        self.posting_agent = AutoPostingAgent()
        self.analytics_agent = AnalyticsAgent()
        
        # ============================================================
        # SUB-AGENTS
        # ============================================================
        self.video_editor_sub_agent = VideoEditorSubAgent(self.mcp)
        self.caption_writer_sub_agent = CaptionWriterSubAgent(self.mcp)
        self.posting_sub_agent = PostingSubAgent(self.mcp)
        self.affiliate_research_agent = AffiliateResearchSubAgent(self.mcp)
        
        # ============================================================
        # TELEGRAM (Optional)
        # ============================================================
        self.telegram_agent = None
        if TELEGRAM_AVAILABLE and TelegramSubAgent:
            try:
                self.telegram_agent = TelegramSubAgent(self.mcp)
                logger.info("✅ Telegram Sub-Agent enabled")
            except Exception as e:
                logger.warning(f"⚠️ Telegram init failed: {e}")
                self.telegram_agent = None
        else:
            logger.info("ℹ️ Telegram Sub-Agent disabled (not available)")
        
        # ============================================================
        # SKILLS
        # ============================================================
        self.shopee_skills = ShopeeSkills()
        self.video_skills = VideoSkills()
        self.caption_skills = CaptionSkills()
        self.affiliate_skills = AffiliateSkills()
        
        # ============================================================
        # BROWSER CONTROLLER
        # ============================================================
        self.browser = BrowserController(headless=HEADLESS_MODE)
        logger.info(f"✅ Browser Controller initialized (headless={HEADLESS_MODE})")
        
        # ============================================================
        # N8N
        # ============================================================
        self.n8n_enabled = N8N_ENABLED
        self.n8n_url = N8N_URL
        if self.n8n_enabled:
            logger.info(f"✅ n8n integration enabled: {self.n8n_url}")
        else:
            logger.info("ℹ️ n8n integration disabled")
        
        # ============================================================
        # STATE
        # ============================================================
        self.workflow_results = {}
        self.is_running = False
        
        self.mcp.save_to_memory('orchestrator', self)
        
        logger.info("✅ All components initialized successfully")
        logger.info(f"📊 Session ID: {self.mcp.session_id}")
    
    # ============================================================
    # PHASE 0: RESEARCH
    # ============================================================
    async def phase_0_research_affiliates(self, query: str = "AI", limit: int = 10):
        """Phase 0: Nghiên cứu chương trình affiliate"""
        logger.info("\n" + "=" * 70)
        logger.info("🔍 PHASE 0: Affiliate Program Research")
        logger.info("=" * 70)
        
        try:
            self.mcp.push_context('research', {
                'agent_id': 'research_agent',
                'phase': 0,
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"📊 Searching for '{query}' programs...")
            
            task = {
                'type': 'search_programs',
                'query': query,
                'sort': 'top',
                'limit': limit
            }
            
            result = await self.affiliate_research_agent.execute_task(task)
            
            if result['status'] == 'success':
                programs = result['programs']
                logger.info(f"✅ Found {len(programs)} affiliate programs")
                
                logger.info("\n📋 Top Programs:")
                for idx, prog in enumerate(programs[:5], 1):
                    logger.info(f"   {idx}. {prog.get('name')} - {prog.get('commission_rate')} ({prog.get('category')})")
                
                self.mcp.save_to_memory('researched_programs', programs)
                self.mcp.pop_context()
                return programs
            else:
                logger.error(f"❌ Research failed: {result.get('message')}")
                self.mcp.pop_context()
                return None
                
        except Exception as e:
            logger.error(f"❌ Phase 0 error: {e}")
            self.mcp.pop_context()
            return None
    
    # ============================================================
    # PHASE 1: DISCOVER PRODUCTS
    # ============================================================
    async def phase_1_discover_products(self, use_browser: bool = False):
        """Phase 1: Discover high-commission products"""
        logger.info("\n" + "=" * 70)
        logger.info("📊 PHASE 1: Product Discovery")
        logger.info("=" * 70)
        
        try:
            self.mcp.push_context('product_discovery', {
                'agent_id': 'product_agent',
                'phase': 1,
                'timestamp': datetime.now().isoformat()
            })
            
            # Sử dụng mock data để test
            logger.info("📦 Using mock data for testing...")
            products = await self.product_agent.scan_trending_products(limit=5)
            
            if not products:
                logger.error("❌ No products found")
                self.mcp.pop_context()
                return None
            
            logger.info(f"✅ Found {len(products)} trending products")
            
            # Filter high commission
            high_comm_products = await self.shopee_skills.filter_high_commission_products(
                products, min_commission=15.0
            )
            
            logger.info(f"✅ {len(high_comm_products)} products with commission >= 15%")
            
            # Generate affiliate links
            products_with_links = await self.product_agent.generate_affiliate_links(high_comm_products)
            
            self.mcp.save_to_memory('discovered_products', products_with_links)
            
            # Export to Excel
            excel_path = self.product_agent.export_to_excel(products_with_links)
            logger.info(f"✅ Exported to {excel_path}")
            
            self.mcp.pop_context()
            return products_with_links
            
        except Exception as e:
            logger.error(f"❌ Phase 1 error: {e}")
            self.mcp.pop_context()
            return None
    
    # ============================================================
    # PHASE 2: CONTENT CREATION
    # ============================================================
    async def phase_2_create_content(self, products: List[Dict]):
        """Phase 2: Create video content"""
        logger.info("\n" + "=" * 70)
        logger.info("🎥 PHASE 2: Content Creation")
        logger.info("=" * 70)
        
        if not products:
            logger.error("❌ No products available")
            return None
        
        try:
            contents = []
            
            for idx, product in enumerate(products[:3], 1):
                product_name = product.get('product_name') or product.get('name', 'Unknown')
                logger.info(f"\n📱 Creating content {idx}/3: {product_name}")
                
                self.mcp.push_context('content_creation', {
                    'agent_id': 'content_agent',
                    'product_id': product.get('item_id') or product.get('id', ''),
                    'product_name': product_name
                })
                
                # Step 1: Download video (mock)
                logger.info(f"  ⏬ Step 1: Downloading video...")
                video_path = await self.content_agent.download_video(
                    category=product.get('category', 'Electronics')
                )
                logger.info(f"  ✅ Downloaded: {video_path}")
                
                # Step 2: Edit video
                logger.info(f"  ✂️  Step 2: Editing video...")
                edit_task = {
                    'type': 'add_watermark',
                    'video_path': video_path,
                    'product_name': product_name,
                    'affiliate_link': product.get('affiliate_link', '')
                }
                edit_result = await self.video_editor_sub_agent.execute_task(edit_task)
                processed_video = edit_result.get('output_path', video_path)
                logger.info(f"  ✅ Video processed: {processed_video}")
                
                # Step 3: Generate caption
                logger.info(f"  ✍️  Step 3: Generating captions...")
                caption_task = {
                    'type': 'generate_caption',
                    'product_name': product_name,
                    'price': f"{product.get('price', 0):,} VND",
                    'platform': 'tiktok'
                }
                caption_result = await self.caption_writer_sub_agent.execute_task(caption_task)
                captions = caption_result.get('captions', [])
                
                if captions:
                    selected_caption = captions[0]
                    logger.info(f"  ✅ Caption: {selected_caption[:50]}...")
                    
                    # Step 4: Check compliance
                    logger.info(f"  🔍 Step 4: Checking caption compliance...")
                    compliance_task = {
                        'type': 'check_compliance',
                        'caption': selected_caption,
                        'platform': 'tiktok'
                    }
                    compliance_result = await self.caption_writer_sub_agent.execute_task(compliance_task)
                    
                    if compliance_result.get('compliant', False):
                        logger.info(f"  ✅ Caption compliant")
                    else:
                        logger.warning(f"  ⚠️  Caption violations: {compliance_result.get('violations', [])}")
                    
                    contents.append({
                        'product': product,
                        'video': processed_video,
                        'caption': selected_caption,
                        'compliance': compliance_result.get('compliant', False)
                    })
                
                self.mcp.pop_context()
            
            logger.info(f"\n✅ Created {len(contents)} content items")
            self.mcp.save_to_memory('created_contents', contents)
            
            return contents
            
        except Exception as e:
            logger.error(f"❌ Phase 2 error: {e}")
            return None
    
    # ============================================================
    # PHASE 3: AUTO POSTING
    # ============================================================
    async def phase_3_auto_posting(self, contents: List[Dict]):
        """Phase 3: Auto posting to TikTok & Facebook"""
        logger.info("\n" + "=" * 70)
        logger.info("📤 PHASE 3: Auto Posting")
        logger.info("=" * 70)
        
        if not contents:
            logger.error("❌ No content available")
            return None
        
        try:
            posted_items = []
            
            for idx, content in enumerate(contents, 1):
                product_name = content['product'].get('product_name') or content['product'].get('name', 'Unknown')
                logger.info(f"\n📍 Posting {idx}/{len(contents)}: {product_name}")
                
                self.mcp.push_context('posting', {
                    'agent_id': 'posting_agent',
                    'product_name': product_name,
                    'content_index': idx
                })
                
                # Post to TikTok
                logger.info(f"  📱 Posting to TikTok...")
                tiktok_task = {
                    'type': 'post_to_tiktok',
                    'video_path': content['video'],
                    'caption': content['caption'],
                    'affiliate_link': content['product'].get('affiliate_link', '')
                }
                tiktok_result = await self.posting_sub_agent.execute_task(tiktok_task)
                
                if tiktok_result.get('status') == 'success':
                    logger.info(f"  ✅ TikTok posted")
                    posted_items.append({
                        'product': product_name,
                        'platform': 'tiktok',
                        'post_id': tiktok_result.get('post_id', ''),
                        'status': 'success'
                    })
                else:
                    logger.error(f"  ❌ TikTok posting failed")
                
                # Post to Facebook
                logger.info(f"  📘 Posting to Facebook...")
                facebook_task = {
                    'type': 'post_to_facebook',
                    'video_path': content['video'],
                    'caption': content['caption'],
                    'affiliate_link': content['product'].get('affiliate_link', '')
                }
                facebook_result = await self.posting_sub_agent.execute_task(facebook_task)
                
                if facebook_result.get('status') == 'success':
                    logger.info(f"  ✅ Facebook posted")
                    posted_items.append({
                        'product': product_name,
                        'platform': 'facebook',
                        'post_id': facebook_result.get('post_id', ''),
                        'status': 'success'
                    })
                else:
                    logger.error(f"  ❌ Facebook posting failed")
                
                self.mcp.pop_context()
            
            logger.info(f"\n✅ Total posts: {len(posted_items)}")
            self.mcp.save_to_memory('posted_items', posted_items)
            
            return posted_items
            
        except Exception as e:
            logger.error(f"❌ Phase 3 error: {e}")
            return None
    
    # ============================================================
    # PHASE 4: ANALYTICS
    # ============================================================
    async def phase_4_analytics(self):
        """Phase 4: Analytics & Optimization"""
        logger.info("\n" + "=" * 70)
        logger.info("📊 PHASE 4: Analytics & Optimization")
        logger.info("=" * 70)
        
        try:
            logger.info("📈 Collecting analytics data...")
            
            session_summary = self.mcp.get_session_summary()
            logger.info(f"✅ Session Summary:")
            logger.info(f"   - Session ID: {session_summary['session_id']}")
            logger.info(f"   - Contexts: {session_summary['context_count']}")
            logger.info(f"   - Memory Items: {session_summary['memory_items']}")
            
            products = self.mcp.get_from_memory('discovered_products')
            contents = self.mcp.get_from_memory('created_contents')
            posted = self.mcp.get_from_memory('posted_items')
            researched = self.mcp.get_from_memory('researched_programs')
            
            logger.info(f"📊 Workflow Summary:")
            logger.info(f"   - Products Discovered: {len(products) if products else 0}")
            logger.info(f"   - Content Created: {len(contents) if contents else 0}")
            logger.info(f"   - Posts Published: {len(posted) if posted else 0}")
            logger.info(f"   - Programs Researched: {len(researched) if researched else 0}")
            
            logger.info("💾 Generating analytics report...")
            report_path = await self.analytics_agent.generate_report()
            logger.info(f"✅ Report saved to: {report_path}")
            
            return {
                'session_summary': session_summary,
                'report_path': report_path,
                'products_count': len(products) if products else 0,
                'content_count': len(contents) if contents else 0,
                'posts_count': len(posted) if posted else 0,
                'researched_count': len(researched) if researched else 0
            }
            
        except Exception as e:
            logger.error(f"❌ Phase 4 error: {e}")
            return None
    
    # ============================================================
    # RUN FULL WORKFLOW
    # ============================================================
    async def run_full_workflow(
        self,
        run_research: bool = True,
        research_query: str = "AI",
        use_browser: bool = False
    ):
        """Run complete workflow"""
        self.is_running = True
        
        logger.info("\n\n")
        logger.info("╔" + "=" * 68 + "╗")
        logger.info("║" + " " * 15 + "🚀 AI AFFILIATE AGENT - FULL WORKFLOW" + " " * 15 + "║")
        logger.info("║" + f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^66} " + "║")
        logger.info("╚" + "=" * 68 + "╝")
        
        try:
            # Phase 0: Research
            if run_research:
                researched = await self.phase_0_research_affiliates(query=research_query, limit=10)
                if researched:
                    logger.info(f"✅ Research completed: {len(researched)} programs found")
            
            # Phase 1: Discover
            products = await self.phase_1_discover_products(use_browser=False)
            if not products:
                logger.error("❌ Cannot proceed - Phase 1 failed")
                return False
            
            # Phase 2: Create Content
            contents = await self.phase_2_create_content(products)
            if not contents:
                logger.error("❌ Cannot proceed - Phase 2 failed")
                return False
            
            # Phase 3: Post
            posted = await self.phase_3_auto_posting(contents)
            if not posted:
                logger.error("❌ Cannot proceed - Phase 3 failed")
                return False
            
            # Phase 4: Analytics
            analytics = await self.phase_4_analytics()
            
            self.workflow_results = {
                'products': products,
                'contents': contents,
                'posted': posted,
                'analytics': analytics,
                'completed_at': datetime.now().isoformat()
            }
            
            logger.info("\n" + "╔" + "=" * 68 + "╗")
            logger.info("║" + " " * 20 + "✅ WORKFLOW COMPLETED!" + " " * 25 + "║")
            logger.info("╚" + "=" * 68 + "╝")
            
            logger.info("\n📊 Final Results:")
            logger.info(f"   ✅ Products Discovered: {len(products)}")
            logger.info(f"   ✅ Content Created: {len(contents)}")
            logger.info(f"   ✅ Posts Published: {len(posted)}")
            
            logger.info("\n📁 Output Locations:")
            logger.info(f"   📊 Reports: ./data/reports/")
            logger.info(f"   🎬 Videos: ./data/videos/")
            logger.info(f"   📝 Logs: ./logs/")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Workflow error: {e}")
            return False
            
        finally:
            self.is_running = False


async def main():
    """Entry point"""
    orchestrator = AffiliateAgentOrchestrator()
    
    success = await orchestrator.run_full_workflow(
        run_research=True,
        research_query="AI",
        use_browser=False
    )
    
    if success:
        logger.info("\n🎉 All tasks completed successfully!")
    else:
        logger.error("\n❌ Workflow failed!")
    
    return success


if __name__ == '__main__':
    asyncio.run(main())