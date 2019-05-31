# -*- coding: utf-8 -*-
import codecs
from collections import defaultdict
import numpy as np
from collections import OrderedDict

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
        self.min_freq = -1
        self.max_freq = -1
        self.frequency = None

    def create_dictionary(self, path_to_file, form_file):
        with open(f'{path_to_file}/{form_file}', 'r') as f:
            if f != '\n':
                for row in f.readlines():
                    listOfWords = row.replace('\n', '').split();
                    for word in listOfWords[1:]:
                        self.dict_of_words[word] = listOfWords[0];

    def create_frequency_dict(self, text):
        frequency = OrderedDict()
        for line in text:
            words = line.split()
            for word in words:
                if word in frequency:
                    frequency[word] += 1
                else:
                    frequency[word] = 0
        freq_list = list(frequency.values())
        max_freq = max(freq_list)
        self.min_freq = (int)((0.2 / 100.0) * max_freq)
        self.max_freq = (int)((95.0 / 100.0) *max_freq)

        self.frequency = frequency

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

    def pre_process_vol_2(self, text):
        result = []
        for row in text:
            words = row.split()
            row_res = []
            for word in words:
                try:
                    occur = self.frequency[word.lower()]
                    if self.min_freq < occur < self.max_freq:
                        row_res.append(word)
                except Exception:
                    a = 3
            if len(row_res) > 0:
                result.append(' '.join(word for word in row_res).strip(' '))
        return result