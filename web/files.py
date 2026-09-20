from fastapi import Request
from fastapi.responses import RedirectResponse
from web.auth import logged
from web.i18n import context
from database.files import list_files

def setup_routes(app,templates):
    @app.get('/files')
    async def files_page(request:Request):
        if not logged(request): return RedirectResponse('/login',status_code=303)
        return templates.TemplateResponse(request=request,name='files.html',context={**context(),'files':list_files()})
