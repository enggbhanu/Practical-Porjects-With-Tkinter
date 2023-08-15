'''
Author : Bhanu Pratap Singh
Example shows extending BaseWindow class to add new widget to GUI also test simple blocking non-blocking call
'''

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog
import os
import inspect
import sys

# Finding the root path, required to run from terminal
directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
root_path = os.path.dirname(directory)
# setting root path
sys.path.append(root_path)
from utils.subproccess_manager import ProcessManager


class BaseWindow:
    def __init__(self, title="GUI"):
        self.base_win = tk.Tk()
        # self.title = tk.StringVar()
        self.status_var = tk.StringVar()

        # self.title.set(title)
        self.base_win.title(title)
        # for i in range(2):
        self.base_win.columnconfigure(0, weight=1, minsize=20)
        # for scrolled window and status bar
        for row in range(2):
            self.base_win.rowconfigure(row, weight=1, minsize=20)
        self.status_var.set("Ready ..")

        self.frm_main = ttk.Frame(self.base_win)
        self.frm_main.grid(column=0, row=0)

        self.frm_browse_dir = tk.LabelFrame(self.frm_main, relief=tk.RIDGE)
        self.frm_browse_dir.grid(column=0, row=0, sticky='w')

        self.lbl_browse = ttk.Label(self.frm_browse_dir, text="Browse Source Image Directory..",
                                    relief=tk.GROOVE, width=30)
        self.lbl_browse.grid(column=0, row=0, sticky='w')

        self.dir_path = tk.StringVar()
        self.btn_browse_dir = ttk.Button(self.frm_browse_dir, text="Browse", command=self.browse_dir)
        self.btn_browse_dir.grid(column=1, row=0, padx=5)

        self.txt_dir_path = ttk.Entry(self.frm_browse_dir, textvariable=self.dir_path, width=30)
        self.txt_dir_path.grid(column=2, row=0, padx=2, sticky='e')

        self.lbl_store_in_new_folder = ttk.Label(self.frm_browse_dir, text="Store output in different directory",
                                                 relief=tk.GROOVE, width=30)
        self.lbl_store_in_new_folder.grid(column=0, row=1, sticky='w')

        self.chk_create_store_in_folder = tk.Checkbutton(self.frm_browse_dir, text="Redirect output to local folder")
        self.chk_create_store_in_folder.grid(column=1, row=1)

        self.lst_src_files = tk.Listbox(self.frm_browse_dir, selectmode=tk.MULTIPLE, width=30, height=8)
        self.lst_src_files.grid(column=0, row=2, padx=2, sticky='w')

        self.btn_convert = ttk.Button(self.frm_browse_dir, text="Convert", command=self.convert_image)
        self.btn_convert.grid(column=1, row=2, padx=5)

        self.lst_dst_files = tk.Listbox(self.frm_browse_dir, selectmode=tk.MULTIPLE, width=30, height=8)
        self.lst_dst_files.grid(column=2, row=2, padx=2, sticky='e')

        self.scrl_output_widget = scrolledtext.ScrolledText(self.base_win, wrap=tk.WORD, width=30, height=10)
        self.scrl_output_widget.grid(column=0, row=3, sticky='we')

        self.status_bar = ttk.Label(self.base_win, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(column=0, row=4, sticky='we')
        # self.base_win.children()

    def convert_image(self):
        outfile_list = []
        selected_images_idx = self.lst_src_files.curselection()
        if not selected_images_idx:
            msg.showwarning("Please select at least one image to convert.")
            return
        for idx in selected_images_idx:
            src_fname = self.lst_src_files.get(idx)
            dst_fname = src_fname.split('.')[0]
            outfile_list.append(f"{dst_fname}.png")
            cmd = f"convert {self.dir_path.get()}/{src_fname} {self.dir_path.get()}/{dst_fname}.png"
            cmd_handle = ProcessManager(cmd, self.status_var, self.scrl_output_widget, dbg=True)
            cmd_handle.run()
        # When loop ends check for file.png exits than add it to dst list box
        for idx, out_files in enumerate(outfile_list):
            if os.path.exists(f"{self.dir_path.get()}/{out_files}"):
                self.lst_dst_files.insert(idx, out_files)
        # IDEA - could use thread with initial file count and add files to list widget as it appears

    def browse_dir(self):
        # find all webp files from the selected directory and display in source file list
        dir_path = filedialog.askdirectory(initialdir=os.path.expanduser("~") + '/GUI_Projects',
                                           title='Select image folder')
        self.dir_path.set(dir_path)
        src_files = self.list_files()
        self.lst_src_files.delete(0, tk.END)
        for idx, file in enumerate(src_files):
            self.lst_src_files.insert(idx, file)

    def list_files(self):
        file_list = []
        if os.path.exists(self.dir_path.get()):
            for file in os.listdir(self.dir_path.get()):
                if '.webp' in file:
                    file_list.append(file)
        print(file_list)
        return file_list

    def cb_nonblocking(self):
        cmd = 'cat file.txt'
        cmd_handle = ProcessManager(cmd, self.status_var, self.scrl_output_widget, dbg=True)
        cmd_handle.run()


if __name__ == '__main__':
    base_window = BaseWindow('Test GUI')
    base_window.base_win.mainloop()
