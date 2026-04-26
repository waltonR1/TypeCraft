import tkinter as tk
from tkinter import ttk
import time
from ui.tabs.base_tab import BaseTab

class LogTab(BaseTab):
    def __init__(self, notebook, app_ui):
        super().__init__(notebook, "执行日志", app_ui)

    def _build(self):
        self.log_box = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 10), background="#f0f0f0")
        self.log_box.pack(fill=tk.BOTH, expand=True)

    def append_log(self, msg):
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)
