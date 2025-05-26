import sqlite3
from db.database import get_connection

class Story:
    @staticmethod
    def create(title, content, genre, media_path=None):
        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO stories (title, content, genre, media_path) VALUES (?, ?, ?, ?)',
                  (title, content, genre, media_path))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all(approved_only=True):
        conn = get_connection()
        c = conn.cursor()
        if approved_only:
            c.execute('SELECT * FROM stories WHERE is_approved=1 ORDER BY created_at DESC')
        else:
            c.execute('SELECT * FROM stories ORDER BY created_at DESC')
        stories = c.fetchall()
        conn.close()
        return stories

    @staticmethod
    def get_all_admin(filter_val='all'):
        conn = get_connection()
        c = conn.cursor()
        if filter_val == 'unapproved':
            c.execute('SELECT * FROM stories WHERE is_approved=0 ORDER BY created_at DESC')
        elif filter_val == 'approved':
            c.execute('SELECT * FROM stories WHERE is_approved=1 ORDER BY created_at DESC')
        else:
            c.execute('SELECT * FROM stories ORDER BY is_approved ASC, created_at DESC')
        stories = c.fetchall()
        conn.close()
        return stories

    @staticmethod
    def get_by_id(story_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM stories WHERE id=?', (story_id,))
        story = c.fetchone()
        conn.close()
        return story

    @staticmethod
    def search(keyword, genre=None):
        conn = get_connection()
        c = conn.cursor()
        query = 'SELECT * FROM stories WHERE is_approved=1 AND (title LIKE ? OR content LIKE ?)' 
        params = [f'%{keyword}%', f'%{keyword}%']
        if genre:
            query += ' AND genre=?'
            params.append(genre)
        c.execute(query, params)
        results = c.fetchall()
        conn.close()
        return results

    @staticmethod
    def approve(story_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute('UPDATE stories SET is_approved=1 WHERE id=?', (story_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(story_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute('DELETE FROM stories WHERE id=?', (story_id,))
        conn.commit()
        conn.close()
