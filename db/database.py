import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'secret_cafe.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Users table (for admin, optional for users)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        is_admin INTEGER DEFAULT 0
    )''')
    # Stories table
    c.execute('''CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        genre TEXT,
        media_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_approved INTEGER DEFAULT 0
    )''')
    # Feedback table
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_id INTEGER,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(story_id) REFERENCES stories(id)
    )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
