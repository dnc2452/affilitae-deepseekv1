#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Affiliate Agent - Main Entry Point
"""

import sys
import asyncio
import logging
import codecs
from datetime import datetime

# Set encoding for stdout to handle emoji/Unicode on Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("🚀 AI AFFILIATE AGENT STARTING")
    logger.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        from orchestrator import AffiliateAgentOrchestrator
        
        orchestrator = AffiliateAgentOrchestrator()
        logger.info("✅ Orchestrator initialized")
        
        success = await orchestrator.run_full_workflow(
            run_research=True,
            research_query="AI",
            use_browser=False
        )
        
        if success:
            logger.info("\n" + "=" * 60)
            logger.info("🎉 ALL TASKS COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            
            # In kết quả
            results = orchestrator.workflow_results
            logger.info(f"\n📊 Final Results:")
            logger.info(f"   ✅ Products: {len(results.get('products', []))}")
            logger.info(f"   ✅ Contents: {len(results.get('contents', []))}")
            logger.info(f"   ✅ Posts: {len(results.get('posted', []))}")
            
            # Kết nối Telegram nếu có
            if orchestrator.telegram_agent:
                await orchestrator.telegram_agent.send_message(
                    text=f"✅ **Workflow Completed!**\n"
                         f"📊 Products: {len(results.get('products', []))}\n"
                         f"🎬 Contents: {len(results.get('contents', []))}\n"
                         f"📤 Posts: {len(results.get('posted', []))}"
                )
                logger.info("✅ Telegram notification sent")
            
            return True
        else:
            logger.error("❌ Workflow failed!")
            return False
            
    except KeyboardInterrupt:
        logger.info("\n⏹️ Stopped by user")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    exit_code = 0 if asyncio.run(main()) else 1
    sys.exit(exit_code)