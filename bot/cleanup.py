import asyncio
from datetime import datetime, timezone
from pathlib import Path
from database.core import db
from config.settings import pending_retention_hours


def cleanup_old_pending_files():
    cutoff = datetime.now(timezone.utc).timestamp() - pending_retention_hours()*3600
    conn=db(); rows=conn.execute('SELECT id,path,created_at FROM pending_files').fetchall()
    count=0
    for row in rows:
        try:
            created=datetime.fromisoformat(row['created_at'].replace('Z','+00:00'))
            if created.timestamp() < cutoff:
                Path(row['path']).unlink(missing_ok=True)
                conn.execute('DELETE FROM pending_files WHERE id=?',(row['id'],)); count+=1
        except Exception:
            pass
    conn.commit(); conn.close()
    return count


async def cleanup_loop():
    while True:
        try:
            count=cleanup_old_pending_files()
            if count: print(f'Cleanup removed {count} expired pending files')
        except Exception:
            pass
        await asyncio.sleep(600)
