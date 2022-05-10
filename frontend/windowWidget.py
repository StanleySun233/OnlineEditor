import tkinter as tk

import fun


class WindowWidget:
    def __init__(self, width, height, name):
        fun.logFormat(fun.INFO, f'打开{name}')
        self.window = tk.Tk()
        self.width = 400
        self.height = 300
        self.window.geometry(
            f'{width}x{height}+{round((self.window.winfo_screenwidth() - width) / 2)}+{round((self.window.winfo_height() - height) / 2)}')
        self.window.title(name)
        self.window.resizable(False, False)
