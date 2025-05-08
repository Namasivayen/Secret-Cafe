import tkinter as tk
from tkinter import ttk, messagebox
from models.story import Story
from models.feedback import Feedback

class InteractFrame(tk.Frame):
    def __init__(self, master, app=None):
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()
        self.load_stories()

    def create_widgets(self):
        tk.Label(self, text='Interact with Stories', font=self.app.header_font, bg='#f7efe5', fg='#a47149').pack(pady=10)
        self.tree = ttk.Treeview(self, columns=('Title', 'Genre', 'Date'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Date', text='Date')
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', self.on_story_select)

    def load_stories(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        stories = Story.get_all()
        for s in stories:
            self.tree.insert('', 'end', iid=s[0], values=(s[1], s[3], s[5]))

    def on_story_select(self, event):
        item = self.tree.selection()
        if item:
            story_id = int(item[0])
            story = Story.get_by_id(story_id)
            self.show_feedback_popup(story)

    def show_feedback_popup(self, story):
        popup = tk.Toplevel(self)
        popup.title(f'Feedback for: {story[1]}')
        tk.Label(popup, text=story[2], wraplength=400, justify='left').pack(pady=10)
        feedbacks = Feedback.get_for_story(story[0])
        fb_frame = tk.Frame(popup)
        fb_frame.pack(pady=5)
        tk.Label(fb_frame, text='Comments:').pack(anchor='w')
        for fb in feedbacks:
            tk.Label(fb_frame, text=f'- {fb[2]} ({fb[3]})', wraplength=350, justify='left').pack(anchor='w')
        tk.Label(popup, text='Leave a comment:').pack(anchor='w', pady=(10,0))
        comment_entry = tk.Entry(popup, width=50)
        comment_entry.pack()
        def submit_comment():
            comment = comment_entry.get().strip()
            if comment:
                Feedback.add(story[0], comment)
                messagebox.showinfo('Success', 'Comment added!')
                popup.destroy()
        tk.Button(popup, text='Submit', command=submit_comment).pack(pady=5)
