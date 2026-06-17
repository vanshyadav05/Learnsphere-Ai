import sqlite3

def create_table():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, content):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (role, content) VALUES (?, ?)",
        (role, content)
    )

    conn.commit()
    conn.close()


def load_messages():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT role, content FROM chats")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"role": row[0], "content": row[1]}
        for row in rows
    ]


def clear_messages():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chats")

    conn.commit()
    conn.close()