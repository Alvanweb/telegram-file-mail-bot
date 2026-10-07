from database.core import db


def _search_clause(search):
    search = (search or '').strip()
    if not search:
        return '', []
    value = f'%{search}%'
    return (
        '''WHERE (
            files.filename LIKE ? OR
            files.subject LIKE ? OR
            files.status LIKE ? OR
            users.first_name LIKE ? OR
            users.username LIKE ? OR
            users.phone LIKE ? OR
            CAST(files.telegram_id AS TEXT) LIKE ?
        )''',
        [value] * 7,
    )


def count_files(search=''):
    conn = db()
    where, params = _search_clause(search)
    row = conn.execute(
        f'''SELECT COUNT(*) FROM files
            LEFT JOIN users ON users.telegram_id=files.telegram_id
            {where}''',
        params,
    ).fetchone()
    conn.close()
    return int(row[0])


def list_files(page=1, per_page=25, search=''):
    page = max(int(page or 1), 1)
    per_page = max(min(int(per_page or 25), 100), 1)
    offset = (page - 1) * per_page
    conn = db()
    where, params = _search_clause(search)
    rows = conn.execute(
        f'''SELECT files.*, users.first_name, users.username, users.phone
            FROM files
            LEFT JOIN users ON users.telegram_id=files.telegram_id
            {where}
            ORDER BY files.created_at DESC
            LIMIT ? OFFSET ?''',
        [*params, per_page, offset],
    ).fetchall()
    conn.close()
    return rows


def file_stats():
    conn = db()
    total = conn.execute('SELECT COUNT(*) FROM files').fetchone()[0]
    success = conn.execute("SELECT COUNT(*) FROM files WHERE status='success'").fetchone()[0]
    failed = conn.execute("SELECT COUNT(*) FROM files WHERE status='failed'").fetchone()[0]
    conn.close()
    return total, success, failed
