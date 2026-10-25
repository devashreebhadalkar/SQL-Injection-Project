import sqlite3
from pathlib import Path

# Locate the database inside the project folder.
DATABASE_PATH = Path(__file__).resolve().parent / "users.db"


def login(username, password):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # SECURE: Use parameterized SQL to separate input from the query.
    query = (
        "SELECT id, username FROM users "
        "WHERE username = ? AND password = ?"
    )

    print("\nSQL query template:")
    print(query)

    try:
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            print("\nLogin successful!")
            print("Welcome,", result[1])
        else:
            print("\nLogin failed! Invalid credentials.")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    finally:
        connection.close()


def main():
    print("=== SECURE LOGIN SYSTEM ===")

    username = input("Enter username: ")
    password = input("Enter password: ")

    login(username, password)


if __name__ == "__main__":
    main()