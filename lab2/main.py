from DictionaryPL import DictionaryPL
from BookProcessor import BookProcessor
import time
import operator
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy  import array
import numpy as np

pathToDict = "./data/odm.txt"
pathToBook = "./data/potop.txt"

axisLen = 50;

def mandelbrot_func(x, P, d, B):
    return P/((x+d)**B)

def zipf_func(x,k):
    return k/x;

def sort_dict_by_value(dict):
    return sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

if __name__ ==  '__main__':
    start = time.time();

    ### BASIC FORM

    dic = DictionaryPL(pathToDict)
    dic.read_rules()
    dic.create_dictionary()

    book = BookProcessor(pathToBook, dic.dictionary)
    book.read_book()
    book.create_ranking()

    print(f'total words: {book.totalWords}')
    print(f'invalid words: {book.invalidWords}')


    ### Ocurrance

    sorted_ranking = book.sorted_ranking()
    zipf = sorted_ranking[0:axisLen]
    zipf_vec = []
    zipf_ranking = dict();
    for item in zipf:
        zipf_ranking[item[0]] = item[1];
        zipf_vec.append(item[1])

    plt.figure(figsize=(15,10))
    plt.plot(zipf_ranking.keys(), zipf_ranking.values(),  'bo-',markersize=3, label = 'In text')
    plt.xticks(rotation=90)


    ### Zipf
    x = [_+1 for _ in range(axisLen)]
    popt, pcov = curve_fit(zipf_func, x, zipf_vec)
    y_zipf = [zipf_func(_, popt) for _ in x];
    plt.plot(x, y_zipf, 'ro-', markersize=3, label='Zipf k/x')

    ### Mandelbrot

    mandt, mandcov  = curve_fit(mandelbrot_func, x, zipf_vec, p0=[0, 0, 0])
    y_mandel = [mandelbrot_func(_, mandt[0], mandt[1], mandt[2]) for _ in x];
    plt.plot(x, y_mandel, 'yo-', markersize=3, label='Mandelbrot')

    mandel_array = array(y_mandel)
    zipf_array = array(y_zipf)
    real_array = array(zipf_vec)
    mse_mandel = np.square(np.subtract(mandel_array, real_array)).mean()
    mse_zipf = np.square(np.subtract(zipf_array, real_array)).mean()

    print(f'MSE Mandelbrot: {mse_mandel}')
    print(f'MSE Zipf: {mse_zipf}')

    plt.legend()
    plt.show()
    plt.savefig('Zipf1.png');
    plt.close()

    ### HAPAX * 50%

    hapax = book.count_hapax_logomena()
    print(f'Number of hapax logomena: {hapax}')

    half_text = book.words_of_half_text(sorted_ranking)
    print(f'words of 50% text: {half_text}')


    ### NGRAM statistic

    book.create_ngram_dict()
    digram = sort_dict_by_value(book.digram_dict)
    trigram = sort_dict_by_value(book.trigram_dict)

    digram_rank = dict()
    trigram_rank = dict()
    for index in range(axisLen):
        digram_rank[digram[index][0]] = digram[index][1];
        trigram_rank[trigram[index][0]] = trigram[index][1];

    plt.figure(figsize=(15,10))
    plt.plot(digram_rank.keys(), digram_rank.values(), 'bo-', markersize=3)
    plt.xticks(rotation=90)
    plt.show()

    plt.figure(figsize=(15,10))
    plt.plot(trigram_rank.keys(), trigram_rank.values(), 'bo-', markersize=3)
    plt.xticks(rotation=90)
    plt.show()

    end = time.time()
    print(f'It took me: {end-start}')
    a =5.0



