import re
import numpy as np

pathToFile = './data/'
upper_limit = 10;

class TextPreprocessor:
    def __init__(self):
        self.siema = 5
        self.digram_dict = dict()
        self.trigram_dict = dict()

    def __read_file(self, file):
        fullPath = pathToFile + file;
        with open(fullPath, 'r', encoding='utf-8') as f:
            if f != '\n':
                content = f.readlines();
        return content;

    def __filtr_file(self, content):
        stop_list = self.get_stop_list()
        filtered_file = []
        for row in content:
            lower_row = row.lower()
            for item in stop_list:
                r = re.sub('[\\\n--,.\t/+-;:\'\\"<>@?*&#$!\[]', '', lower_row)
                replaced_row = r.replace(item, '')

            filtered_file.append(replaced_row)
        return filtered_file

    def calculate_norm(self):
        return 2;

    def open_and_filtr_file(self, file):
        content = self.__read_file(file)
        return self.__filtr_file(content);

    def get_stop_list(self):
        return ['sp', 'llc', 'co', 'ltd', 'tel', 'email', ' ', 'tel', 'fax', 'gmail',
                'com', 'eu', 'pl', 'telfax', 'office', 'burg', 'poland']

    def create_clusters(self, norm_matrix, upper_limit):
        clusters = dict()
        for iterator in range(len(norm_matrix)):
            norms = [x for x in norm_matrix[iterator] if x < upper_limit]

        # dice_matrix[index][iterator] = dice;


