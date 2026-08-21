#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Affiliate Agent - Kiếm tiền tự động từ Shopee + TikTok
Version 2.0 - With MCP, Sub-Agents, Skills
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Create directories
for dir_path in ['./data', './data/videos', './data/reports', './logs', './config', './agents', './sub_agents', './skills', './mcp']:
    os.makedirs(dir_path, exist_ok=True)

# Setup logging
log_file = f'./logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import orchestrator
try:
    from orchestrator import AffiliateAgentOrchestrator
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    logger.error("Make sure all files are in correct directories!")
    sys.exit(1)


async def main():
    """Main entry point"""
    try:
        # Check Python version
        if sys.version_info < (3, 10):
            logger.error("❌ Python 3.10+ is required")
            sys.exit(1)
        
        logger.info("🚀 Starting AI Affiliate Agent Orchestrator...")
        
        # Initialize orchestrator
        orchestrator = AffiliateAgentOrchestrator()
        
        # Run workflow
        success = await orchestrator.run_full_workflow()
        
        if success:
            logger.info("\n" + "="*70)
            logger.info("🎉 Agent completed all tasks successfully!")
            logger.info("="*70)
            logger.info("\n📊 What happens next:")
            logger.info("   1. Monitor your TikTok & Facebook posts")
            logger.info("   2. Check affiliate earnings in your dashboard")
            logger.info("   3. Optimize content based on analytics")
            logger.info("   4. Run agent again tomorrow for more posts")
            logger.info("\n💡 Tips:")
            logger.info("   - Create consistent content daily")
            logger.info("   - Monitor views, likes, and clicks")
            logger.info("   - Refine captions based on performance")
            logger.info("   - Scale to multiple product categories")
            return 0
        else:
            logger.error("\n❌ Workflow failed")
            return 1
            
    except KeyboardInterrupt:
        logger.info("\n⏸️  Agent stopped by user")
        return 0
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)