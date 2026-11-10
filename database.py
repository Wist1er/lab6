import sqlite3
from pathlib import Path


def connect(db_path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: str | Path) -> None:
    with connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def list_items(db_path: str | Path) -> list[dict]:
    with connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, name, quantity FROM items ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def create_item(db_path: str | Path, name: str, quantity: int) -> dict:
    with connect(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO items (name, quantity) VALUES (?, ?)",
            (name, quantity),
        )
        item_id = cursor.lastrowid

    return get_item(db_path, item_id)


def get_item(db_path: str | Path, item_id: int) -> dict | None:
    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT id, name, quantity FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()
    return dict(row) if row else None


def update_item(
    db_path: str | Path,
    item_id: int,
    name: str,
    quantity: int,
) -> dict | None:
    with connect(db_path) as connection:
        cursor = connection.execute(
            "UPDATE items SET name = ?, quantity = ? WHERE id = ?",
            (name, quantity, item_id),
        )
        if cursor.rowcount == 0:
            return None

    return get_item(db_path, item_id)


def delete_item(db_path: str | Path, item_id: int) -> bool:
    with connect(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM items WHERE id = ?",
            (item_id,),
        )
        return cursor.rowcount > 0
