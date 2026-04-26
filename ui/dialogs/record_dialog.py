import tkinter as tk
from tkinter import ttk

class RecordDialog:
    KEY_ORDER = {
        "ctrl": 0,
        "cmd": 1,
        "alt": 2,
        "shift": 3,
    }

    def __init__(self, parent, target_var):
        self.parent = parent
        self.target_var = target_var
        self.recorded_actions = []
        self.current_keys = set()
        
        self.win = tk.Toplevel(parent)
        self.win.title("录制按键脚本")
        self.win.geometry("350x180")
        self.win.transient(parent)
        self.win.grab_set()
        
        self._build_ui()
        self._bind_events()
        self._center_window()

    def _build_ui(self):
        main_frame = ttk.Frame(self.win, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="正在录制按键脚本...", font=("Arial", 11, "bold")).pack(pady=(0, 10))
        
        self.display_var = tk.StringVar(value="等待按键...")
        status_label = ttk.Label(main_frame, textvariable=self.display_var, font=("Consolas", 12), foreground="#e67e22")
        status_label.pack(pady=10)
        
        ttk.Label(main_frame, text="直接按下键盘组合 (支持多动作)\n按 ESC 完成并保存", foreground="gray", justify=tk.CENTER).pack(pady=5)
        
        ttk.Button(main_frame, text="完成并关闭", command=self.win.destroy).pack(pady=10)

    def _bind_events(self):
        self.win.bind("<KeyPress>", self._on_key_press)
        self.win.bind("<KeyRelease>", self._on_key_release)

    def _on_key_press(self, event):
        key = event.keysym.lower()
        mapping = {
            "return": "enter", "control_l": "ctrl", "control_r": "ctrl",
            "alt_l": "alt", "alt_r": "alt", "shift_l": "shift", "shift_r": "shift",
            "command": "cmd", "win_l": "cmd", "win_r": "cmd", "meta_l": "cmd", "meta_r": "cmd"
        }
        key = mapping.get(key, key)
        if key == "escape":
            self.win.destroy()
            return
        self.current_keys.add(key)
            
    def _on_key_release(self, event):
        if not self.current_keys: return
        combo = "+".join(sorted(self.current_keys, key=lambda key: (self.KEY_ORDER.get(key, 99), key)))
        self.recorded_actions.append(combo)
        self.target_var.set(" ".join(self.recorded_actions))
        self.display_var.set(" ".join(self.recorded_actions))
        self.current_keys.clear()

    def _center_window(self):
        self.win.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.win.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.win.winfo_height() // 2)
        self.win.geometry(f"+{x}+{y}")
