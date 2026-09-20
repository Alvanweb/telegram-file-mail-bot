import asyncio, logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from config.settings import PANEL_HOST, PANEL_PORT, SESSION_SECRET
from database.core import init_db
from database.settings import init_settings
from bot.app import build_bot
from bot.cleanup import cleanup_loop
from web.auth import setup_routes as setup_auth
from web.dashboard import setup_routes as setup_dashboard
from web.users import setup_routes as setup_users
from web.files import setup_routes as setup_files
from web.settings import setup_routes as setup_settings

logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(message)s')
logger=logging.getLogger('telegram-file-mail-bot')
BASE_DIR=__import__('pathlib').Path(__file__).resolve().parent
templates=Jinja2Templates(directory=str(BASE_DIR/'templates'))
bot_application=None
cleanup_task=None

@asynccontextmanager
async def lifespan(app):
    global bot_application, cleanup_task
    init_db(); init_settings()
    bot_application=build_bot()
    await bot_application.initialize(); await bot_application.start(); await bot_application.updater.start_polling(allowed_updates=__import__('telegram').Update.ALL_TYPES)
    cleanup_task=asyncio.create_task(cleanup_loop())
    logger.info('Telegram bot polling started successfully')
    yield
    if cleanup_task: cleanup_task.cancel()
    if bot_application.updater.running: await bot_application.updater.stop()
    if bot_application.running: await bot_application.stop()
    await bot_application.shutdown()

app=FastAPI(title='Telegram File Mail Bot',lifespan=lifespan)
app.add_middleware(SessionMiddleware,secret_key=SESSION_SECRET,https_only=False,same_site='lax',max_age=8*60*60)
app.mount('/static',StaticFiles(directory=str(BASE_DIR/'static')),name='static')
setup_auth(app,templates); setup_dashboard(app,templates); setup_users(app,templates); setup_files(app,templates); setup_settings(app,templates)

if __name__=='__main__': uvicorn.run(app,host=PANEL_HOST,port=PANEL_PORT)
