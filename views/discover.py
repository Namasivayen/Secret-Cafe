import tkinter as tk
from tkinter import ttk, messagebox
from models.story import Story

class DiscoverFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.load_stories()

    def create_widgets(self):
        tk.Label(self, text='Discover Stories', font=('Arial', 18)).pack(pady=10)
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text='Search:').pack(side='left')
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left')
        tk.Label(search_frame, text='Genre:').pack(side='left')
        self.genre_entry = tk.Entry(search_frame, width=15)
        self.genre_entry.pack(side='left')
        tk.Button(search_frame, text='Go', command=self.search_stories).pack(side='left', padx=5)
        tk.Button(search_frame, text='Random', command=self.random_story).pack(side='left')
        self.tree = ttk.Treeview(self, columns=('Title', 'Genre', 'Date'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Date', text='Date')
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', self.on_story_select)

    def load_stories(self, stories=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if stories is None:
            stories = Story.get_all()
        for s in stories:
            self.tree.insert('', 'end', iid=s[0], values=(s[1], s[3], s[5]))

    def search_stories(self):
        keyword = self.search_entry.get().strip()
        genre = self.genre_entry.get().strip()
        results = Story.search(keyword, genre if genre else None)
        self.load_stories(results)

    def random_story(self):
        import random
        stories = Story.get_all()
        if stories:
            s = random.choice(stories)
            self.show_story_popup(s)

    def on_story_select(self, event):
        item = self.tree.selection()
        if item:
            story_id = int(item[0])
            story = Story.get_by_id(story_id)
            self.show_story_popup(story)

    def show_story_popup(self, story):
        popup = tk.Toplevel(self)
        popup.title(story[1])
        tk.Label(popup, text=f'Genre: {story[3]}', font=('Arial', 10)).pack()
        tk.Label(popup, text=story[2], wraplength=400, justify='left').pack(pady=10)
        if story[4]:
            try:
                from PIL import Image, ImageTk
                img = Image.open(story[4])
                img.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(popup, image=photo)
                img_label.image = photo
                img_label.pack()
            except Exception:
                tk.Label(popup, text='[Image could not be loaded]').pack()
        tk.Label(popup, text=f'Date: {story[5]}').pack()
