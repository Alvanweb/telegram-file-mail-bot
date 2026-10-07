from fastapi import Request
from fastapi.responses import RedirectResponse
from web.auth import logged
from web.i18n import context
from database.files import list_files, count_files

PER_PAGE = 25


def setup_routes(app, templates):
    @app.get('/files')
    async def files_page(request: Request, page: int = 1, search: str = ''):
        if not logged(request):
            return RedirectResponse('/login', status_code=303)

        total = count_files(search)
        pages = max((total + PER_PAGE - 1) // PER_PAGE, 1)
        page = min(max(page, 1), pages)
        rows = list_files(page=page, per_page=PER_PAGE, search=search)

        return templates.TemplateResponse(
            request=request,
            name='files.html',
            context={
                **context(),
                'files': rows,
                'page': page,
                'pages': pages,
                'total_files': total,
                'per_page': PER_PAGE,
                'search': search,
            },
        )
