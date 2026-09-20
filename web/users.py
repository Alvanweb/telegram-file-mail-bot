from fastapi import Request
from fastapi.responses import RedirectResponse
from web.auth import logged
from web.i18n import context
from database.users import list_users,toggle_user,delete_user
from pathlib import Path

def setup_routes(app,templates):
    @app.get('/users')
    async def users_page(request:Request):
        if not logged(request): return RedirectResponse('/login',status_code=303)
        return templates.TemplateResponse(request=request,name='users.html',context={**context(),'users':list_users()})
    @app.post('/users/{telegram_id}/toggle')
    async def toggle(request:Request,telegram_id:int):
        if not logged(request): return RedirectResponse('/login',status_code=303)
        toggle_user(telegram_id); return RedirectResponse('/users',status_code=303)
    @app.post('/users/{telegram_id}/delete')
    async def delete(request:Request,telegram_id:int):
        if not logged(request): return RedirectResponse('/login',status_code=303)
        paths=delete_user(telegram_id)
        for path in paths:
            try: Path(path).unlink(missing_ok=True)
            except Exception: pass
        return RedirectResponse('/users',status_code=303)
