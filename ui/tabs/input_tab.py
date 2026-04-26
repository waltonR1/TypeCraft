import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ui.tabs.base_tab import BaseTab

class InputTab(BaseTab):
    def __init__(self, notebook, app_ui):
        super().__init__(notebook, "输入文本", app_ui)

    def _build(self):
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(btn_frame, text="导入文件 (TXT/MD)", command=self._load_file).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="清空内容", command=lambda: self.text_box.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=5)

        self.text_box = tk.Text(self, wrap=tk.WORD, font=("Consolas", 11), undo=True)
        self.text_box.pack(fill=tk.BOTH, expand=True)

    def _load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text/Markdown", "*.txt *.md"), ("All Files", "*.*")])
        if not path: return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, content)
            self.app_ui.log(f"已导入文件: {path}")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件: {e}")

    def get_text(self):
        return self.text_box.get("1.0", tk.END).strip()

    def clear_text(self):
        self.text_box.delete("1.0", tk.END)
