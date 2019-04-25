import time
from TextPreprocessor import TextPreprocessor
import Levenshtein
from numba import jit
import numpy as np

pathToFile = './data/'
lines = 'lines.txt'
clusters = 'clusters.txt'
limes = 12

def create_primary_clusters(path):
    fullPath = pathToFile + path;
    with open(fullPath, 'r', encoding='utf-8') as f:
        if f != '\n':
            content = f.readlines();
    return content;

def dice_coefficient(a, b):
    """dice coefficient 2nt/(na + nb)."""
    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0/(len(a_bigrams) + len(b_bigrams))

def pre_process_cluster(file):
    clusters = dict()
    index = 0;
    for item in file:
        if(item != '\n'):
            if(item == '##########\n'):
                index+=1;
            else:
                clusters[item] = index;
    return clusters;

def calculate_norm(string_array, lev_matrix, dice_matrix):
    for iterator in range(len(string_array)):
        row = string_array[iterator]

        for index in range(int(iterator+1/2)):
            lev = Levenshtein.distance(string_array[index], row)
            lev_matrix[index][iterator] = lev

            dice = dice_coefficient(string_array[index], row)
            dice_matrix[index][iterator] = dice;

if __name__ == '__main__':
    start = time.time();
    textProc = TextPreprocessor();
    l_test = np.array(['sdadadasda', 'sadadadaqweqe', 'sdadadadac'])
    m_test = np.zeros((3,3), dtype='int32');
    m_test2 = np.zeros((3,3), dtype='float32');

    calculate_norm(l_test, m_test, m_test2)
    l = textProc.open_and_filtr_file(lines)
    m_len = len(l);
    companies_array = np.asarray(l);
    lev_matrix = np.zeros((m_len, m_len), dtype='int32')
    dice_matrix = np.zeros((m_len, m_len), dtype='float32')

    #calculate_norm(companies_array, lev_matrix, dice_matrix)

    primary_clusters = create_primary_clusters(clusters);

    group_clusters = pre_process_cluster(primary_clusters);

    print(5)

    end = time.time()

    print(f'It took me: {end-start}')
