import os
import sqlite3
from datetime import datetime

from backend.config import config


def _db_path_from_url(url):
    if url.startswith("sqlite:///"):
        path = url.replace("sqlite:///", "", 1)
    else:
        path = url

    if not os.path.isabs(path):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        path = os.path.join(root, path)
    return path


def _current_db_path():
    return _db_path_from_url(os.getenv("KMS_DB_URL", config.DB_URL))


def get_connection():
    path = _current_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS knowledge_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def _row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "tags": [tag for tag in row["tags"].split(",") if tag],
        "source": row["source"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def create_entry(payload):
    now = datetime.utcnow().isoformat() + "Z"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO knowledge_entries (title, content, tags, source, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["title"],
            payload["content"],
            ",".join(payload.get("tags", [])),
            payload.get("source", "manual"),
            payload.get("status", "active"),
            now,
            now,
        ),
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return get_entry(entry_id)


def get_entry(entry_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knowledge_entries WHERE id = ?", (entry_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return _row_to_dict(row)


def update_entry(entry_id, payload):
    now = datetime.utcnow().isoformat() + "Z"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE knowledge_entries
        SET title = ?, content = ?, tags = ?, source = ?, status = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            payload["title"],
            payload["content"],
            ",".join(payload.get("tags", [])),
            payload.get("source", "manual"),
            payload.get("status", "active"),
            now,
            entry_id,
        ),
    )
    conn.commit()
    conn.close()
    return get_entry(entry_id)


def delete_entry(entry_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM knowledge_entries WHERE id = ?", (entry_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def list_entries(query=None, tag=None, limit=20, offset=0):
    conn = get_connection()
    cursor = conn.cursor()

    filters = []
    params = []
    if query:
        like_query = f"%{query}%"
        filters.append("(title LIKE ? OR content LIKE ?)")
        params.extend([like_query, like_query])
    if tag:
        filters.append("tags LIKE ?")
        params.append(f"%{tag}%")

    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    cursor.execute(f"SELECT COUNT(*) FROM knowledge_entries {where_clause}", params)
    total = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT * FROM knowledge_entries {where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?",
        params + [limit, offset],
    )
    rows = cursor.fetchall()
    conn.close()

    return total, [_row_to_dict(row) for row in rows]
