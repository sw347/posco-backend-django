import itertools
from domain.utils.dot_to_list import braille_to_list
from domain.utils.format_display import format_braille_for_display
from domain.utils.post_process import post_process_braille

MAX_DISPLAY_CHARS = 16
BLANK_BRAILLE_CELL = [0, 0, 0, 0, 0, 0]

def get_formatted_braille_data(braille_string):
    processed_braille_string = post_process_braille(braille_string)
    lines = format_braille_for_display(processed_braille_string)
    
    mqtt_braille_chunks = []
    json_braille_chunks = []
    
    for line in lines:
        braille_dot_data = braille_to_list(line)
        padded_two_d_chunk = braille_dot_data['two_dimension']
        
        if len(padded_two_d_chunk) < MAX_DISPLAY_CHARS:
            padding_needed = MAX_DISPLAY_CHARS - len(padded_two_d_chunk)
            padded_two_d_chunk.extend([BLANK_BRAILLE_CELL] * padding_needed)

        json_braille_chunks.append(padded_two_d_chunk)

        mqtt_braille_chunks.extend(list(itertools.chain.from_iterable(padded_two_d_chunk)))
        
    return {
        'mqtt_data': mqtt_braille_chunks,
        'json_data': json_braille_chunks
    }