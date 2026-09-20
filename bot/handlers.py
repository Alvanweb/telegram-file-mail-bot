import asyncio, logging, os, tempfile, json
from pathlib import Path
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database.users import get_user, register_user, clear_subject, set_subject
from database.pending import pending_total, add_pending_file, get_pending_files, clear_pending_files, create_file_record
from config.settings import PENDING_DIR, max_total_bytes, max_total_mb
from database.settings import get_setting
from mail.smtp import send_email_sync
from bot.helpers import upload_summary, send_button, restart_button
from i18n import tr

logger=logging.getLogger('telegram-file-mail-bot')


async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user=update.effective_user
    if not user or not update.message:return
    row=get_user(user.id)
    if row and row['active']==0:
        await update.message.reply_text(tr('telegram_blocked')); return
    clear_pending_files(user.id); clear_subject(user.id)
    if not row:
        kb=ReplyKeyboardMarkup([[KeyboardButton(tr('register_button'),request_contact=True)]],resize_keyboard=True,one_time_keyboard=True)
        await update.message.reply_text(tr('register_prompt'),reply_markup=kb); return
    await update.message.reply_text(tr('subject_prompt'),reply_markup=ReplyKeyboardRemove())


async def contact_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user=update.effective_user; contact=update.message.contact
    if not user or not contact:return
    if contact.user_id != user.id:
        await update.message.reply_text(tr('wrong_contact')); return
    register_user(user.id,user.first_name or '',user.username or '',contact.phone_number)
    clear_pending_files(user.id); clear_subject(user.id)
    await update.message.reply_text(tr('registered'),reply_markup=ReplyKeyboardRemove())


async def text_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user=update.effective_user
    if not user or not update.message:return
    row=get_user(user.id)
    if not row: await update.message.reply_text(tr('start_register')); return
    if row['active']==0: await update.message.reply_text(tr('blocked')); return
    text=(update.message.text or '').strip()
    if not text:return
    if len(text)>200: await update.message.reply_text(tr('subject_too_long')); return
    clear_pending_files(user.id); set_subject(user.id,text)
    await update.message.reply_text(tr('subject_saved', mb=max_total_mb()))


async def get_telegram_file(message):
    if message.document:
        x=await message.document.get_file(); return x, message.document.file_name or f'document_{message.document.file_unique_id}', message.document.file_size or 0
    if message.photo:
        x=await message.photo[-1].get_file(); return x, f'photo_{message.photo[-1].file_unique_id}.jpg', message.photo[-1].file_size or 0
    if message.video:
        x=await message.video.get_file(); return x, message.video.file_name or f'video_{message.video.file_unique_id}.mp4', message.video.file_size or 0
    if message.audio:
        x=await message.audio.get_file(); return x, message.audio.file_name or f'audio_{message.audio.file_unique_id}', message.audio.file_size or 0
    if message.voice:
        x=await message.voice.get_file(); return x, f'voice_{message.voice.file_unique_id}.ogg', message.voice.file_size or 0
    return None,None,0


async def file_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user=update.effective_user
    if not user or not update.message:return
    row=get_user(user.id)
    if not row: await update.message.reply_text(tr('start_register')); return
    if row['active']==0: await update.message.reply_text(tr('blocked')); return
    if not row['pending_subject']: await update.message.reply_text(tr('subject_first')); return
    tgfile,filename,reported_size=await get_telegram_file(update.message)
    if not tgfile: await update.message.reply_text(tr('unsupported')); return
    _,current_total=pending_total(user.id)
    if current_total+reported_size>max_total_bytes():
        await update.message.reply_text(tr('size_limit', current=current_total/1024/1024, new=reported_size/1024/1024, maximum=max_total_mb())); return
    temp_path=None
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=Path(filename).suffix,dir=PENDING_DIR) as f: temp_path=f.name
        await update.message.reply_text(tr('receiving'))
        await tgfile.download_to_drive(custom_path=temp_path)
        actual=os.path.getsize(temp_path); _,after=pending_total(user.id)
        if after+actual>max_total_bytes():
            Path(temp_path).unlink(missing_ok=True); await update.message.reply_text(tr('size_limit', current=after/1024/1024, new=actual/1024/1024, maximum=max_total_mb())); return
        add_pending_file(user.id,filename,temp_path,actual); temp_path=None
        count,total=pending_total(user.id)
        await update.message.reply_text(tr('file_added', summary=upload_summary(count,total)),reply_markup=send_button())
    except Exception:
        logger.exception('File download failed')
        if temp_path: Path(temp_path).unlink(missing_ok=True)
        await update.message.reply_text(tr('download_failed'))


async def send_batch(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    if not query:return
    await query.answer(); user=query.from_user; row=get_user(user.id)
    if not row: await query.edit_message_text(tr('start_register')); return
    if row['active']==0: await query.edit_message_text(tr('blocked')); return
    subject=row['pending_subject']; pending=get_pending_files(user.id)
    if not subject: await query.edit_message_text(tr('subject_missing')); return
    if not pending: await query.edit_message_text(tr('no_files')); return
    total=sum(x['size_bytes'] for x in pending)
    if total>max_total_bytes(): await query.edit_message_text(tr('total_limit')); return
    await query.edit_message_text(tr('sending', count=len(pending), total=total/1024/1024))
    attachments=[(x['path'],x['filename']) for x in pending]
    try:
        selected_fields = json.loads(get_setting('email_fields', '[]'))
    except Exception:
        selected_fields = []

    labels = {
        'first_name': (tr('full_name'), user.first_name or '-'),
        'username': (tr('telegram_username'), f'@{user.username}' if user.username else '-'),
        'phone': (tr('mobile'), row['phone'] or '-'),
        'telegram_id': (tr('telegram_id'), str(user.id)),
        'subject': (tr('email_subject'), subject),
        'file_count': (tr('file_count'), str(len(pending))),
        'total_size': (tr('total_size'), f'{total/1024/1024:.2f} MB'),
        'filenames': (tr('filenames'), '\n'.join(f'- {x["filename"]} — {x["size_bytes"]/1024/1024:.2f} MB' for x in pending)),
    }
    body_lines = ['***FROM SB9302_BOT MAIL SERVICE***', '']
    for field in selected_fields:
        if field in labels:
            label, value = labels[field]
            body_lines.extend([f'{label}: {value}', ''])
    body = '\n'.join(body_lines).rstrip() + '\n'
    try:
        await asyncio.to_thread(send_email_sync,subject,body,attachments)
        for x in pending: create_file_record(user.id,x['filename'],subject,x['size_bytes'],'success')
        clear_pending_files(user.id); clear_subject(user.id)
        await query.edit_message_text(
            tr('mail_success', count=len(pending), total=total/1024/1024),
            reply_markup=restart_button(),
        )
    except Exception as exc:
        logger.exception('Batch email delivery failed')
        for x in pending: create_file_record(user.id,x['filename'],subject,x['size_bytes'],'failed',str(exc))
        await query.edit_message_text(
            tr('send_failed'),
            reply_markup=send_button(),
        )


async def cancel_batch(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    if not query:return
    await query.answer(); user=query.from_user; clear_pending_files(user.id); clear_subject(user.id)
    await query.edit_message_text(tr('cancelled'))


async def cancel_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user=update.effective_user
    if not user:return
    clear_pending_files(user.id); clear_subject(user.id)
    await update.message.reply_text(tr('cancel_command'),reply_markup=ReplyKeyboardRemove())


async def restart_batch(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    if not query:return
    await query.answer()
    user=query.from_user
    row=get_user(user.id)
    if not row:
        await query.edit_message_text(tr('start_register'))
        return
    if row['active']==0:
        await query.edit_message_text(tr('blocked'))
        return
    clear_pending_files(user.id)
    clear_subject(user.id)
    await query.edit_message_text(tr('restart'))
