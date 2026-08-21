import logging
from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import (
    SCAN_PRODUCTS_TIME,
    CREATE_CONTENT_TIME,
    POST_TIKTOK_TIME,
    POST_FACEBOOK_TIME,
    GENERATE_ANALYTICS_TIME
)

logger = logging.getLogger(__name__)

class JobScheduler:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start scheduler"""
        logger.info("Starting job scheduler...")
        
        # Schedule jobs
        self.scheduler.add_job(
            self.orchestrator.phase_1_discover_products,
            'cron',
            hour=8,
            minute=0,
            id='discover_products'
        )
        
        self.scheduler.add_job(
            self.orchestrator.phase_2_create_content,
            'cron',
            hour=10,
            minute=0,
            id='create_content'
        )
        
        self.scheduler.add_job(
            self.orchestrator.phase_3_auto_posting,
            'cron',
            hour='14,18,22',
            minute=0,
            id='post_tiktok'
        )
        
        self.scheduler.start()
        logger.info("✅ Scheduler started")
    
    def stop(self):
        """Stop scheduler"""
        self.scheduler.shutdown()
        logger.info("❌ Scheduler stopped")