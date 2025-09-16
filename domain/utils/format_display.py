MAX_DISPLAY_CHARS = 16
BRAILLE_SPACE_CHAR = "⠠"

def format_braille_for_display(braille_string):
    filtered_words = [word for word in braille_string.split(BRAILLE_SPACE_CHAR) if word]
    lines_to_publish = []
    current_line = ""
    for word in filtered_words:
        if len(current_line) + len(word) + 1 > MAX_DISPLAY_CHARS:
            if current_line:
                lines_to_publish.append(current_line.strip())
            current_line = word + BRAILLE_SPACE_CHAR
        else:
            current_line += word + BRAILLE_SPACE_CHAR
    if current_line:
        lines_to_publish.append(current_line.strip())
    return lines_to_publish