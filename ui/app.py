import tkinter as tk
from tkinter import ttk, messagebox
import queue
from utils.constants import APP_TITLE
from utils.os_helper import detect_os

# Import refactored components
from ui.tabs.input_tab import InputTab
from ui.tabs.settings_tab import SettingsTab
from ui.tabs.markdown_tab import MarkdownTab
from ui.tabs.log_tab import LogTab

class HumanTypingUI:
    def __init__(self, root, engine_start_callback, engine_stop_callback, engine_pause_callback):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("800x750") # Slightly taller to ensure no clipping
        self.root.minsize(600, 500)

        self.engine_start = engine_start_callback
        self.engine_stop = engine_stop_callback
        self.engine_pause = engine_pause_callback
        self.log_queue = queue.Queue()

        self._init_vars()
        self._build_ui()
        self.poll_log_queue()

    def _init_vars(self):
        # System
        self.system_var = tk.StringVar(value=detect_os())
        
        # Typing Params
        self.min_delay_var = tk.DoubleVar(value=0.04)
        self.max_delay_var = tk.DoubleVar(value=0.10)
        self.countdown_var = tk.IntVar(value=5)
        self.mistake_rate_var = tk.DoubleVar(value=0.0)
        
        # Switches
        self.char_jitter_var = tk.BooleanVar(value=True)
        self.punctuation_pause_var = tk.BooleanVar(value=True)
        self.sentence_pause_var = tk.BooleanVar(value=True)
        self.random_long_pause_var = tk.BooleanVar(value=False)
        self.mistake_var = tk.BooleanVar(value=False)
        self.auto_pair_handle_var = tk.BooleanVar(value=True)
        self.auto_pair_config_var = tk.StringVar(value="(), [], {}, \"\", ''")
        
        # Editor Behavior
        self.auto_bullet_list_var = tk.BooleanVar(value=False)
        self.auto_numbered_list_var = tk.BooleanVar(value=False)
        self.auto_table_var = tk.BooleanVar(value=False)
        self.auto_quote_var = tk.BooleanVar(value=False)
        
        # Table Scripting
        self.table_skip_separator_var = tk.BooleanVar(value=True)
        self.table_cell_move_script_var = tk.StringVar(value="tab")
        self.table_row_move_script_var = tk.StringVar(value="enter")
        self.table_exit_script_var = tk.StringVar(value="")
        
        # Code Block Scripting
        self.code_end_script_var = tk.StringVar(value="enter")

        # Status
        self.status_var = tk.StringVar(value="状态：停止")
        self.countdown_label_var = tk.StringVar(value="准备就绪")

    def _build_ui(self):
        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header_frame, text=APP_TITLE, font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(header_frame, textvariable=self.status_var, font=("Arial", 10, "italic"))
        self.status_label.pack(side=tk.RIGHT)

        # Tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Initialize Tab Objects
        self.input_tab = InputTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        self.markdown_tab = MarkdownTab(self.notebook, self)
        self.log_tab = LogTab(self.notebook, self)

        # Footer / Controls
        footer = ttk.Frame(main_container, padding=(0, 10, 0, 0))
        footer.pack(fill=tk.X)

        ttk.Button(footer, text="开始执行", command=self._on_start, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(footer, text="暂停 / 继续", command=self._on_pause).pack(side=tk.LEFT, padx=5)
        ttk.Button(footer, text="停止", command=self._on_stop).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(footer, textvariable=self.countdown_label_var, foreground="#d35400", font=("Arial", 11, "bold")).pack(side=tk.RIGHT)

    def _on_start(self):
        text = self.input_tab.get_text()
        if not text:
            messagebox.showwarning("提示", "请输入要打字的文本")
            return
        if self.engine_start:
            self.engine_start(text)

    def _on_pause(self):
        if self.engine_pause:
            self.engine_pause()

    def _on_stop(self):
        if self.engine_stop:
            self.engine_stop()

    def log(self, msg):
        self.log_queue.put(msg)

    def poll_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get_nowait()
            self.log_tab.append_log(msg)
        self.root.after(100, self.poll_log_queue)

    def get_config(self):
        return {
            'min_delay': self.min_delay_var.get(),
            'max_delay': self.max_delay_var.get(),
            'countdown': self.countdown_var.get(),
            'mistake_rate': self.mistake_rate_var.get(),
            'jitter': self.char_jitter_var.get(),
            'punc_pause': self.punctuation_pause_var.get(),
            'sent_pause': self.sentence_pause_var.get(),
            'long_pause': self.random_long_pause_var.get(),
            'mistake_enabled': self.mistake_var.get(),
            'auto_pair_handle': self.auto_pair_handle_var.get(),
            'auto_pair_config': self.auto_pair_config_var.get(),
            'auto_bullet_list': self.auto_bullet_list_var.get(),
            'auto_numbered_list': self.auto_numbered_list_var.get(),
            'auto_table': self.auto_table_var.get(),
            'auto_quote': self.auto_quote_var.get(),
            'skip_table_sep': self.table_skip_separator_var.get(),
            'table_cell_script': self.table_cell_move_script_var.get(),
            'table_row_script': self.table_row_move_script_var.get(),
            'table_exit_script': self.table_exit_script_var.get(),
            'code_end_script': self.code_end_script_var.get(),
        }

    def update_status(self, state_text):
        self.status_var.set(f"状态：{state_text}")

    def update_countdown(self, text):
        self.countdown_label_var.set(text)
