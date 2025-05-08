import sqlite3
import os
import getpass

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
    # Create an initial admin user if not exists
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from models.user import User
    from models.story import Story
    username = input('Enter admin username: ')
    password = getpass.getpass('Enter admin password: ')
    try:
        User.create(username, password, is_admin=1)
        print(f'Admin user "{username}" created successfully.')
    except Exception as e:
        print(f'Error creating admin user: {e}')

    # Seed demo stories
    try:
        Story.create(
            title='A Night at Secret Cafe',
            content='It was a rainy night when I stumbled upon the Secret Cafe. The aroma of coffee and the sound of jazz welcomed me inside...',
            genre='Slice of Life',
            media_path=None
        )
        Story.create(
            title='The Lost Letter',
            content='Hidden behind the old bookshelf, I found a letter addressed to no one. Its words changed my life forever.',
            genre='Mystery',
            media_path=None
        )
        Story.create(
            title='Whispers in the Dark',
            content='They say the Secret Cafe is haunted. Last night, I heard the whispers myself...',
            genre='Horror',
            media_path=None
        )
        Story.create(
            title='Espresso Dreams',
            content='Every cup of coffee at the Secret Cafe brings a new dream. Some are sweet, some are nightmares.',
            genre='Fantasy',
            media_path=None
        )
        print('Demo stories seeded successfully.')
    except Exception as e:
        print(f'Error seeding demo stories: {e}')

    # Approve all seeded stories
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('UPDATE stories SET is_approved=1')
        conn.commit()
        conn.close()
        print('All demo stories approved.')
    except Exception as e:
        print(f'Error approving demo stories: {e}')
