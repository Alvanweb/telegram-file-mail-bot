import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import File, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse

from config.settings import DB_PATH, BASE_DIR
from database.settings import get_setting
from web.auth import logged
from web.i18n import context
from web.timezone import format_timestamp, get_timezone_name

BACKUP_DIR = BASE_DIR / 'storage' / 'backups'
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def _safe_backup_name(name):
    return Path(name).name


def _valid_sqlite(path):
    try:
        conn = sqlite3.connect(path)
        result = conn.execute('PRAGMA integrity_check').fetchone()[0]
        conn.close()
        return result == 'ok'
    except Exception:
        return False


def _create_backup(prefix='backup'):
    # Keep backup filenames in UTC for stable sorting and portability.
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    target = BACKUP_DIR / f'{prefix}_{timestamp}.db'
    target_conn = sqlite3.connect(target)
    try:
        if Path(DB_PATH).exists():
            source_conn = sqlite3.connect(DB_PATH)
            try:
                source_conn.backup(target_conn)
            finally:
                source_conn.close()
        else:
            target_conn.execute('VACUUM')
    finally:
        target_conn.close()
    return target


def _backup_view(path):
    stat = path.stat()
    return {
        'path': path,
        'name': path.name,
        'size': stat.st_size,
        'time': format_timestamp(stat.st_mtime),
        'mtime': stat.st_mtime,
    }


def setup_routes(app, templates):
    @app.get('/backups')
    async def backups_page(request: Request):
        if not logged(request):
            return RedirectResponse('/login', status_code=303)
        backups = sorted(
            [_backup_view(p) for p in BACKUP_DIR.glob('*.db') if p.is_file()],
            key=lambda item: item['mtime'],
            reverse=True,
        )
        return templates.TemplateResponse(
            request=request,
            name='backups.html',
            context={
                **context(),
                'backups': backups,
                'timezone': get_timezone_name(),
                'message': request.session.pop('backup_message', None),
                'error': request.session.pop('backup_error', None),
            },
        )

    @app.post('/backups/create')
    async def create_backup(request: Request):
        if not logged(request):
            return RedirectResponse('/login', status_code=303)
        try:
            target = _create_backup()
            request.session['backup_message'] = f'Backup created: {target.name}'
        except Exception as exc:
            request.session['backup_error'] = f'Backup failed: {exc}'
        return RedirectResponse('/backups', status_code=303)

    @app.get('/backups/download/{filename}')
    async def download_backup(request: Request, filename: str):
        if not logged(request):
            return RedirectResponse('/login', status_code=303)
        path = BACKUP_DIR / _safe_backup_name(filename)
        if not path.exists() or path.suffix != '.db':
            return RedirectResponse('/backups', status_code=303)
        return FileResponse(path, filename=path.name, media_type='application/octet-stream')

    @app.post('/backups/delete/{filename}')
    async def delete_backup(request: Request, filename: str):
        if not logged(request):
            return RedirectResponse('/login', status_code=303)
        path = BACKUP_DIR / _safe_backup_name(filename)
        if path.exists() and path.suffix == '.db':
            path.unlink()
        return RedirectResponse('/backups', status_code=303)

    @app.post('/backups/restore')
    async def restore_backup(request: Request, backup: UploadFile = File(...)):
        if not logged(request):
            return RedirectResponse('/login', status_code=303)

        temp = BACKUP_DIR / f'.restore_{os.getpid()}_{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")}.db'
        try:
            with temp.open('wb') as output:
                while chunk := await backup.read(1024 * 1024):
                    output.write(chunk)

            if not _valid_sqlite(temp):
                raise ValueError('The uploaded file is not a valid SQLite database.')

            _create_backup(prefix='pre_restore')
            source_conn = sqlite3.connect(temp)
            destination_conn = sqlite3.connect(DB_PATH)
            try:
                source_conn.backup(destination_conn)
            finally:
                destination_conn.close()
                source_conn.close()
            request.session['backup_message'] = 'Database restored successfully. Restart the service after restore.'
        except Exception as exc:
            temp.unlink(missing_ok=True)
            request.session['backup_error'] = f'Restore failed: {exc}'

        return RedirectResponse('/backups', status_code=303)
