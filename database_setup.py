import sqlite3
from pathlib import Path

# Get the project folder's location.
PROJECT_FOLDER = Path(__file__).resolve().parent

# Define the database file path.
DATABASE_PATH = PROJECT_FOLDER / "users.db"


def create_database():
    # Connect to the database.
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Create the users table.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Insert fictional test users.
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", "admin123")
    )

    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("student", "student123")
    )

    # Save database changes.
    connection.commit()

    # Display the users.
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()

    print("DATABASE CREATED SUCCESSFULLY!")
    print("\nUsers stored in the database:")

    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}")

    connection.close()


if __name__ == "__main__":
    create_database()