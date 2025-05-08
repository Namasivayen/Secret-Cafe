import sqlite3
from db.database import get_connection
from utils.hashing import hash_password, check_password

class User:
    @staticmethod
    def create(username, password, is_admin=0):
        conn = get_connection()
        c = conn.cursor()
        password_hash = hash_password(password)
        c.execute('INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
                  (username, password_hash, is_admin))
        conn.commit()
        conn.close()

    @staticmethod
    def authenticate(username, password):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT password_hash, is_admin FROM users WHERE username=?', (username,))
        row = c.fetchone()
        conn.close()
        if row and check_password(password, row[0]):
            return True, bool(row[1])
        return False, False
