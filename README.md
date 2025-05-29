# Secret Cafe ☕

A beautiful desktop story-sharing platform built with Python and Tkinter. Share your stories anonymously, discover others' tales, and manage content with an admin panel.

## Features
- **Discover Stories:** Browse, search, and filter stories by genre or keyword.
- **Publish:** Submit your own stories with optional image attachments.
- **Comment:** Leave feedback on stories.
- **Admin Panel:** Approve or delete stories (admin login required).

## Installation
1. **Clone the repository:**
   ```
   git clone <repo-url>
   cd Secret-Cafe
   ```
2. **Install dependencies:**
   - Python 3.10+
   - [Pillow](https://pypi.org/project/Pillow/)
   ```
   pip install Pillow
   ```
3. **Run the app:**
   ```
   python main.py
   ```

## Usage
- **Discover:** Browse and search for stories.
- **Publish:** Click 'Publish' to submit a new story.
- **Admin:** Click 'Admin' and log in to approve or delete stories.

### Admin Login
- **Username:** Namasi
- **Password:** Namasi

## Project Structure
- `main.py` — Main application entry point
- `views/` — UI frames (Discover, Publish, Admin)
- `models/` — Database models (Story, User, Feedback)
- `db/` — SQLite database and initialization
- `assets/` — Images and media
- `utils/` — Utility functions

---
Enjoy sharing and discovering stories at the Secret Cafe!
