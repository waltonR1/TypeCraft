import tkinter as tk
from ui.app import HumanTypingUI
from core.engine import TypingEngine
from core.keyboard_manager import KeyboardManager
from utils.constants import TypingState

def main():
    root = tk.Tk()
    
    # 1. Initialize Keyboard Manager
    kb_manager = KeyboardManager()
    
    # 2. Initialize UI (placeholders for engine callbacks)
    app_ui = HumanTypingUI(
        root,
        engine_start_callback=None, # Will set later
        engine_stop_callback=None,
        engine_pause_callback=None
    )
    
    # 3. Initialize Engine
    engine = TypingEngine(
        keyboard_manager=kb_manager,
        config_provider=app_ui.get_config,
        status_callback=app_ui.update_countdown,
        log_callback=app_ui.log
    )
    
    # Update Keyboard Manager with UI log callback
    kb_manager.log_callback = app_ui.log
    
    # 4. Connect UI to Engine
    app_ui.engine_start = engine.start
    app_ui.engine_stop = engine.stop
    app_ui.engine_pause = lambda: engine.pause() if engine.state == TypingState.RUNNING else engine.resume()

    # Periodically update state in UI
    def update_ui_state():
        state_map = {
            TypingState.STOPPED: "停止",
            TypingState.RUNNING: "运行中",
            TypingState.PAUSED: "暂停"
        }
        app_ui.update_status(state_map.get(engine.state, "未知"))
        root.after(500, update_ui_state)

    update_ui_state()
    
    # Handle window close
    def on_close():
        engine.stop()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
