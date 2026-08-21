#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Mock - Chay thu he thong voi du lieu mau
"""

import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_mock():
    logger.info("=" * 60)
    logger.info("START TEST MOCK")
    logger.info("=" * 60)
    
    try:
        from orchestrator import AffiliateAgentOrchestrator
        orchestrator = AffiliateAgentOrchestrator()
        logger.info("Orchestrator created successfully")
        
        success = await orchestrator.run_full_workflow(
            run_research=True,
            research_query="AI",
            use_browser=False
        )
        
        if success:
            logger.info("TEST MOCK SUCCESS!")
        else:
            logger.error("TEST MOCK FAILED!")
            
    except Exception as e:
        logger.error(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
   
    return True

if __name__ == "__main__":
    asyncio.run(test_mock())