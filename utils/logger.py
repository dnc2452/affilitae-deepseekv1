import logging
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

init(autoreset=True)

def setup_logger(name='AffiliateAgent', log_level='INFO'):
    """Setup logging configuration"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    os.makedirs('./logs', exist_ok=True)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    file_handler = logging.FileHandler(
        f'./logs/app_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger