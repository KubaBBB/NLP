# -*- coding: utf-8 -*-
import codecs
from collections import defaultdict
import numpy as np

polish_lang_mapper = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ó': 'o', 'ń': 'n', 'ś': 's', 'ź': 'x', 'ż': 'z'}

def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "Unknown"

class TextProcessor:
    def __init__(self):
        self.dict_of_words = dict()
        self.pap = []

    def create_dictionary(self, path_to_file, form_file):
        polish_lang_values = list(polish_lang_mapper.values())
        with open(f'{path_to_file}/{form_file}', 'r') as f:
            if f != '\n':
                for row in f.readlines():
                    listOfWords = row.replace('\n', '').split();
                    for word in listOfWords[1:]:
                        self.dict_of_words[word] = listOfWords[0];

    def preprocess(self, row):
        result = []
        words = row.split()
        for word in words:
            if len(word) > 1:
                basic_form = word
                try:
                    basic_form = self.dict_of_words[word]
                except Exception:
                    result.append(basic_form)
            else:
                result.append(word)
        return ' '.join(word for word in result).strip(' ')


def get_hapax_dict(texts):
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    return frequency