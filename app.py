import sqlite3
import re
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

DATABASE_PATH = Path(__file__).resolve().parent / "users.db"


def get_database_info():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]

        return user_count, columns

    finally:
        connection.close()


def secure_login(username, password):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        return cursor.fetchone()

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


@app.route("/", methods=["GET", "POST"])
def dashboard():
    login_message = None
    detection_message = None
    detection_status = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "login":
            username = request.form.get("username", "")
            password = request.form.get("password", "")

            if secure_login(username, password):
                login_message = "Login successful!"
            else:
                login_message = "Login failed! Invalid credentials."

        elif action == "detect":
            user_input = request.form.get("sample_input", "")

            if detect_sql_injection(user_input):
                detection_message = "Suspicious SQL injection pattern detected."
                detection_status = "warning"
            else:
                detection_message = "No suspicious pattern detected by these rules."
                detection_status = "safe"

    try:
        user_count, columns = get_database_info()
        database_status = "Connected"
    except sqlite3.Error:
        user_count = 0
        columns = []
        database_status = "Unavailable"

    return render_template(
        "dashboard.html",
        database_status=database_status,
        user_count=user_count,
        columns=columns,
        login_message=login_message,
        detection_message=detection_message,
        detection_status=detection_status,
    )


if __name__ == "__main__":
    app.run(debug=False)