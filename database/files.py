from database.core import db


def list_files():
    conn = db()
    rows = conn.execute('''SELECT files.*, users.first_name, users.username, users.phone
                          FROM files LEFT JOIN users ON users.telegram_id=files.telegram_id
                          ORDER BY files.created_at DESC''').fetchall()
    conn.close(); return rows


def file_stats():
    conn = db()
    total = conn.execute('SELECT COUNT(*) FROM files').fetchone()[0]
    success = conn.execute("SELECT COUNT(*) FROM files WHERE status='success'").fetchone()[0]
    failed = conn.execute("SELECT COUNT(*) FROM files WHERE status='failed'").fetchone()[0]
    conn.close(); return total, success, failed
