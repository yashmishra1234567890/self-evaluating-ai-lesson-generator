import sqlite3
from pathlib import Path

from config import get_settings


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.

    Returns:
        sqlite3.Connection: Active database connection.
    """

    settings = get_settings()

    # Get database path
    database_path = Path(settings.database_path)

    # Create parent directory if it does not exist
    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Establish database connection
    connection = sqlite3.connect(
        database_path,
        timeout=30
    )

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


def close_connection(connection: sqlite3.Connection) -> None:
    """
    Safely close an active database connection.
    """

    if connection:
        connection.close()
