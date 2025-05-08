import tkinter as tk
from tkinter import filedialog, messagebox
from models.story import Story
from utils.media import save_media
import os

class PublishFrame(tk.Frame):
    def __init__(self, master, app=None):
        super().__init__(master)
        self.app = app
        self.create_widgets()
        self.media_path = None

    def create_widgets(self):
        tk.Label(self, text='Submit Your Story', font=self.app.header_font, bg='#f7efe5', fg='#a47149').pack(pady=10)
        tk.Label(self, text='Title:', bg='#f7efe5', font=self.app.custom_font).pack(anchor='w')
        self.title_entry = tk.Entry(self, width=60, font=self.app.custom_font)
        self.title_entry.pack()
        tk.Label(self, text='Genre/Theme:', bg='#f7efe5', font=self.app.custom_font).pack(anchor='w')
        self.genre_entry = tk.Entry(self, width=40, font=self.app.custom_font)
        self.genre_entry.pack()
        tk.Label(self, text='Content:', bg='#f7efe5', font=self.app.custom_font).pack(anchor='w')
        self.content_text = tk.Text(self, width=70, height=15, font=self.app.custom_font)
        self.content_text.pack()
        tk.Button(self, text='Attach Image', command=self.attach_media, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font).pack(pady=5)
        self.media_label = tk.Label(self, text='No image attached', bg='#f7efe5', font=self.app.custom_font)
        self.media_label.pack()
        tk.Button(self, text='Submit Story', command=self.submit_story, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font).pack(pady=10)

    def attach_media(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif')])
        if file_path:
            dest = save_media(file_path, os.path.join(os.getcwd(), 'assets'))
            self.media_path = dest
            self.media_label.config(text=f'Attached: {os.path.basename(dest)}')

    def submit_story(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        if not title or not content:
            messagebox.showerror('Error', 'Title and content are required.')
            return
        Story.create(title, content, genre, self.media_path)
        messagebox.showinfo('Success', 'Story submitted for review!')
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)
        self.media_label.config(text='No image attached')
        self.media_path = None
