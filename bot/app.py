from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config.settings import BOT_TOKEN
from bot.handlers import start, contact_handler, text_handler, file_handler, send_batch, cancel_batch, cancel_command, restart_batch


def build_bot():
    if not BOT_TOKEN: raise RuntimeError('BOT_TOKEN is not configured')
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('cancel',cancel_command))
    app.add_handler(MessageHandler(filters.CONTACT,contact_handler))
    app.add_handler(CallbackQueryHandler(send_batch,pattern='^send_batch$'))
    app.add_handler(CallbackQueryHandler(cancel_batch,pattern='^cancel_batch$'))
    app.add_handler(CallbackQueryHandler(restart_batch,pattern='^restart_batch$'))
    app.add_handler(MessageHandler(filters.Document.ALL|filters.PHOTO|filters.VIDEO|filters.AUDIO|filters.VOICE,file_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,text_handler))
    return app
