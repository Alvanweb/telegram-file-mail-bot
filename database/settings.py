from database.core import db, now_iso
from config.settings import DEFAULTS


def init_settings():
    conn = db()
    for key, value in DEFAULTS.items():
        conn.execute('INSERT OR IGNORE INTO settings(key,value,updated_at) VALUES(?,?,?)', (key, value, now_iso()))
    conn.commit()
    conn.close()


def get_setting(key, default=None):
    conn = db()
    row = conn.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
    conn.close()
    if row is None:
        return DEFAULTS.get(key, default)
    return row['value']


def set_setting(key, value):
    conn = db()
    conn.execute('''INSERT INTO settings(key,value,updated_at) VALUES(?,?,?)
                    ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at''',
                 (key, str(value), now_iso()))
    conn.commit()
    conn.close()


def all_settings():
    conn = db()
    rows = conn.execute('SELECT key,value,updated_at FROM settings ORDER BY key').fetchall()
    conn.close()
    return rows
