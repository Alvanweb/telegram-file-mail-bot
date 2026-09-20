from fastapi import Request
from fastapi.responses import RedirectResponse
from database.users import list_users
from database.files import file_stats
from web.auth import logged
from web.i18n import context

def setup_routes(app,templates):
    @app.get('/')
    async def dashboard(request:Request):
        if not logged(request): return RedirectResponse('/login',status_code=303)
        users=list_users(); total_files,success,failed=file_stats(); active=sum(1 for x in users if x['active']); blocked=len(users)-active
        return templates.TemplateResponse(request=request,name='dashboard.html',context={**context(),'total_users':len(users),'active_users':active,'blocked_users':blocked,'total_files':total_files,'successful_files':success,'failed_files':failed})
