import re
import operator
import collections

# datasets      learning / (learning+testing)
quot = 0.8;

class Language:
    def __init__(self, path, ngram_len, encoding='default'):
        self.ngram_len = ngram_len;
        self.path = path;
        self.context = [];
        self.ngram_dict = dict();
        self.encoding = encoding;
        self.norm = None;
        self.testing_set = None;
        self.training_set = None;
        self.recall = 0;
        self.precision = 0;

    def open_and_remove_bad_chars(self, fname):
        fullpath = self.path + fname;
        if self.encoding is not 'default':
            with open(fullpath, 'r', encoding='utf-8') as f:
                if f != '\n':
                    content = f.readlines();
        else:
            with open(fullpath) as f:
                if f != '\n':
                    content = f.readlines();
        content = [x for x in content if x != '\n']

        rows = []
        for row in content:
            rows.append(re.sub('[\\\n--,.\t]', '', row).lower())

        self.context += rows;

    def share_dataset(self):
        len = self.context.__len__()*quot;
        self.training_set = self.context[0:int(len)];
        self.testing_set = self.context[int(len):self.context.__len__()];
        return;

    def get_dict(self):
        return self.ngram_dict;

    def get_ngram_vec(self):
        return self.context;

    def create_dictionary(self):
        for row in self.context:
            for index in range(len(row)):
                value = row[index:index + self.ngram_len];

                if value in self.ngram_dict:
                    self.ngram_dict[value] += 1;
                else:
                    self.ngram_dict[value] = 1;

    def get_sorted_dict(self):
        return sorted(self.ngram_dict.items(), key=operator.itemgetter(1), reverse=True);

    def calculate_cos_norm(self, input_ngram):
        collection = collections.Counter(input_ngram);
        dic = self.ngram_dict;
        sum = 0;

        for val in collection:
            count = dic.get(val);
            if count is not None:
                sum += count * collection[val];

        self.norm = 1 - (sum / (len(input_ngram) * len(self.context)));
