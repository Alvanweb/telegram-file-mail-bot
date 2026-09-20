import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / '.env')

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change-me')
SESSION_SECRET = os.getenv('SESSION_SECRET', 'change-this-secret')
DB_PATH = os.getenv('DB_PATH', str(BASE_DIR / 'bot.db'))
PANEL_HOST = os.getenv('PANEL_HOST', '127.0.0.1')
PANEL_PORT = int(os.getenv('PANEL_PORT', '8000'))

PENDING_DIR = BASE_DIR / 'storage' / 'pending_uploads'
PENDING_DIR.mkdir(parents=True, exist_ok=True)

DEFAULTS = {
    'smtp_host': os.getenv('SMTP_HOST', 'smtp-relay.brevo.com'),
    'smtp_port': os.getenv('SMTP_PORT', '587'),
    'smtp_user': os.getenv('SMTP_USER', ''),
    'smtp_password': os.getenv('SMTP_PASSWORD', ''),
    'smtp_from': os.getenv('SMTP_FROM', os.getenv('SMTP_USER', '')),
    'smtp_recipients': os.getenv('EMAIL_TO', ''),
    'smtp_use_tls': os.getenv('SMTP_USE_TLS', 'true').lower(),
    'max_total_mb': os.getenv('MAX_TOTAL_MB', '5'),
    'pending_retention_hours': os.getenv('PENDING_RETENTION_HOURS', '24'),
    'email_fields': '["first_name","username","phone","telegram_id","subject","file_count","total_size","filenames"]',
    'language': 'en',
}


def get_setting(key, default=None):
    from database.settings import get_setting as _get
    return _get(key, default)


def set_setting(key, value):
    from database.settings import set_setting as _set
    return _set(key, value)


def smtp_config():
    return {
        'host': get_setting('smtp_host', DEFAULTS['smtp_host']),
        'port': int(get_setting('smtp_port', DEFAULTS['smtp_port'])),
        'user': get_setting('smtp_user', DEFAULTS['smtp_user']),
        'password': get_setting('smtp_password', DEFAULTS['smtp_password']),
        'from': get_setting('smtp_from', DEFAULTS['smtp_from']),
        'recipients': get_setting('smtp_recipients', DEFAULTS['smtp_recipients']),
        'use_tls': str(get_setting('smtp_use_tls', DEFAULTS['smtp_use_tls'])).lower() == 'true',
    }


def max_total_mb():
    return int(get_setting('max_total_mb', DEFAULTS['max_total_mb']))


def max_total_bytes():
    return max_total_mb() * 1024 * 1024


def pending_retention_hours():
    return int(get_setting('pending_retention_hours', DEFAULTS['pending_retention_hours']))
