import itertools

BRAILLE_BLANK_CHAR = "⠀"
BRAILLE_SPACE_CHAR = "⠠"

def braille_to_list(braille_string):
  result_list = []

  braille_base_code = 0x2800
  
  braille_string = braille_string.replace(BRAILLE_SPACE_CHAR, BRAILLE_BLANK_CHAR)

  for char in braille_string:

    char_code = ord(char)

    pattern_value = char_code - braille_base_code

    dot_pattern = [0] * 6

    if pattern_value & 1:
      dot_pattern[0] = 1
    if pattern_value & 2:
      dot_pattern[1] = 1
    if pattern_value & 4:
      dot_pattern[2] = 1
    if pattern_value & 8:
      dot_pattern[3] = 1
    if pattern_value & 16:
      dot_pattern[4] = 1
    if pattern_value & 32:
      dot_pattern[5] = 1

    result_list.append(dot_pattern)
  
  flat_list = list(itertools.chain.from_iterable(result_list))
  
  return { 'one_dimension': flat_list, 'two_dimension': result_list }