from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.settings import max_total_mb
from i18n import tr

def upload_summary(count,total_bytes):
    return tr("summary", count=count, total=total_bytes/1024/1024, maximum=max_total_mb())

def send_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton(tr("send_email"),callback_data="send_batch")],[InlineKeyboardButton(tr("cancel_restart"),callback_data="cancel_batch")]])

def restart_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton(tr("new_file"),callback_data="restart_batch")]])
