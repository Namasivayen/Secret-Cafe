import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os
from views.publish import PublishFrame
from views.discover import DiscoverFrame
from views.admin import AdminFrame

class SecretCafeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Secret Cafe - Story Sharing Platform')
        self.geometry('900x600')
        self.configure(bg='#f7efe5')  # Soft cafe background
        self.frames = {}
        self.custom_font = tkfont.Font(family='Segoe UI', size=12)
        self.header_font = tkfont.Font(family='Segoe UI', size=22, weight='bold')
        self.menu_bg = '#a47149'
        self.menu_fg = '#fff'
        self.button_bg = '#d9b08c'
        self.button_fg = '#4b3832'
        self.create_banner()
        # Add a content frame for all main app frames
        self.content_frame = tk.Frame(self, bg='#f7efe5')
        self.content_frame.pack(fill='both', expand=True)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.create_menu()
        self.show_frame('Discover')

    def create_banner(self):
        try:
            banner_path = os.path.join(os.path.dirname(__file__), 'assets', 'banner.png')
            if os.path.exists(banner_path):
                img = Image.open(banner_path)
                img = img.resize((900, 100))
                self.banner_img = ImageTk.PhotoImage(img)
                banner = tk.Label(self, image=self.banner_img, bg='#f7efe5')
                banner.pack(side='top', fill='x')
            else:
                tk.Label(self, text='☕ Secret Cafe ☕', font=self.header_font, bg='#f7efe5', fg='#a47149').pack(side='top', pady=10)
        except Exception:
            tk.Label(self, text='☕ Secret Cafe ☕', font=self.header_font, bg='#f7efe5', fg='#a47149').pack(side='top', pady=10)

    def create_menu(self):
        menubar = tk.Menu(self, bg=self.menu_bg, fg=self.menu_fg, activebackground='#c97b63', activeforeground='#fff')
        self.config(menu=menubar)
        menubar.add_command(label='Discover', command=lambda: self.show_frame('Discover'))
        menubar.add_command(label='Publish', command=lambda: self.show_frame('Publish'))
        menubar.add_command(label='Admin', command=lambda: self.show_frame('Admin'))

    def show_frame(self, name):
        frame_classes = {
            'Publish': PublishFrame,
            'Discover': DiscoverFrame,
            'Admin': AdminFrame
        }
        if name in self.frames:
            self.frames[name].tkraise()
        else:
            frame = frame_classes[name](self.content_frame, app=self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[name] = frame
            frame.tkraise()
        # Ensure the frame expands dynamically
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

if __name__ == '__main__':
    app = SecretCafeApp()
    app.mainloop()
