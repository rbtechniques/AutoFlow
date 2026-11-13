
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

        # Create workflows table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT NOT NULL
            )
        """)

        # Create history table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                files_moved INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def add_history(action, details, files_moved=0):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO history (action, details, files_moved)
            VALUES (?, ?, ?)
            """,
            (action, details, files_moved)
        )


def get_history():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM history ORDER BY id DESC"
        ).fetchall()

    return [dict(row) for row in rows]
