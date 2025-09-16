BRAILLE_SPACE_CHAR = "⠠"

BRAILLE_VOWELS = set([
    '⠁', '⠂', '⠈', '⠐', '⠰', '⠠', '⠡', '⠪', '⠳', '⠻', '⠹', '⠵',
])

def post_process_braille(braille_string):
    processed_string = ""
    for i, char in enumerate(braille_string):
        if char ==  BRAILLE_SPACE_CHAR:
            if i > 0 and braille_string[i-1] in BRAILLE_VOWELS:
                processed_string += char
            else:
                processed_string += ' '
        else:
            processed_string += char
    return processed_string