#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

SHOPEE_EMAIL = os.getenv('SHOPEE_EMAIL', '')
SHOPEE_PASSWORD = os.getenv('SHOPEE_PASSWORD', '')
TIKTOK_USERNAME = os.getenv('TIKTOK_USERNAME', '')
TIKTOK_PASSWORD = os.getenv('TIKTOK_PASSWORD', '')
FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL', '')
FACEBOOK_PASSWORD = os.getenv('FACEBOOK_PASSWORD', '')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID', '')

DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', './data/videos')
EXPORT_DIR = os.getenv('EXPORT_DIR', './data/reports')
DB_PATH = os.getenv('DB_PATH', './data/products.db')

MAX_VIDEOS_PER_DAY = int(os.getenv('MAX_VIDEOS_PER_DAY', '5'))
VIDEO_QUALITY = os.getenv('VIDEO_QUALITY', '720')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

print("✅ Config loaded!")
# ===== BROWSER SETTINGS =====
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'false').lower() == 'true'
BROWSER_TIMEOUT = int(os.getenv('BROWSER_TIMEOUT', '30'))
HUMAN_TYPING_SPEED = float(os.getenv('HUMAN_TYPING_SPEED', '0.1'))
SCROLL_DELAY_MIN = float(os.getenv('SCROLL_DELAY_MIN', '0.3'))
SCROLL_DELAY_MAX = float(os.getenv('SCROLL_DELAY_MAX', '0.8'))

# ===== TELEGRAM SETTINGS =====
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')
TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID', '')
TELEGRAM_ADMIN_IDS = os.getenv('TELEGRAM_ADMIN_IDS', '')

# ===== N8N SETTINGS =====
N8N_ENABLED = os.getenv('N8N_ENABLED', 'false').lower() == 'true'
N8N_URL = os.getenv('N8N_URL', 'http://localhost:5678')
N8N_API_KEY = os.getenv('N8N_API_KEY', '')