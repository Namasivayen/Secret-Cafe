import sqlite3
from db.database import get_connection

class Feedback:
    @staticmethod
    def add(story_id, comment):
        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO feedback (story_id, comment) VALUES (?, ?)', (story_id, comment))
        conn.commit()
        conn.close()

    @staticmethod
    def get_for_story(story_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM feedback WHERE story_id=? ORDER BY created_at DESC', (story_id,))
        feedbacks = c.fetchall()
        conn.close()
        return feedbacks
