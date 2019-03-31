from DictionaryPL import DictionaryPL
from BookProcessor import BookProcessor
import time
import operator
import matplotlib.pyplot as plt

pathToDict = "./data/odm.txt"
pathToBook = "./data/potop.txt"

axisLen = 50;

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


    ### ZIPF

    sorted_ranking = book.sorted_ranking()
    zipf = sorted_ranking[0:axisLen]

    zipf_ranking = dict();
    for item in zipf:
        zipf_ranking[item[0]] = item[1];

    plt.figure(figsize=(15,10))
    plt.plot(zipf_ranking.keys(), zipf_ranking.values(), 'bo-')
    plt.xticks(rotation=90)

    #plt.show()
    plt.savefig('Zipf1.png');
    plt.close()

    sumOfWords = sum(zipf_ranking.values())
    zipf2 = {k: 100* v / sumOfWords for total in (sum(zipf_ranking.values()),) for k, v in zipf_ranking.items()}

    sorted_zipf2 = sorted(zipf2.items(), key=operator.itemgetter(1))
    zipf2_ranking=dict()
    for item in sorted_zipf2:
        zipf2_ranking[item[0]] = item[1];

    plt.figure(figsize=(15,10))
    plt.plot(zipf2_ranking.keys(), zipf2_ranking.values(), 'mo-')
    plt.xticks(rotation=90)
    #plt.show()
    plt.savefig('Zipf2.png')


    ### MANDELBROT


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
    for item in digram:
        digram_rank[item[0]] = item[1];
    for item in trigram:
        trigram_rank[item[0]] = item[1];

    # digram_list = []
    # for key, value in digram_rank.iteritems():
    #     temp = [key, value]
    #     digram_list.append(temp)
    #
    # digram_statistic = digram_rank[0:axisLen]
    plt.figure(figsize=(15,10))
    plt.plot(digram[0:axisLen].keys(), digram[0:axisLen].values(), 'bo-')
    plt.xticks(rotation=90)
    plt.show()
    end = time.time()
    print(f'It took me: {end-start}')
    a =5.0



