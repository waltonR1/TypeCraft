import time
import random
from pynput.keyboard import Controller, Key

class KeyboardManager:
    def __init__(self, log_callback=None):
        self.keyboard = Controller()
        self.log_callback = log_callback

    def log(self, msg):
        if self.log_callback:
            self.log_callback(msg)

    def resolve_key(self, name):
        name = name.lower()
        mapping = {
            "enter": Key.enter,
            "return": Key.enter,
            "tab": Key.tab,
            "space": Key.space,
            "backspace": Key.backspace,
            "delete": Key.delete,
            "esc": Key.esc,
            "escape": Key.esc,
            "up": Key.up,
            "down": Key.down,
            "left": Key.left,
            "right": Key.right,
            "shift": Key.shift,
            "ctrl": Key.ctrl,
            "control": Key.ctrl,
            "alt": Key.alt,
            "option": Key.alt,
            "cmd": Key.cmd,
            "command": Key.cmd,
            "win": Key.cmd,
            "home": Key.home,
            "end": Key.end,
            "pageup": Key.page_up,
            "pagedown": Key.page_down,
        }
        if name in mapping:
            return mapping[name]
        if len(name) == 1:
            return name
        return None

    def press_key_combo(self, combo):
        keys_to_press = []
        parts = combo.split("+")
        for part in parts:
            key = self.resolve_key(part.strip())
            if key is not None:
                keys_to_press.append(key)
            else:
                self.log(f"未知按键：{part}")
        if not keys_to_press:
            return
        for key in keys_to_press:
            self.keyboard.press(key)
        for key in reversed(keys_to_press):
            self.keyboard.release(key)

    def run_key_script(self, script, stop_check=None):
        script = script.strip()
        if not script:
            return
        tokens = script.split()
        for token in tokens:
            if stop_check and stop_check():
                return
            if token.startswith("delay:"):
                try:
                    seconds = float(token.split(":")[1])
                    time.sleep(seconds)
                except (IndexError, ValueError):
                    self.log(f"无效的延迟格式：{token}")
            else:
                self.press_key_combo(token)
            time.sleep(random.uniform(0.08, 0.22))

    def type_text(self, text):
        for char in text:
            try:
                self.keyboard.type(char)
            except Exception:
                try:
                    self.keyboard.press(char)
                    self.keyboard.release(char)
                except Exception as e:
                    self.log(f"字符输入失败：{repr(char)} - {e}")

    def press_key(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    def press_enter(self):
        self.press_key(Key.enter)

    def press_backspace(self):
        self.press_key(Key.backspace)
