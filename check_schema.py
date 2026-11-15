
import sqlite3

from database.connection import get_connection
from database.schema import create_tables


def test_tables_created():

    create_tables()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tables = cursor.fetchall()

    table_names = [row["name"] for row in tables]

    print("Tables found:", table_names)

    assert "runs" in table_names
    assert "evaluation_logs" in table_names
    assert "learning_memory" in table_names

    connection.close()

    print("All three tables verified!")


if __name__ == "__main__":

    test_tables_created()
