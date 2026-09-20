from fastapi import Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from config.settings import ADMIN_USERNAME, ADMIN_PASSWORD
from web.i18n import context
from i18n import tr

def logged(request: Request): return request.session.get('admin') is True

def setup_routes(app, templates):
    @app.get('/login',response_class=HTMLResponse)
    async def login_page(request:Request): return templates.TemplateResponse(request=request,name='login.html',context={**context(),'error':None})
    @app.post('/login')
    async def login(request:Request,username:str=Form(...),password:str=Form(...)):
        if username==ADMIN_USERNAME and password==ADMIN_PASSWORD:
            request.session['admin']=True; return RedirectResponse('/',status_code=303)
        return templates.TemplateResponse(request=request,name='login.html',context={**context(),'error':tr('invalid_login')},status_code=401)
    @app.get('/logout')
    async def logout(request:Request): request.session.clear(); return RedirectResponse('/login',status_code=303)
