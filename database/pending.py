from pathlib import Path
from database.core import db, now_iso


def pending_total(telegram_id):
    conn = db(); row = conn.execute('SELECT COUNT(*) AS count, COALESCE(SUM(size_bytes),0) AS total FROM pending_files WHERE telegram_id=?', (telegram_id,)).fetchone(); conn.close(); return row['count'], row['total']


def get_pending_files(telegram_id):
    conn = db(); rows = conn.execute('SELECT * FROM pending_files WHERE telegram_id=? ORDER BY id ASC', (telegram_id,)).fetchall(); conn.close(); return rows


def add_pending_file(telegram_id, filename, path, size_bytes):
    conn = db(); cur = conn.execute('INSERT INTO pending_files(telegram_id,filename,path,size_bytes,created_at) VALUES(?,?,?,?,?)', (telegram_id,filename,path,size_bytes,now_iso())); conn.commit(); conn.close(); return cur.lastrowid


def clear_pending_files(telegram_id):
    conn = db(); rows = conn.execute('SELECT path FROM pending_files WHERE telegram_id=?', (telegram_id,)).fetchall(); conn.execute('DELETE FROM pending_files WHERE telegram_id=?', (telegram_id,)); conn.commit(); conn.close()
    for row in rows:
        try: Path(row['path']).unlink(missing_ok=True)
        except Exception: pass


def delete_pending_file(file_id, telegram_id):
    conn = db(); row = conn.execute('SELECT path FROM pending_files WHERE id=? AND telegram_id=?', (file_id,telegram_id)).fetchone(); conn.execute('DELETE FROM pending_files WHERE id=? AND telegram_id=?', (file_id,telegram_id)); conn.commit(); conn.close()
    if row:
        try: Path(row['path']).unlink(missing_ok=True)
        except Exception: pass


def create_file_record(telegram_id, filename, subject, size_bytes, status, error=None):
    conn = db(); cur = conn.execute('INSERT INTO files(telegram_id,filename,subject,size_bytes,status,error,created_at) VALUES(?,?,?,?,?,?,?)', (telegram_id,filename,subject,size_bytes,status,error,now_iso())); conn.commit(); conn.close(); return cur.lastrowid
