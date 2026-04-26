import time
import random
import threading
from core.processor import TextProcessor
from utils.constants import TypingState

# Import handlers
from core.handlers.character_handler import CharacterHandler
from core.handlers.table_handler import TableHandler
from core.handlers.line_handler import LineHandler

class TypingEngine:
    def __init__(self, keyboard_manager, config_provider, status_callback=None, log_callback=None):
        self.kb = keyboard_manager
        self.config = config_provider
        self.status_callback = status_callback
        self.log_callback = log_callback
        self.state = TypingState.STOPPED
        self.thread = None
        self.pending_closures = [] # 追踪编辑器自动补全的闭合符号
        self.is_in_code_block = False # 显式追踪是否在代码块中
        self._stop_requested = False

    def log(self, msg):
        if self.log_callback:
            self.log_callback(msg)

    def set_status(self, status):
        if self.status_callback:
            self.status_callback(status)

    def start(self, text):
        if self.state in {TypingState.RUNNING, TypingState.PAUSED}:
            self.log("当前已有任务在执行或暂停中，忽略重复启动请求")
            return
        self._stop_requested = False
        self.state = TypingState.RUNNING
        self.thread = threading.Thread(target=self._worker, args=(text,), daemon=True)
        self.thread.start()

    def stop(self):
        self._stop_requested = True
        self.state = TypingState.STOPPED

    def pause(self):
        if self.state == TypingState.RUNNING:
            self.state = TypingState.PAUSED

    def resume(self):
        if self.state == TypingState.PAUSED:
            self.state = TypingState.RUNNING

    def _wait_if_paused(self):
        while self.state == TypingState.PAUSED:
            time.sleep(0.1)

    def _sleep(self, duration):
        """可中断的 sleep，每 0.1s 检查一次停止状态"""
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.state == TypingState.STOPPED:
                return True
            time.sleep(min(0.1, duration - (time.time() - start_time)))
        return False

    def _worker(self, text):
        conf = self.config()
        countdown = conf.get('countdown', 5)
        code_block_mode = conf.get('code_block_mode', 'markdown')
        pairs = TextProcessor.parse_auto_pairs(conf.get('auto_pair_config', "")) if conf.get('auto_pair_handle') else {}

        for i in range(countdown, 0, -1):
            if self.state == TypingState.STOPPED: return
            self.set_status(f"倒计时：{i} 秒，请切换到目标窗口")
            if self._sleep(1): return

        self.set_status("正在输入...")
        lines = text.split("\n")
        prev_type = "normal"
        in_table = False
        self.is_in_code_block = False 
        self.pending_closures = [] 

        for index, line in enumerate(lines):
            if self.state == TypingState.STOPPED: break
            self._wait_if_paused()
            
            # 每行开始前清空补全栈，确保单行逻辑纯净
            self.pending_closures = []

            # 预识别当前行类型
            raw_curr_type = TextProcessor.detect_line_type(line)
            next_line_type = TextProcessor.detect_line_type(lines[index+1]) if index < len(lines)-1 else "end"

            # --- 状态机核心：代码块逻辑优先 ---
            if self.is_in_code_block:
                # 严格检查是否是结束行：只要是纯反引号行（>=3个）就视为结束
                is_closing_block = raw_curr_type == "markdown_code_block" and all(c == '`' for c in line.strip())
                if is_closing_block:
                    self.log(f"第 {index + 1} 行：检测到代码块结束")
                    exit_script = conf.get('code_end_script', "").strip()
                    if code_block_mode == "block_editor" and exit_script:
                        self.kb.run_key_script(exit_script, lambda: self.state == TypingState.STOPPED)
                    else:
                        for ch in line:
                            self.kb.type_text(ch)
                        self.kb.press_enter()
                    
                    if self._sleep(random.uniform(1.0, 1.5)): return
                    self.is_in_code_block = False
                    prev_type = "markdown_code_block"
                    continue
                else:
                    # 在代码块内部，所有行一律视为普通文本
                    curr_type = "normal" if line.strip() else "blank"
            else:
                # 不在代码块中，检查是否开启
                if raw_curr_type == "markdown_code_block" and line.strip().startswith("```"):
                    self.log(f"第 {index + 1} 行：执行代码块开启流程")
                    # 提取语言，例如 ```python -> python
                    lang = line.strip().replace("`", "").strip()
                    if code_block_mode == "block_editor":
                        self.kb.type_text("```")
                        if self._sleep(random.uniform(1.0, 1.5)): return
                        if lang:
                            self.kb.type_text(lang)
                            if self._sleep(random.uniform(0.6, 1.0)): return
                        self.kb.press_enter()
                        if self._sleep(random.uniform(1.2, 1.8)): return
                    else:
                        for ch in line:
                            if self.state == TypingState.STOPPED: return
                            self._wait_if_paused()
                            if CharacterHandler.type_char(self, ch, conf, "markdown_code_block", pairs): return
                        if index < len(lines) - 1:
                            self.kb.press_enter()
                            if self._sleep(random.uniform(0.4, 0.7)): return
                    
                    self.is_in_code_block = True
                    prev_type = "markdown_code_block"
                    continue
                curr_type = raw_curr_type

            # --- 表格逻辑（仅在非代码块状态生效） ---
            if not self.is_in_code_block and conf.get('auto_table'):
                if curr_type == "markdown_table_separator":
                    if conf.get('skip_table_sep', True):
                        self.log(f"跳过第 {index + 1} 行表格分隔线")
                        in_table = True
                        prev_type = curr_type
                        continue

                    self.log(f"第 {index + 1} 行：保留表格分隔线原样输入")
                    in_table = True

                if curr_type == "markdown_table_row":
                    is_first_row = prev_type not in {"markdown_table_row", "markdown_table_separator"}
                    if is_first_row:
                        self.log(f"第 {index + 1} 行：表格首行转换")
                        for ch in line:
                            if self.state == TypingState.STOPPED: return
                            self._wait_if_paused()
                            if CharacterHandler.type_char(self, ch, conf, "normal"): return
                        self.kb.press_enter()
                        if self._sleep(random.uniform(1.2, 1.8)): return
                        in_table = True
                    else:
                        in_table = True
                        if TableHandler.type_table_row(self, line, conf): return

                    actual_next_type = next_line_type
                    lookahead_offset = 1
                    while actual_next_type == "markdown_table_separator" and (index + lookahead_offset + 1) < len(lines):
                        lookahead_offset += 1
                        actual_next_type = TextProcessor.detect_line_type(lines[index + lookahead_offset])

                    if actual_next_type == "markdown_table_row":
                        if not is_first_row:
                            self.kb.run_key_script(conf.get('table_row_script'), lambda: self.state == TypingState.STOPPED)
                            if self._sleep(random.uniform(0.35, 0.8)): return
                    else:
                        if in_table: TableHandler.exit_table(self, conf)
                        if index < len(lines) - 1:
                            self.kb.press_enter()
                            if self._sleep(random.uniform(0.5, 1.0)): return
                        in_table = False
                    prev_type = curr_type
                    continue

            # --- 通用打字逻辑 ---
            line_to_type = TextProcessor.prepare_line_for_editor(line, curr_type, prev_type, conf)
            
            # 解析符号补全对 (仅当开启 auto_pair_handle 时)
            for ch in line_to_type:
                if self.state == TypingState.STOPPED: break
                self._wait_if_paused()

                if CharacterHandler.type_char(self, ch, conf, curr_type, pairs): return

            # 行间换行处理
            if index < len(lines) - 1:
                if self.is_in_code_block:
                    # 代码块内部换行：保守策略
                    self.kb.press_enter()
                    if self._sleep(random.uniform(0.4, 0.7)): return
                else:
                    if LineHandler.type_enter_between_lines(self, curr_type, next_line_type, conf): return
            
            prev_type = curr_type

        completed_normally = not self._stop_requested
        self.state = TypingState.STOPPED
        self.set_status("输入完成" if completed_normally else "已停止")
