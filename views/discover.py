import tkinter as tk
from tkinter import ttk, messagebox
from models.story import Story

class DiscoverFrame(tk.Frame):
    def __init__(self, master, app=None):
        super().__init__(master)
        self.app = app
        self.create_widgets()
        self.load_stories()

    def create_widgets(self):
        tk.Label(self, text='Discover Stories', font=self.app.header_font, bg='#f7efe5', fg='#a47149').pack(pady=10)
        search_frame = tk.Frame(self, bg='#f7efe5')
        search_frame.pack(pady=5)
        tk.Label(search_frame, text='Search:', bg='#f7efe5', font=self.app.custom_font).pack(side='left')
        self.search_entry = tk.Entry(search_frame, width=30, font=self.app.custom_font)
        self.search_entry.pack(side='left')
        tk.Label(search_frame, text='Genre:', bg='#f7efe5', font=self.app.custom_font).pack(side='left')
        # Genre dropdown (Combobox) with predefined genres
        self.genre_var = tk.StringVar()
        self.genre_combobox = ttk.Combobox(search_frame, textvariable=self.genre_var, state='readonly')
        genre_list = [
            'Fantasy', 'Science Fiction', 'Romance', 'Mystery', 'Thriller', 'Drama',
            'Adventure', 'Horror', 'Historical', 'Comedy', 'Action', 'Slice of Life',
            'Supernatural', 'Crime'
        ]
        self.genre_combobox['values'] = genre_list
        self.genre_combobox.set('')
        self.genre_combobox.pack(side='left')
        tk.Button(search_frame, text='Go', command=self.search_stories, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font).pack(side='left', padx=5)
        tk.Button(search_frame, text='Random', command=self.random_story, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font).pack(side='left')
        # Add Refresh button
        tk.Button(search_frame, text='Refresh', command=self.load_stories, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font).pack(side='left', padx=5)
        self.tree = ttk.Treeview(self, columns=('Title', 'Genre', 'Date'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Date', text='Date')
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', self.on_story_select)

    def refresh_genres(self):
        # No longer needed, but kept for compatibility
        pass

    def load_stories(self, stories=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if stories is None:
            stories = Story.get_all()
        for s in stories:
            self.tree.insert('', 'end', iid=s[0], values=(s[1], s[3], s[5]))

    def search_stories(self):
        keyword = self.search_entry.get().strip()
        genre = self.genre_var.get().strip() or None
        results = Story.search(keyword, genre)
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
        # Add a scrollable frame for the story content
        content_frame = tk.Frame(popup)
        content_frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(content_frame, width=450, height=350)
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        # Show title in block letters, bigger font
        tk.Label(scrollable_frame, text=story[1].upper(), font=('Segoe UI', 18, 'bold')).pack(pady=(10,0))
        tk.Label(scrollable_frame, text=f'Genre: {story[3]}', font=('Arial', 10)).pack()
        tk.Label(scrollable_frame, text=story[2], wraplength=400, justify='left').pack(pady=10)
        if story[4]:
            try:
                from PIL import Image, ImageTk
                img = Image.open(story[4])
                img.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(scrollable_frame, image=photo)
                img_label.image = photo
                img_label.pack()
            except Exception:
                tk.Label(scrollable_frame, text='[Image could not be loaded]').pack()
        tk.Label(scrollable_frame, text=f'Date: {story[5]}').pack()
        # --- Feedback Section ---
        from models.feedback import Feedback
        feedbacks = Feedback.get_for_story(story[0])
        fb_frame = tk.Frame(scrollable_frame)
        fb_frame.pack(pady=5, fill='x')
        tk.Label(fb_frame, text='Comments:', font=('Arial', 11, 'bold')).pack(anchor='w')
        for fb in feedbacks:
            tk.Label(fb_frame, text=f'- {fb[2]} ({fb[3]})', wraplength=350, justify='left').pack(anchor='w')
        tk.Label(scrollable_frame, text='Leave a comment:').pack(anchor='w', pady=(10,0))
        comment_entry = tk.Entry(scrollable_frame, width=50)
        comment_entry.pack()
        def submit_comment():
            comment = comment_entry.get().strip()
            if comment:
                Feedback.add(story[0], comment)
                messagebox.showinfo('Success', 'Comment added!')
                popup.destroy()
        tk.Button(scrollable_frame, text='Submit', command=submit_comment).pack(pady=5)
