import operator
import re
import string


class BookProcessor:
    def __init__(self, path, dictionary):
        self.pathToFile = path;
        self.ranking = dict();
        self.dictionary = dictionary;
        self.invalidWords= 0;
        self.totalWords=0;
        self.digram_dict = dict()
        self.trigram_dict = dict()

    def read_book(self):
        with open(self.pathToFile, 'r', encoding='utf-8') as f:
            if f != '\n':
                content = f.readlines();
        content = [x for x in content if x != '\n']

        self.content = clean_rows(content);

    def create_ranking(self):
        for row in self.content:
            listOfWords = row.split();
            for word in listOfWords:
                try:
                    self.totalWords+=1
                    basicWord = self.dictionary[word].replace(' ','')
                    if basicWord is not None:
                        if basicWord in self.ranking:
                            self.ranking[basicWord] += 1;
                        else:
                            self.ranking[basicWord] = 1;
                except:
                    self.invalidWords+=1;

    def sorted_ranking(self):
        return sorted(self.ranking.items(), key=operator.itemgetter(1), reverse=True)

    def count_hapax_logomena(self):
        return sum(item == 1 for item in self.ranking.values())

    def words_of_half_text(self, sorted_list):
        sorted_ranking = dict()
        for item in sorted_list:
            sorted_ranking[item[0]] = item[1];
        values = list(sorted_ranking.values())
        act_sum = 0;
        index = 0
        while act_sum < sum(sorted_ranking.values())/2.0:
            act_sum +=values[index]
            index +=1

        return index;

    def create_ngram_dict(self):
        ngram_len = [2,3]
        for ngram in ngram_len:
            for row in self.content:
                for index in range(len(row)):
                    value = row[index:index + ngram].replace(' ','');
                    if value.__len__() == ngram:
                        if ngram == 2:
                            if value in self.digram_dict:
                                self.digram_dict[value] += 1;
                            else:
                                self.digram_dict[value] = 1;
                        else:
                            if value in self.trigram_dict:
                                self.trigram_dict[value] += 1;
                            else:
                                self.trigram_dict[value] = 1;

def clean_rows(content):
    return[ x.lower().translate(str.maketrans('', '', string.punctuation)).replace('\n','') for x in content if x.strip()];