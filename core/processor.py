import re

class TextProcessor:
    @staticmethod
    def parse_auto_pairs(config_str):
        cleaned = config_str.replace(" ", "").replace(",", "")
        return {pair[0]: pair[1] for pair in re.findall(r'(.)(.)', cleaned)}

    @staticmethod
    def detect_line_type(line):
        stripped = line.lstrip()
        if not stripped:
            return "blank"
        if re.match(r"^#{1,6}\s", stripped):
            return "markdown_heading"
        if re.match(r"^[-*+]\s", stripped):
            return "markdown_bullet_list"
        if re.match(r"^\d+\.\s", stripped):
            return "markdown_numbered_list"
        if re.match(r"^>\s", stripped):
            return "markdown_quote"
        if TextProcessor.is_markdown_table_separator(line):
            return "markdown_table_separator"
        if stripped.startswith("|") and stripped.endswith("|"):
            return "markdown_table_row"
        if re.match(r"^`{3,}", stripped):
            return "markdown_code_block"
        if re.match(r"^[-*_]{3,}\s*$", stripped):
            return "markdown_separator"
        return "normal"

    @staticmethod
    def is_markdown_table_separator(line):
        stripped = line.strip()
        return bool(re.match(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", stripped))

    @staticmethod
    def parse_markdown_table_row(line):
        stripped = line.strip()
        if stripped.startswith("|"):
            stripped = stripped[1:]
        if stripped.endswith("|"):
            stripped = stripped[:-1]
        return [cell.strip() for cell in stripped.split("|")]

    @staticmethod
    def prepare_line_for_editor(line, current_line_type, previous_line_type, config):
        result = line
        if config.get('auto_bullet_list') and previous_line_type == "markdown_bullet_list" and current_line_type == "markdown_bullet_list":
            result = re.sub(r"^\s*[-*+]\s+", "", result)
        if config.get('auto_numbered_list') and previous_line_type == "markdown_numbered_list" and current_line_type == "markdown_numbered_list":
            result = re.sub(r"^\s*\d+\.\s+", "", result)
        if config.get('auto_quote') and previous_line_type == "markdown_quote" and current_line_type == "markdown_quote":
            result = re.sub(r"^\s*>\s+", "", result)
        return result
