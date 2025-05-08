import tkinter as tk
from views.publish import PublishFrame
from views.discover import DiscoverFrame
from views.interact import InteractFrame
from views.admin import AdminFrame

class SecretCafeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Secret Cafe - Story Sharing Platform')
        self.geometry('900x600')
        self.frames = {}
        self.create_menu()
        self.show_frame('Discover')

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        menubar.add_command(label='Discover', command=lambda: self.show_frame('Discover'))
        menubar.add_command(label='Publish', command=lambda: self.show_frame('Publish'))
        menubar.add_command(label='Interact', command=lambda: self.show_frame('Interact'))
        menubar.add_command(label='Admin', command=lambda: self.show_frame('Admin'))

    def show_frame(self, name):
        frame_classes = {
            'Publish': PublishFrame,
            'Discover': DiscoverFrame,
            'Interact': InteractFrame,
            'Admin': AdminFrame
        }
        if name in self.frames:
            self.frames[name].tkraise()
        else:
            frame = frame_classes[name](self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[name] = frame
            frame.tkraise()

if __name__ == '__main__':
    app = SecretCafeApp()
    app.mainloop()
