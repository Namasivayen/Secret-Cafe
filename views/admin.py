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
        stories = Story.get_all(approved_only=False)
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
        tk.Label(popup, text=story[2], wraplength=400, justify='left').pack(pady=10)
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
