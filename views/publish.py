import tkinter as tk
from tkinter import filedialog, messagebox
from models.story import Story
from utils.media import save_media
import os
from tkinter import ttk

class PublishFrame(tk.Frame):
    def __init__(self, master, app=None):
        super().__init__(master)
        self.app = app
        self.create_widgets()
        self.media_path = None

    def create_widgets(self):
        form_frame = tk.Frame(self, bg='#f7efe5')
        form_frame.pack(pady=10)
        # Title
        tk.Label(form_frame, text='Title:', bg='#f7efe5', font=self.app.custom_font, anchor='w', width=15).grid(row=0, column=0, sticky='w', pady=2)
        self.title_entry = tk.Entry(form_frame, width=60, font=self.app.custom_font)
        self.title_entry.grid(row=0, column=1, pady=2, sticky='w')
        # Genre
        tk.Label(form_frame, text='Genre/Theme:', bg='#f7efe5', font=self.app.custom_font, anchor='w', width=15).grid(row=1, column=0, sticky='w', pady=2)
        self.genre_var = tk.StringVar()
        self.genre_combobox = ttk.Combobox(form_frame, textvariable=self.genre_var, state='readonly')
        genre_list = [
            'Fantasy', 'Science Fiction', 'Romance', 'Mystery', 'Thriller', 'Drama',
            'Adventure', 'Horror', 'Historical', 'Comedy', 'Action', 'Slice of Life',
            'Supernatural', 'Crime'
        ]
        self.genre_combobox['values'] = genre_list
        self.genre_combobox.set('')
        self.genre_combobox.grid(row=1, column=1, pady=2, sticky='w')
        # Content
        tk.Label(form_frame, text='Content:', bg='#f7efe5', font=self.app.custom_font, anchor='nw', width=15).grid(row=2, column=0, sticky='nw', pady=2)
        self.content_text = tk.Text(form_frame, width=70, height=15, font=self.app.custom_font)
        self.content_text.grid(row=2, column=1, pady=2, sticky='w')
        # Attach image and submit buttons
        tk.Button(self, text='Attach Image', command=self.attach_media, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font).pack(pady=5)
        self.media_label = tk.Label(self, text='No image attached', bg='#f7efe5', font=self.app.custom_font)
        self.media_label.pack()
        tk.Button(self, text='Submit Story', command=self.submit_story, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font).pack(pady=10)

    def refresh_genres(self):
        # No longer needed, but keep for compatibility
        pass

    def attach_media(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif')])
        if file_path:
            dest = save_media(file_path, os.path.join(os.getcwd(), 'assets'))
            self.media_path = dest
            self.media_label.config(text=f'Attached: {os.path.basename(dest)}')

    def submit_story(self):
        title = self.title_entry.get().strip()
        genre = self.genre_var.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        if not title or not content:
            messagebox.showerror('Error', 'Title and content are required.')
            return
        Story.create(title, content, genre, self.media_path)
        messagebox.showinfo('Success', 'Story submitted for review!')
        self.title_entry.delete(0, tk.END)
        self.genre_combobox.set('')
        self.content_text.delete('1.0', tk.END)
        self.media_label.config(text='No image attached')
        self.media_path = None
