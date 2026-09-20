from database.core import db, now_iso


def get_user(telegram_id):
    conn = db(); row = conn.execute('SELECT * FROM users WHERE telegram_id=?', (telegram_id,)).fetchone(); conn.close(); return row


def register_user(telegram_id, first_name, username, phone):
    conn = db()
    conn.execute('''INSERT INTO users(telegram_id,first_name,username,phone,registered_at,active)
                    VALUES(?,?,?,?,?,1)
                    ON CONFLICT(telegram_id) DO UPDATE SET first_name=excluded.first_name, username=excluded.username, phone=excluded.phone''',
                 (telegram_id, first_name, username, phone, now_iso()))
    conn.commit(); conn.close()


def set_subject(telegram_id, subject):
    conn = db(); conn.execute('UPDATE users SET pending_subject=? WHERE telegram_id=?', (subject, telegram_id)); conn.commit(); conn.close()


def clear_subject(telegram_id):
    conn = db(); conn.execute('UPDATE users SET pending_subject=NULL WHERE telegram_id=?', (telegram_id,)); conn.commit(); conn.close()


def list_users():
    conn = db(); rows = conn.execute('SELECT * FROM users ORDER BY registered_at DESC').fetchall(); conn.close(); return rows


def toggle_user(telegram_id):
    conn = db(); conn.execute('UPDATE users SET active=CASE WHEN active=1 THEN 0 ELSE 1 END WHERE telegram_id=?', (telegram_id,)); conn.commit(); conn.close()


def delete_user(telegram_id):
    conn = db()
    pending = conn.execute('SELECT path FROM pending_files WHERE telegram_id=?', (telegram_id,)).fetchall()
    conn.execute('DELETE FROM pending_files WHERE telegram_id=?', (telegram_id,))
    conn.execute('DELETE FROM files WHERE telegram_id=?', (telegram_id,))
    conn.execute('DELETE FROM users WHERE telegram_id=?', (telegram_id,))
    conn.commit(); conn.close()
    return [row['path'] for row in pending]
