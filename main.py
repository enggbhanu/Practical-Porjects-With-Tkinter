'''
Author : Bhanu Pratap Singh
Example shows extending BaseWindow class to add new widget to GUI also test simple blocking non-blocking call
'''
import time
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox as msg
from utils.subproccess_manager import ProcessManager


class BaseWindow:
    def __init__(self, title="GUI"):
        self.base_win = tk.Tk()
        # self.title = tk.StringVar()
        self.status_var = tk.StringVar()

        # self.title.set(title)
        self.base_win.title(title)
        # for i in range(2):
        self.base_win.columnconfigure(0, weight=1, minsize=40)
        self.status_var.set("Ready ..")

        self.frm_main = ttk.Frame(self.base_win)
        self.frm_main.grid(column=0, row=0)

        self.scrl_output_widget = scrolledtext.ScrolledText(self.base_win, wrap=tk.WORD)
        self.scrl_output_widget.grid(column=0, row=1, sticky='we')

        self.status_bar = ttk.Label(self.base_win, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(column=0, row=2, sticky='we')


class ProcessTest(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frm_button_blocking = tk.Button(self.frm_main, text="Blocking Call", command=self.cb_blocking)
        self.frm_button_blocking.grid(column=0, row=0, sticky='w')

        self.frm_button_nonblocking = tk.Button(self.frm_main, text="Non-blocking Call", command=self.cb_nonblocking)
        self.frm_button_nonblocking.grid(column=1, row=0, sticky='e')

    def cb_blocking(self):
        cmd = 'cat file.txt'
        self.status_var.set('Busy..')
        cmd_handle = ProcessManager(cmd, self.status_var, self.scrl_output_widget, blocking=True, dbg=True)
        cmd_handle.run()

    def cb_nonblocking(self):
        cmd = 'cat file.txt'
        self.status_var.set('Busy..')
        cmd_handle = ProcessManager(cmd, self.status_var, self.scrl_output_widget, dbg=True)
        cmd_handle.run()


if __name__ == '__main__':
    base_window = ProcessTest('Test GUI')
    base_window.base_win.mainloop()
