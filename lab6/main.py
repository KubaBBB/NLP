import time;
import numpy as np
from textprocessor import TextProcessor
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer


def get_stop_list():
        return ['sp', 'llc', 'co', 'ltd', 'tel', 'email', ' ', 'tel', 'fax', 'gmail',
                'com', 'eu', 'pl', 'telfax', 'office', 'burg', 'poland']

fileName = "./data/pap.txt"
note_idx = 155


#https://www.datascienceassn.org/sites/default/files/users/user1/lsa_presentation_final.pdf?fbclid=IwAR3ax6JNemqmWzfau24-UwePT7isOEDP5mAE3jbCQG92dITVVwV9ZS7CYiA

if __name__ == '__main__':
    start = time.time();

    ### PREPROCESSING

    textProcessor = TextProcessor()
    textProcessor.create_dictionary("data", "odm.txt")

    lineWords = []
    for line in open(fileName, 'r', encoding='utf-8'):
        read_line = line.replace('#', '').strip('\n').strip(' ')
        if not read_line.isdigit():
            lineWords.append(textProcessor.preprocess(read_line))

    ### Document-term matrix

    stop_list = get_stop_list()
    ct_vectorizer = CountVectorizer(min_df=1, stop_words=stop_list)
    tdtf = TfidfVectorizer()

    dtm = ct_vectorizer.fit_transform(lineWords)
    feature_names = ct_vectorizer.get_feature_names()[:10]

    ### Singular value decomposition and LSA - could use arpack algorithm
    lsa = TruncatedSVD(100, algorithm='randomized')

    dtm_lsa = lsa.fit_transform(dtm)
    dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)

    ### NOTE
    dtm_matrix1 = np.asmatrix(dtm_lsa)
    dtm_matrix2 = np.asmatrix(dtm_lsa).T[:,note_idx]

    similarity = np.asarray(dtm_matrix1 * dtm_matrix2)

    indexes = np.where(similarity > 0.98)
    print(f'Note: {lineWords[note_idx]}')
    ar = indexes[0]
    for item in indexes[0]:
        print(f'Familar note: {lineWords[item]}')
    end_time = time.time()
    print(f'Elapsed {end_time-start}')
