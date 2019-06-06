# coding: utf-8

import re
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import codecs
from collections import defaultdict
import operator
import time

path = 'C:/Users/BOLSON-PC/Desktop/studia/IT/PJN/NLP/lab7/data'
authors = ['Szklarski', 'Dukaj', 'MacLean', 'Norton', 'McCaffrey', 'Bulyczow', 'Scott', 'Gibson']
fileToCreateDict = 'odm.txt'


def create_dictionary(fullpath):
    voc = dict()
    with codecs.open(fullpath, 'r', 'utf-8') as f:
        text = f.read().lower()
        lines = text.split('\r\n')
        for line in lines:
            words = np.array(line.split(', '))
            for word in words:
                voc[word] = words[0]
    return voc

def to_basic_form(matchobj):
    word = matchobj.group(0)
    if word in dictionary:
        return dictionary[word]
    else:
        return None

def read_text_for_each_author(path):
    text_per_author = defaultdict(list)
    for file in os.listdir(path):
        for author in authors:
            if author in file:
                print(file)
                with codecs.open(path + '/' + file, 'r', 'utf-8') as f:
                    text = f.read().lower()
                    pre_text = re.sub(r'#\d+', '##', text)
                    pre_text = re.sub(r'\n', ' ', pre_text)
                    pre_text = re.sub(
                        r'[§$#¨|\^\\,.\-\'\"()?:;+\/\d+&`!\[\]@<>%*~{}=\x9a\x96\x91\x84\x8c\x93\x9c\x9f\x92\x80\x94\x95°\x97]',
                        '', pre_text)
                    pre_text = re.sub(r'   ', '  ', pre_text)
                    pre_text = re.sub(r'  ', ' ', pre_text)
                    text_per_author[author].append(pre_text)
    return text_per_author

def get_text_per_author_with_basic_forms(text_per_author, word_pattern):
    texts_with_authors_basic_forms = defaultdict(list)
    for author in text_per_author:
        for text in text_per_author[author]:
            texts_with_authors_basic_forms[author].append(word_pattern.sub(to_basic_form, text))
    return texts_with_authors_basic_forms

def get_all_texts(texts_with_authors_basic_forms):
    all_texts = list()
    for key in texts_with_authors_basic_forms:
        all_texts += texts_with_authors_basic_forms[key]
    return all_texts

def get_markov_models_dict(texts_per_author_basic_forms):
    markov_models = defaultdict(lambda: defaultdict(int))
    for author in authors:
        concatenated_texts = []
        for text in texts_per_author_basic_forms[author]:
            concatenated_texts += text.split()
        words_counts = defaultdict(int)
        for word in concatenated_texts:
            words_counts[word] += 1

        length_of_concatenated_texts = len(concatenated_texts)
        for i in range(length_of_concatenated_texts):
            if i == length_of_concatenated_texts - 1:
                break;
            markov_models[author][(words_indices[concatenated_texts[i]], words_indices[concatenated_texts[i + 1]])] = (
                    1 / words_counts[concatenated_texts[i]])
    return markov_models

def calculate_scores(texts_per_author_basic_forms, words_indices ):
    all_scores = defaultdict(list)
    for real_author in texts_per_author_basic_forms:
        books_list = list()
        for i in range(len(texts_per_author_basic_forms[real_author])):
            chosen_book = texts_per_author_basic_forms[real_author][i].split()
            words_counts = defaultdict(int)
            for word in chosen_book:
                words_counts[word] += 1

            chosen_book_markov_model = defaultdict(int)
            length_of_chosen_book = len(chosen_book)
            for i in range(length_of_chosen_book):
                if i == length_of_chosen_book - 1:
                    break;
                chosen_book_markov_model[(words_indices[chosen_book[i]], words_indices[chosen_book[i + 1]])] = (
                        1 / words_counts[chosen_book[i]])
            scores = defaultdict(int)
            for author in markov_models:
                indices_to_compare = set(markov_models[author]) | set(chosen_book_markov_model)
                for ind in indices_to_compare:
                    scores[author] += abs(chosen_book_markov_model[ind] - markov_models[author][ind])
            books_list.append(scores)
            print("Chosen book's real author: " + real_author)
            print("Differences in writing style:")

            for a in scores:
                print(a + ' <- ' + str(scores[a]))
            print('')
        all_scores[real_author] = books_list
    return all_scores

def calculate_metrics(all_scores):
    for real_author in all_scores:
        good = 0
        alls = 0
        for book in all_scores[real_author]:
            pred_author = min(book.items(), key=operator.itemgetter(1))[0]
            #         print('real author: ' + ra + '   pred author:' + pred_author)
            alls += 1
            if pred_author == real_author:
                good += 1
        print('Accuracy for ' + real_author + ' books: ' + str(good / alls))


if __name__ == '__main__':
    start = time.time()

    dictionary = create_dictionary(fullpath=os.path.join(path, fileToCreateDict))

    text_per_author = read_text_for_each_author(path)
    texts_per_author_basic_forms = get_text_per_author_with_basic_forms(text_per_author, re.compile('\w+'))

    all_texts = get_all_texts(texts_per_author_basic_forms)

    cv = CountVectorizer(token_pattern='(?u)\\b\\w+\\b')

    cv_freq_matrix = cv.fit_transform(all_texts)
    distinct_words = cv.get_feature_names()
    number_of_distinct_words = cv_freq_matrix.shape[1]
    words_indices = dict(zip(distinct_words, range(len(distinct_words))))

    markov_models = get_markov_models_dict(texts_per_author_basic_forms)
    all_scores = calculate_scores(texts_per_author_basic_forms, words_indices )

    calculate_metrics(all_scores)

    end = time.time()

    print(f'Time elapsed: {end-start}')

