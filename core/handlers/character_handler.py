import time
import random
from utils.constants import TypingState

class CharacterHandler:
    @staticmethod
    def type_char(engine, ch, conf, line_type, pairs=None):
        if engine.state == TypingState.STOPPED: return True
        
        # 智能处理自动补全逻辑
        if conf.get('auto_pair_handle') and pairs:
            # 1. 检查是否需要跳过（当前字符是预期的闭合符）
            if engine.pending_closures and ch == engine.pending_closures[-1]:
                engine.kb.run_key_script("right", lambda: engine.state == TypingState.STOPPED)
                # 必须等待光标移动
                time.sleep(random.uniform(0.08, 0.15))
                engine.log(f"智能跳过自动补全字符: {ch}")
                engine.pending_closures.pop()
                return False # 跳过打字
            
            # 2. 如果是开启符，记录预期的闭合符
            if ch in pairs:
                engine.pending_closures.append(pairs[ch])

        # 正常的打字逻辑
        if conf.get('mistake_enabled') and ch.isalpha() and random.random() < (conf.get('mistake_rate', 0) / 100):
            wrong_ch = CharacterHandler._get_wrong_char(ch)
            engine.kb.type_text(wrong_ch)
            if engine._sleep(random.uniform(0.05, 0.2)): return True
            engine.kb.press_backspace()
            if engine._sleep(random.uniform(0.05, 0.18)): return True
            engine.kb.type_text(ch)
        else:
            engine.kb.type_text(ch)
        
        # Pause after character
        delay = random.uniform(conf.get('min_delay', 0.04), conf.get('max_delay', 0.10)) if conf.get('jitter') else conf.get('min_delay', 0.04)
        
        if ch == " " and conf.get('system') == "macOS":
            # 针对 macOS 的空格自动变句号问题，增加空格后的延迟
            delay += random.uniform(0.35, 0.55)
        
        if line_type in {"markdown_table_row", "markdown_code_block"}: delay += random.uniform(0.01, 0.05)
        if conf.get('punc_pause') and ch in ",;:": delay += random.uniform(0.12, 0.35)
        if conf.get('sent_pause') and ch in ".!?": delay += random.uniform(0.25, 0.65)
        if conf.get('long_pause') and random.random() < 0.015: delay += random.uniform(0.8, 2.2)
        
        return engine._sleep(delay)

    @staticmethod
    def _get_wrong_char(correct_ch):
        letters = "abcdefghijklmnopqrstuvwxyz"
        if correct_ch.isupper(): letters = letters.upper()
        candidates = [c for c in letters if c.lower() != correct_ch.lower()]
        return random.choice(candidates)
