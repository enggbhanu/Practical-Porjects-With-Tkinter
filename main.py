'''
Author : Bhanu Pratap Singh
Date : 15-05-2023
'''

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox as msg


class BaseWindow:
    def __init__(self, title="GUI"):
        self.base_win = tk.Tk()
        # self.title = tk.StringVar()
        self.status_var = tk.StringVar()

        # self.title.set(title)
        self.base_win.title(title)

        self.status_var.set("Ready ..")
        self.create_base_window()

        self.frm_main = ttk.Frame(self.base_win)
        self.frm_main.grid(column=0, row=0)

        self.scrl_output_widget = scrolledtext.ScrolledText(self.base_win, wrap=tk.WORD)
        self.scrl_output_widget.grid(column=0, row=1, sticky='we')

        self.status_bar = ttk.Label(self.base_win, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(column=0, row=3, sticky='we')

    def create_base_window(self):
        pass


if __name__ == '__main__':
    base_window = BaseWindow("TEST GUI")
    base_window.base_win.mainloop()
