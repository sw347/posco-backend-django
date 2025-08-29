import random
import os

class Words:
    consonants = [
        'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
        'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ'
    ]

    vowels = [
        'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ',
        'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅘ', 'ㅝ', 'ㅙ', 'ㅞ', 'ㅢ'
    ]

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    korean_alphabets = random.sample(consonants + vowels, 10)

    @staticmethod
    def generate_full_korean_characters():
        start_char_code = ord('가')
        end_char_code = ord('힣')
        
        full_korean_chars = []
        for code in range(start_char_code, end_char_code + 1):
            full_korean_chars.append(chr(code))
        return random.sample(full_korean_chars, 15)

    full_korean_character_list = generate_full_korean_characters()

    @staticmethod
    def load_words(filename, count=20):
        with open(filename, "r", encoding="utf-8") as f:
            all_words = f.read().splitlines()
        return random.sample(all_words, count)
    
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    parent_dir = os.path.dirname(current_dir)
    words_file_path = os.path.join(parent_dir, "resources", "words.txt")


    full_korean_word_list = load_words(words_file_path, 20)