# SQL Context for Secret Cafe

## Tables

### users
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `username` (TEXT, UNIQUE)
- `password_hash` (TEXT)
- `is_admin` (INTEGER, DEFAULT 0)

### stories
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `title` (TEXT, NOT NULL)
- `content` (TEXT, NOT NULL)
- `genre` (TEXT)
- `media_path` (TEXT)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `is_approved` (INTEGER, DEFAULT 0)
- `is_deleted` (INTEGER, DEFAULT 0)

### feedback
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `story_id` (INTEGER, FOREIGN KEY to stories.id)
- `comment` (TEXT, NOT NULL)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

## Table Structures

### users
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT,
    is_admin INTEGER DEFAULT 0
);
```

### stories
```sql
CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    genre TEXT,
    media_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_approved INTEGER DEFAULT 0,
    is_deleted INTEGER DEFAULT 0
);
```

### feedback
```sql
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story_id INTEGER,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(story_id) REFERENCES stories(id)
);
```

---

## SQL Queries

### User Queries
- **Create User:**
  ```sql
  INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?);
  ```
- **Authenticate User:**
  ```sql
  SELECT password_hash, is_admin FROM users WHERE username=?;
  ```

### Story Queries
- **Create Story:**
  ```sql
  INSERT INTO stories (title, content, genre, media_path) VALUES (?, ?, ?, ?);
  ```
- **Get All Stories (approved only):**
  ```sql
  SELECT * FROM stories WHERE is_approved=1 ORDER BY created_at DESC;
  ```
- **Get All Stories (admin):**
  ```sql
  SELECT * FROM stories ORDER BY is_approved ASC, created_at DESC;
  SELECT * FROM stories WHERE is_approved=0 ORDER BY created_at DESC;
  SELECT * FROM stories WHERE is_approved=1 ORDER BY created_at DESC;
  ```
- **Get Story by ID:**
  ```sql
  SELECT * FROM stories WHERE id=?;
  ```
- **Search Stories:**
  ```sql
  SELECT * FROM stories WHERE is_approved=1 AND (title LIKE ? OR content LIKE ?);
  SELECT * FROM stories WHERE is_approved=1 AND (title LIKE ? OR content LIKE ?) AND genre=?;
  ```
- **Approve Story:**
  ```sql
  UPDATE stories SET is_approved=1 WHERE id=?;
  ```
- **Delete Story:**
  ```sql
  DELETE FROM stories WHERE id=?;
  ```

### Feedback Queries
- **Add Feedback:**
  ```sql
  INSERT INTO feedback (story_id, comment) VALUES (?, ?);
  ```
- **Get Feedback for Story:**
  ```sql
  SELECT * FROM feedback WHERE story_id=? ORDER BY created_at DESC;
  ```
