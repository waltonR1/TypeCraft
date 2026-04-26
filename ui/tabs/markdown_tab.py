import tkinter as tk
from tkinter import ttk
from ui.tabs.base_tab import BaseTab
from ui.dialogs.record_dialog import RecordDialog

class MarkdownTab(BaseTab):
    def __init__(self, notebook, app_ui):
        super().__init__(notebook, "Markdown/表格", app_ui)

    def _build(self):
        # Editor Auto behavior
        editor_frame = ttk.LabelFrame(self, text="目标编辑器自动行为 (开启后程序将跳过对应符号)", padding=10)
        editor_frame.pack(fill=tk.X, pady=(0, 10))
        
        behaviors = [
            ("自动延续项目符号 (- / * / +)", self.app_ui.auto_bullet_list_var),
            ("自动延续数字列表 (1. / 2.)", self.app_ui.auto_numbered_list_var),
            ("自动延续引用块 (> )", self.app_ui.auto_quote_var),
            ("Markdown 表格转真实表格模式", self.app_ui.auto_table_var),
        ]
        for i, (txt, var) in enumerate(behaviors):
            ttk.Checkbutton(editor_frame, text=txt, variable=var).grid(row=i//2, column=i%2, sticky="w", padx=10, pady=5)

        # Table settings
        table_frame = ttk.LabelFrame(self, text="真实表格键盘脚本设置", padding=10)
        table_frame.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(table_frame, text="跳过 Markdown 分隔线 (| --- |)", variable=self.app_ui.table_skip_separator_var).grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        
        ttk.Label(table_frame, text="单元格间移动脚本:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Button(table_frame, textvariable=self.app_ui.table_cell_move_script_var, width=45, command=lambda: RecordDialog(self.app_ui.root, self.app_ui.table_cell_move_script_var)).grid(row=1, column=1, sticky="w", padx=10)
        
        ttk.Label(table_frame, text="行之间移动脚本:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Button(table_frame, textvariable=self.app_ui.table_row_move_script_var, width=45, command=lambda: RecordDialog(self.app_ui.root, self.app_ui.table_row_move_script_var)).grid(row=2, column=1, sticky="w", padx=10)
        
        ttk.Label(table_frame, text="表格结束退出脚本:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Button(table_frame, textvariable=self.app_ui.table_exit_script_var, width=45, command=lambda: RecordDialog(self.app_ui.root, self.app_ui.table_exit_script_var)).grid(row=3, column=1, sticky="w", padx=10)

        # Code Block settings
        code_frame = ttk.LabelFrame(self, text="代码块键盘脚本设置 (替代结束的 ``` 符号)", padding=10)
        code_frame.pack(fill=tk.X, pady=10)

        ttk.Label(code_frame, text="退出代码块脚本:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Button(code_frame, textvariable=self.app_ui.code_end_script_var, width=45, command=lambda: RecordDialog(self.app_ui.root, self.app_ui.code_end_script_var)).grid(row=0, column=1, sticky="w", padx=10)
        
        ttk.Label(self, text="点击上方按钮即可录制或修改按键脚本", font=("Arial", 8), foreground="gray").pack(anchor="w", padx=15)
