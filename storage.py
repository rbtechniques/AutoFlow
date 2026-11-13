
import sqlite3
import os

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "database",
    "autoflow.db"
)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT NOT NULL
            )
        """)


def add_workflow(name, description, workflow_type):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO workflows (name, description, type)
            VALUES (?, ?, ?)
            """,
            (name, description, workflow_type)
        )


def get_workflows():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM workflows ORDER BY id DESC"
        ).fetchall()

    return [dict(row) for row in rows]
