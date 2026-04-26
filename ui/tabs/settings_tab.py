import tkinter as tk
from tkinter import ttk
from ui.tabs.base_tab import BaseTab

class SettingsTab(BaseTab):
    def __init__(self, notebook, app_ui):
        super().__init__(notebook, "打字设置", app_ui)

    def _build(self):
        # System info
        sys_frame = ttk.LabelFrame(self, text="系统环境", padding=10)
        sys_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(sys_frame, text="识别到的系统：").pack(side=tk.LEFT)
        ttk.Combobox(sys_frame, textvariable=self.app_ui.system_var, values=["Windows", "macOS", "Linux"], state="readonly", width=12).pack(side=tk.LEFT)

        # Basic Params
        param_frame = ttk.LabelFrame(self, text="打字参数", padding=10)
        param_frame.pack(fill=tk.X, pady=10)
        
        self._add_spinbox(param_frame, "最小字符延迟 (秒)", self.app_ui.min_delay_var, 0.01, 2.0, 0, 0)
        self._add_spinbox(param_frame, "最大字符延迟 (秒)", self.app_ui.max_delay_var, 0.01, 3.0, 0, 2)
        self._add_spinbox(param_frame, "执行前倒计时 (秒)", self.app_ui.countdown_var, 0, 30, 1, 0)
        self._add_spinbox(param_frame, "英法错字率 (%)", self.app_ui.mistake_rate_var, 0, 30, 1, 2)

        # Simulation Switches
        switch_frame = ttk.LabelFrame(self, text="真人模拟开关", padding=10)
        switch_frame.pack(fill=tk.X, pady=10)
        
        switches = [
            ("字符随机抖动", self.app_ui.char_jitter_var),
            ("标点符号停顿", self.app_ui.punctuation_pause_var),
            ("句子末尾停顿", self.app_ui.sentence_pause_var),
            ("随机长停顿 (模拟思考)", self.app_ui.random_long_pause_var),
            ("模拟输入错误并修正", self.app_ui.mistake_var),
            ("智能处理自动补全 (括号/引号)", self.app_ui.auto_pair_handle_var),
        ]
        for i, (txt, var) in enumerate(switches):
            ttk.Checkbutton(switch_frame, text=txt, variable=var).grid(row=i//3, column=i%3, sticky="w", padx=10, pady=5)

        ttk.Label(switch_frame, text="补全符号配置 (成对输入):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(switch_frame, textvariable=self.app_ui.auto_pair_config_var, width=30).grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=5)

    def _add_spinbox(self, parent, label, var, from_, to, row, col):
        ttk.Label(parent, text=label).grid(row=row, column=col, sticky="w", padx=5, pady=5)
        ttk.Spinbox(parent, textvariable=var, from_=from_, to=to, increment=0.01 if isinstance(var.get(), float) else 1, width=8).grid(row=row, column=col+1, sticky="w", padx=5)
