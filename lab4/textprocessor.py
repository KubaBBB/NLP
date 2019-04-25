from collections import defaultdict

polish_lang_mapper = {'ą': 'A', 'ć': 'C', 'ę': 'E', 'ł': 'L', 'ó': 'O', 'ń': 'N', 'ś': 'S', 'ź': 'X', 'ż': 'Z'}
char_to_be_replaced = ['"', ',', '.', '?', '!', ':', ';', '[', ']', '(', ')', '–', '-', '%', '*', '`', 'ú']


def replace_chars_by_pattern(main_string, to_be_replaces, new_string):
    for elem in to_be_replaces:
        if elem in main_string:
            main_string = main_string.replace(elem, new_string)
    return main_string


def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


class TextProcessor:
    def __init__(self):
        self.dict_of_words = defaultdict(int)

    def map_chars(self, word):
        for i in range(len(word)):
            if word[i] in polish_lang_mapper:
                word = word.replace(word[i], polish_lang_mapper[word[i]])
        return word

    def create_dictionary(self, path_to_file, form_file):
        words = [line.rstrip('\n') for line in open(f'{path_to_file}/{form_file}.txt', 'r', encoding='utf-8') if 'ú' not in line]
        for word in words:
            word = self.map_chars(word)
            self.dict_of_words[word] += 1

    def improve_dictionary(self, path_to_files, polish_texts):
        for text in polish_texts:
            with open(f'{path_to_files}/{text}.txt', 'r', encoding='utf-8') as file:
                data = file.read().lower().replace('\n', ' ')
            data = replace_chars_by_pattern(data, char_to_be_replaced, '')
            data = ''.join(filter(lambda c: not c.isdigit(), data))
            data = ''.join(data.split())
            text_words = data.split()
            for word in text_words:
                word = self.map_chars(word)
                self.dict_of_words[word] += 1

    def unmap_words(self, word):
        for i in range(len(word)):
            if word[i] in polish_lang_mapper.values():
                key = get_key(word[i], polish_lang_mapper)
                word = word.replace(word[i], key)
        return word
