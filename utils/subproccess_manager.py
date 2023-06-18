import subprocess
from queue import Queue, Empty
from threading import Thread
import tkinter as tk


class ProcessManager:
    def __init__(self, cmd, status_var, output_widget, blocking=False, widget_tk=None, dbg=False):
        self.cmd = cmd
        self.process_status = status_var  # Sets GUI status bar variable ref to object var
        # set base window tkinter widget references
        self.scrolled_output_widget = output_widget
        self.scrolled_output_widget.tag_config("err", foreground="red")
        self.scrolled_output_widget.tag_config("prc_cmd", foreground="green")
        self.widget_tk = widget_tk
        # Defines queues for process management
        self.process_end_state_q = Queue()
        self.process_output_q = Queue()
        # flag to choose blocking/non-blocking exe of process/command
        self.flg_blocking = blocking
        # internal process monitoring flags
        self.flg_finished = False
        self.flg_error = False
        # internal buffer
        self.process_out_buff = []

        # set this variable to true for debugging
        self.dbg = dbg

    def _run_subprocess(self):
        if self.flg_blocking:
            process_out = subprocess.run(self.cmd, shell=True, capture_output=True)
        else:
            process_out = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        return process_out

    def _enqueue_process_output(self, process_out):
        for line in iter(process_out.readline, b''):
            self.process_output_q.put(line)
        process_out.close()

    def _enqueue_process_status(self, process_out):
        # return and store the process status (0=success else failed)s to queue
        self.process_end_state_q.put(process_out.wait())

    @staticmethod
    def format_bytestream(self, bytestream):
        return bytestream.decode("utf-8").split("\n")

    def _process_state_monitor(self):
        if self.dbg:
            print("_process_state_monitor() thread started ...")
        while True:
            try:
                process_state = self.process_end_state_q.get_nowait()
            except Empty:
                continue
            else:
                if process_state != 0:
                    self.scrolled_output_widget.insert(tk.INSERT,
                                                       f"Error: process exited, error code: {process_state}\n")
                    for itm in self.process_out_buff:
                        self.scrolled_output_widget.insert(tk.INSERT, itm)
                    self.flg_error = True
                self.flg_finished = True
                break
        if self.dbg:
            print("_process_state_monitor() thread finished !!")

    def _process_output_monitor(self):
        if self.dbg:
            print("_process_output_monitor() thread started ...")
        idx = 0
        while True:
            try:
                line = self.process_output_q.get_nowait()
            except Empty:
                if self.flg_finished:
                    break
            else:
                self.process_out_buff.append(line)
                if self.widget_tk is not None:
                    if type(self.widget_tk) == tk.Listbox:
                        self.widget_tk.insert(idx, line.decode("utf-8"))
                        idx = +1
                self.scrolled_output_widget.insert(tk.INSERT, line.decode("utf-8"))
                if self.dbg:
                    print(line)
        self.process_status.set("Ready.")
        if self.dbg:
            print("_process_output_monitor() thread finished ...")

    def run(self):
        if not self.cmd:
            print("No command to execute.")
            return
        # blocking call is useful when you are sure process will run and finish quickly
        # if process takes long time it may render tkinter gui unresponsive consider nonblocking call
        process_out = self._run_subprocess()  # non/blocking type handled internally by _run_subprocess function
        if self.flg_blocking:
            if process_out.returncode == 0:
                if self.widget_tk is not None:
                    if type(self.widget_tk) == tk.Listbox:
                        items = self.format_bytestream(process_out)
                        idx = 0
                        for item in items:
                            if len(item) != 0:
                                self.widget_tk.insert(idx, item)
                                idx = +1
                else:
                    self.scrolled_output_widget.insert(tk.INSERT, process_out.stdout.decode("utf-8"))
            else:
                self.scrolled_output_widget.insert(tk.INSERT,
                                                   f"Error: Process Exited with Error, Exit Code: {process_out.returncode}\n",
                                                   "err")
                self.scrolled_output_widget.insert(tk.INSERT, process_out.stdout.decode("utf-8"), "err")
                if self.dbg:
                    print("Error: ", process_out.stdout.decode("utf-8"))
        else:
            # Non blocking
            process_out_q_thread = Thread(target=self._enqueue_process_output, args=(process_out,), daemon=True)
            process_status_q_thread = Thread(target=self._enqueue_process_status, args=(process_out,), daemon=True)

            process_cmd_out_thread = Thread(target=self._process_output_monitor, daemon=True)
            process_cmd_state_thread = Thread(target=self._process_state_monitor, daemon=True)

            process_out_q_thread.start()
            process_status_q_thread.start()
            process_cmd_out_thread.start()
            process_cmd_state_thread.start()
            if self.dbg:
                print("method run() finished for non-blocking call, return to GUI")
