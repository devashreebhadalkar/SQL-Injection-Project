import sqlite3
import re
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "users.db"


def secure_login_test(username, password):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        return cursor.fetchone() is not None

    finally:
        connection.close()


def detect_sql_injection(user_input):
    patterns = [
        r"\bOR\b\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?",
        r"--",
        r"\bUNION\b\s+\bSELECT\b",
        r";\s*(DROP|DELETE|UPDATE|INSERT)\b",
    ]

    return any(
        re.search(pattern, user_input, re.IGNORECASE)
        for pattern in patterns
    )


def run_test(description, condition):
    if condition:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description}")


def main():
    print("=== SQL INJECTION PROJECT: SECURITY TESTS ===\n")

    run_test(
        "Valid credentials are accepted",
        secure_login_test("student", "student123")
    )

    run_test(
        "Incorrect password is rejected",
        not secure_login_test("student", "wrongpassword")
    )

    run_test(
        "SQL injection input is rejected by secure login",
        not secure_login_test("' OR '1'='1' --", "anything")
    )

    run_test(
        "Suspicious SQL injection pattern is detected",
        detect_sql_injection("' OR '1'='1' --")
    )

    run_test(
        "Ordinary username is not flagged",
        not detect_sql_injection("student")
    )


if __name__ == "__main__":
    main()