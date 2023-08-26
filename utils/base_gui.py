import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

'''
Module defines base GUI class, GUI tools that uses command line tools and designed to display shell activities/output
could be inherited from this class 
'''


class BaseWindow:
    def __init__(self, title="GUI"):
        self.base_win = tk.Tk()
        # self.title = tk.StringVar()
        self.status_var = tk.StringVar()

        # self.title.set(title)
        self.base_win.title(title)
        for row in range(1):
            self.base_win.rowconfigure(0, weight=1, minsize=40)
        for clm in range(1):
            self.base_win.columnconfigure(0, weight=1, minsize=40)
        self.status_var.set("Ready ..")

        self.frm_main = ttk.Frame(self.base_win)
        self.frm_main.grid(column=0, row=0)

        self.scrl_output_widget = scrolledtext.ScrolledText(self.base_win, wrap=tk.WORD)
        self.scrl_output_widget.grid(column=0, row=1, sticky='we')

        self.status_bar = ttk.Label(self.base_win, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(column=0, row=2, sticky='we')

    @staticmethod
    def add_checkbutton_cmd_options(max_col: int, checkbutton_attr_text: dict, checkbox_default_state: list,
                                     tk_frame: tk.Frame) -> dict:
        row_increment = max_col - 1
        option_dict = {}
        irow = 0
        idx = 0
        for option in checkbutton_attr_text.keys():
            icol = idx % max_col
            option_dict = tk.Checkbutton(tk_frame, text=option)
            # https://stackoverflow.com/questions/59797094/tkinter-checkbutton-not-updating-when-changing-variable
            # '.var' attribute store reference of IntVar, so that it can be used later as well
            option_dict[option].var = tk.IntVar()
            # 'variable' is tk.Checkbutton variable that sets 'textvariable=' param
            option_dict[option]['variable'] = option_dict[option].var
            if checkbox_default_state[idx] == 1:
                option_dict[option].select()
            option_dict[option].grid(row=irow, column=icol, sticky='w')
            # print(f"item {option} goes in row {irow} and column {icol}")
            if icol == row_increment:
                irow = irow + 1
        return option_dict

