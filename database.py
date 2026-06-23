import sqlite3

DB_NAME = "chat.db"


import os
print("DATABASE FILE:", os.path.abspath(DB_NAME))


def init_db():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        role TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_chat(title):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO chats(title) VALUES(?)",
        (title,)
    )

    conn.commit()
    conn.close()


def get_chats():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "SELECT id,title FROM chats ORDER BY id DESC"
    )

    rows = c.fetchall()

    conn.close()

    return rows


def save_message(chat_id, role, content):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO messages(
            chat_id,
            role,
            content
        )
        VALUES(?,?,?)
        """,
        (chat_id, role, content)
    )

    conn.commit()
    conn.close()


def get_messages(chat_id):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        SELECT role,content
        FROM messages
        WHERE chat_id=?
        ORDER BY id
        """,
        (chat_id,)
    )

    rows = c.fetchall()

    conn.close()

    return rows


def delete_chat(chat_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    print("========== DELETE DEBUG ==========")
    print("Deleting chat id:", chat_id)

    cur.execute(
        "DELETE FROM messages WHERE chat_id=?",
        (chat_id,)
    )
    print("Messages deleted:", cur.rowcount)

    cur.execute(
        "DELETE FROM chats WHERE id=?",
        (chat_id,)
    )
    print("Chats deleted:", cur.rowcount)

    conn.commit()

    cur.execute("SELECT id,title FROM chats")
    print("Remaining chats:", cur.fetchall())

    conn.close()
def rename_chat(chat_id, new_title):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        """
        UPDATE chats
        SET title=?
        WHERE id=?
        """,
        (new_title, chat_id)
    )



    conn.commit()
    conn.close()