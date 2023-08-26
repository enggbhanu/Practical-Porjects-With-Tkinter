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

        self.lbl_browse = ttk.Label(self.frm_browse_dir, text="Browse Source Image Directory    ->",
                                    relief=tk.FLAT, width=30)
        self.lbl_browse.grid(column=0, row=0, sticky='w')

        self.dir_path = tk.StringVar()
        self.btn_browse_dir = ttk.Button(self.frm_browse_dir, text="Browse", command=self.browse_dir)
        self.btn_browse_dir.grid(column=1, row=0, padx=5)

        self.txt_dir_path = ttk.Entry(self.frm_browse_dir, textvariable=self.dir_path, width=40)
        self.txt_dir_path.grid(column=2, row=0, padx=2, sticky='e')

        self.lbl_store_in_new_folder = ttk.Label(self.frm_browse_dir, text="Store output in different directory ->",
                                                 relief=tk.FLAT, width=30)
        self.lbl_store_in_new_folder.grid(column=0, row=1, sticky='w', pady=3)

        create_folder_select = tk.IntVar()

        self.chk_create_store_in_folder = tk.Checkbutton(self.frm_browse_dir, text="Redirect output to local folder",
                                                         variable=create_folder_select)
        self.chk_create_store_in_folder.grid(column=1, row=1, pady=3, sticky='w')
        self.chk_create_store_in_folder.var = create_folder_select

        self.selected_img_count = tk.StringVar()
        self.selected_img_count.set("None Selected")
        self.lbl_img_info = ttk.Label(self.frm_browse_dir, textvariable=self.selected_img_count,
                                        relief=tk.FLAT, width=30)
        self.lbl_img_info.grid(column=0, row=2, sticky='w', pady=3)

        self.lbl_img_format = ttk.Label(self.frm_browse_dir, text="Select output image format   ->",
                                        relief=tk.FLAT, width=30)
        self.lbl_img_format.grid(column=1, row=2, sticky='w', pady=3)

        img_format = tk.StringVar()
        self.cbox_image_format = ttk.Combobox(self.frm_browse_dir, textvariable=img_format)
        self.cbox_image_format['value'] = ('.jpg', '.png', '.jpeg')
        self.cbox_image_format.grid(column=2, row=2, padx=2, pady=3, sticky='w')
        self.cbox_image_format.current(0)

        self.lst_src_files = tk.Listbox(self.frm_browse_dir, selectmode=tk.MULTIPLE, width=40, height=8)
        self.lst_src_files.grid(column=0, row=3, padx=2, sticky='w')
        self.lst_src_files.bind("<Control-a>", lambda cbk: self.list_box_select_all())
        self.lst_src_files.bind("<<ListboxSelect>>", self.set_selected_count)

        self.btn_convert = ttk.Button(self.frm_browse_dir, text="Convert", command=self.convert_image)
        self.btn_convert.grid(column=1, row=3, padx=5)

        self.lst_dst_files = tk.Listbox(self.frm_browse_dir, selectmode=tk.MULTIPLE, width=40, height=8)
        self.lst_dst_files.grid(column=2, row=3, padx=2, sticky='e')

        self.scrl_output_widget = scrolledtext.ScrolledText(self.base_win, wrap=tk.WORD, width=30, height=10)
        self.scrl_output_widget.grid(column=0, row=1, sticky='we')

        self.status_bar = ttk.Label(self.base_win, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(column=0, row=2, sticky='we')
        # self.base_win.children()

    def convert_image(self):
        outfile_list = []
        selected_images_idx = self.lst_src_files.curselection()
        out_img_path = ""
        if not selected_images_idx:
            msg.showwarning("Error converting image(s)", "Please select at least one image to convert.")
            return
        in_img_path = self.dir_path.get()
        if self.chk_create_store_in_folder.var.get():
            # create a folder name converted inside source folder
            print("Store in folder is selected.")
            out_img_path_original = in_img_path + "/" + "converted_images"
            if not os.path.exists(out_img_path_original):
                os.makedirs(out_img_path_original)
        else:
            out_img_path_original = in_img_path

        # if folder name/file contain space must be replaced with escap char for command execution
        in_img_path = in_img_path.replace(' ', '\ ')
        out_img_path = out_img_path_original.replace(' ', '\ ')
        # /_\
        # print(f'select fmt {self.cbox_image_format.get()}')
        if not self.cbox_image_format.get():
            img_format = '.png'
        else:
            img_format = self.cbox_image_format.get()

        for idx in selected_images_idx:
            src_fname = self.lst_src_files.get(idx)
            # find . in end of file name to avoid issue with file name which contains multiple . char
            fname_len = src_fname.rfind('.')
            dst_fname = src_fname[0:fname_len]
            outfile_list.append(f"{dst_fname}{img_format}")
            cmd = f"convert {in_img_path}/{src_fname} {out_img_path}/{dst_fname}{img_format}"
            print(cmd)
            cmd_handle = ProcessManager(cmd, self.status_var, self.scrl_output_widget, blocking=True, dbg=False)
            cmd_handle.run()
        # When loop ends check for file.png exits than add it to dst list box
        for idx, out_files in enumerate(outfile_list):
            if os.path.exists(f"{out_img_path_original}/{out_files}"):
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

    def list_box_select_all(self):
        self.lst_src_files.selection_set(0, tk.END)
        items = self.lst_src_files.curselection()
        self.selected_img_count.set(f'{len(items)} image(s) are selected')
        # print('activating')

    def set_selected_count(self, event):
        items = event.widget.curselection()
        print('item selected', items)
        self.selected_img_count.set(f'{len(items)} image(s) are selected')


if __name__ == '__main__':
    base_window = BaseWindow('Test GUI')
    base_window.base_win.mainloop()
