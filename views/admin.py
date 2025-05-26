import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.story import Story
from models.user import User

class AdminFrame(tk.Frame):
    def __init__(self, master, app=None):
        super().__init__(master)
        self.app = app
        self.is_authenticated = False
        self.create_widgets()

    def create_widgets(self):
        self.login_btn = tk.Button(self, text='Admin Login', command=self.admin_login, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font)
        self.login_btn.pack(pady=10)
        tk.Label(self, text='Admin Panel', font=self.app.header_font, bg='#f7efe5', fg='#a47149').pack(pady=5)
        # Filter options
        filter_frame = tk.Frame(self, bg='#f7efe5')
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text='Show:', bg='#f7efe5', font=self.app.custom_font).pack(side='left')
        self.filter_var = tk.StringVar(value='all')
        filter_options = [('All', 'all'), ('Unapproved', 'unapproved'), ('Approved', 'approved')]
        for text, val in filter_options:
            tk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=val, command=self.load_stories, bg='#f7efe5', font=self.app.custom_font).pack(side='left', padx=2)
        self.tree = ttk.Treeview(self, columns=('Title', 'Genre', 'Date', 'Approved'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Approved', text='Approved')
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', self.on_story_select)
        self.refresh_btn = tk.Button(self, text='Refresh', command=self.load_stories, bg=self.app.button_bg, fg=self.app.button_fg, font=self.app.custom_font)
        self.refresh_btn.pack(pady=5)

    def admin_login(self):
        username = simpledialog.askstring('Admin Login', 'Username:')
        password = simpledialog.askstring('Admin Login', 'Password:', show='*')
        if username and password:
            ok, is_admin = User.authenticate(username, password)
            if ok and is_admin:
                self.is_authenticated = True
                messagebox.showinfo('Success', 'Admin login successful!')
                self.load_stories()
            else:
                messagebox.showerror('Error', 'Invalid admin credentials.')

    def load_stories(self):
        if not self.is_authenticated:
            messagebox.showerror('Error', 'Admin login required.')
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        filter_val = self.filter_var.get()
        stories = Story.get_all_admin(filter_val)
        # Unapproved stories at the top
        stories = sorted(stories, key=lambda s: (s[6] == 0), reverse=True)
        for s in stories:
            self.tree.insert('', 'end', iid=s[0], values=(s[1], s[3], s[5], 'Yes' if s[6] else 'No'))

    def on_story_select(self, event):
        if not self.is_authenticated:
            return
        item = self.tree.selection()
        if item:
            story_id = int(item[0])
            story = Story.get_by_id(story_id)
            self.show_admin_popup(story)

    def show_admin_popup(self, story):
        popup = tk.Toplevel(self)
        popup.title(f'Admin: {story[1]}')
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
        tk.Label(scrollable_frame, text=story[2], wraplength=400, justify='left').pack(pady=10)
        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=5)
        if not story[6]:
            tk.Button(btn_frame, text='Approve', command=lambda: self.approve_story(story[0], popup)).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Delete', command=lambda: self.delete_story(story[0], popup)).pack(side='left', padx=5)

    def approve_story(self, story_id, popup):
        Story.approve(story_id)
        messagebox.showinfo('Success', 'Story approved!')
        popup.destroy()
        self.load_stories()

    def delete_story(self, story_id, popup):
        Story.delete(story_id)
        messagebox.showinfo('Deleted', 'Story deleted!')
        popup.destroy()
        self.load_stories()
