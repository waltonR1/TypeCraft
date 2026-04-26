import random
from utils.constants import TypingState
from core.processor import TextProcessor
from core.handlers.character_handler import CharacterHandler

class TableHandler:
    @staticmethod
    def type_table_row(engine, line, conf):
        cells = TextProcessor.parse_markdown_table_row(line)
        pairs = TextProcessor.parse_auto_pairs(conf.get('auto_pair_config', "")) if conf.get('auto_pair_handle') else {}

        for i, cell in enumerate(cells):
            for ch in cell:
                if engine.state == TypingState.STOPPED: return True
                engine._wait_if_paused()
                if CharacterHandler.type_char(engine, ch, conf, "markdown_table_row", pairs): return True
            if i < len(cells) - 1:
                engine.kb.run_key_script(conf.get('table_cell_script'), lambda: engine.state == TypingState.STOPPED)
                if engine._sleep(random.uniform(0.16, 0.38)): return True
        return False

    @staticmethod
    def exit_table(engine, conf):
        script = conf.get('table_exit_script', "").strip()
        if not script:
            engine._sleep(random.uniform(0.25, 0.55))
        else:
            engine.kb.run_key_script(script, lambda: engine.state == TypingState.STOPPED)
