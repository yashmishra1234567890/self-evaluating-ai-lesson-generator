
from database.connection import get_connection, close_connection


def test_database_connection():

    connection = get_connection()

    print("Database connected successfully!")

    print("SQLite version:", connection.execute(
        "SELECT sqlite_version()"
    ).fetchone()[0])

    close_connection(connection)

    print("Connection closed successfully!")


if __name__ == "__main__":
    test_database_connection()
