import random
from utils.constants import TypingState

class LineHandler:
    @staticmethod
    def type_enter_between_lines(engine, curr_type, next_type, conf):
        if engine.state == TypingState.STOPPED: return True
        engine.kb.press_enter()
        
        # Handle auto-continuation logic
        if curr_type == "markdown_bullet_list" and conf.get('auto_bullet_list') and next_type != "markdown_bullet_list":
            if engine._sleep(random.uniform(0.25, 0.55)): return True
            engine.kb.press_enter()
        if curr_type == "markdown_numbered_list" and conf.get('auto_numbered_list') and next_type != "markdown_numbered_list":
            if engine._sleep(random.uniform(0.25, 0.55)): return True
            engine.kb.press_enter()
        if curr_type == "markdown_quote" and conf.get('auto_quote') and next_type != "markdown_quote":
            if engine._sleep(random.uniform(0.25, 0.55)): return True
            engine.kb.press_enter()
        
        # Line end pauses
        delay = 0
        if curr_type in {"markdown_bullet_list", "markdown_numbered_list", "markdown_quote", "markdown_table_row", "markdown_table_separator", "markdown_code_block", "markdown_separator"}:
            delay = random.uniform(0.65, 1.25)
        elif curr_type == "markdown_heading":
            delay = random.uniform(0.45, 0.95)
        else:
            delay = random.uniform(0.2, 0.55)
            
        return engine._sleep(delay)
