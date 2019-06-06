
# coding: utf-8
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
import codecs
from collections import Counter, defaultdict
from matplotlib import pyplot as plt
import time

datasets_path = 'C:/Users/BOLSON-PC/Desktop/studia/IT/PJN/NLP/lab5'

with codecs.open(datasets_path + '/data/pap.txt', 'r', 'utf-8') as f:
    text = f.read().lower()
    preprocessed_text = re.sub(r'#\d+', '##', text)
    preprocessed_text = re.sub(r'\n', ' ', preprocessed_text)
    preprocessed_text = re.sub(r'[\\,.\-\'\"()?:;+\/\d+&`!\[\]@<>%*~{}=\x96\x84\x8c\x9c\x9f\x92\x80]', '', preprocessed_text)
    preprocessed_text = re.sub(r'[\xbc-\xff]', '', preprocessed_text)
    preprocessed_text = re.sub(r'   ', '  ', preprocessed_text)
    preprocessed_text = re.sub(r'  ', ' ', preprocessed_text)
    splitted_notes = np.array(preprocessed_text.split('##'))


tf = TfidfVectorizer(max_df=3000, min_df=6, token_pattern='(?u)\\b\\w+\\b')
freq_matr = tf.fit_transform(splitted_notes)
freq_matr

frequency_matrix = freq_matr.toarray()
chosen_note = frequency_matrix[2634].astype(bool)

start = time.time()
dice_similarity_vector = [pairwise_distances([chosen_note, note], metric='dice')[0][1] for note in frequency_matrix.astype(bool)]
print("Time:" + str(time.time() - start))

dice_distribution = Counter([metric for metric in dice_similarity_vector if metric != 1.0 and metric != 0.0])
plt.scatter(list(dice_distribution.keys()), list(dice_distribution.values()), s=9)
plt.show()


indices = dict()
indices['tfidf'] = list()
indices['graph3'] = list()
indices['graph4'] = list()
indices['graph5'] = list()
for i in range(len(dice_similarity_vector)):
    if dice_similarity_vector[i] < 0.86:
        indices['tfidf'].append(i)
print("Number of similar notes: " + str(len(indices['tfidf'])))


del frequency_matrix


cv = CountVectorizer(max_df=3000, min_df=6, token_pattern='(?u)\\b\\w+\\b')
cv_freq_matrix = cv.fit_transform(splitted_notes)
words = cv.get_feature_names()
occurence_number = cv_freq_matrix.sum(axis=0).A1
len(cv.stop_words_)
stop_list = cv.stop_words_

occurence_number, words = (list(t) for t in zip(*sorted(zip(occurence_number, words), reverse=True)))

cv_freq_matrix



def delete_banned_words(matchobj):
    word = matchobj.group(0)
    if word.lower() in banned_words:
        return ""
    else:
        return word

banned_words = stop_list
word_pattern = re.compile('\w+')
graph_notes = list()
for sentence in splitted_notes:
    graph_notes.append(word_pattern.sub(delete_banned_words, sentence).split())    


# In[45]:


encoder= {k: v for (k, v) in zip(words, range(len(words)))}


# In[46]:


def transform_from_words_note_to_graph_vector(graph_note, n):
    #note_matrix = np.zeros((len(words), len(words)))
    note_matrix_dict = defaultdict(int)
    note_len = len(graph_note)
    if note_len == n-4 or note_len == n-3 or note_len == n-2 or note_len == n-1:
        return defaultdict(int)
    for i in range(note_len):
        if i == note_len - (n -1):
            break;  
        for j in range(n-1):
            note_matrix_dict[(encoder[graph_note[i]], encoder[graph_note[i+1+j]])] += 1
    return note_matrix_dict


# In[47]:


chosen_note = transform_from_words_note_to_graph_vector(graph_notes[2634], 3)
dice_metric = list()
for note in graph_notes:
    test_note = transform_from_words_note_to_graph_vector(note, 3)
    X_Y = 0
    X = len(test_note)
    Y = len(chosen_note)
    for key in chosen_note:
        if key in test_note:
            X_Y += 1
    dice_metric.append(1-(2*X_Y/(X+Y)))

dice_distribution = Counter([metric for metric in dice_metric if metric != 1.0 and metric != 0.0])
plt.scatter(list(dice_distribution.keys()), list(dice_distribution.values()), s=9)
plt.show()


# In[48]:


for i in range(len(dice_metric)):
    if dice_metric[i] < 0.9999:
        indices['graph3'].append(i)
print("Number of similar notes: " + str(len(indices['graph3'])))


# In[49]:


chosen_note = transform_from_words_note_to_graph_vector(graph_notes[2634], 4)
dice_metric = list()
for note in graph_notes:
    test_note = transform_from_words_note_to_graph_vector(note, 4)
    X_Y = 0
    X = len(test_note)
    Y = len(chosen_note)
    for key in chosen_note:
        if key in test_note:
            X_Y += 1
    dice_metric.append(1-(2*X_Y/(X+Y)))

dice_distribution = Counter([metric for metric in dice_metric if metric != 1.0 and metric != 0.0])
plt.scatter(list(dice_distribution.keys()), list(dice_distribution.values()), s=9)
plt.show()


# In[50]:


for i in range(len(dice_metric)):
    if dice_metric[i] < 0.9999:
        indices['graph4'].append(i)
print("Number of similar notes: " + str(len(indices['graph4'])))


# In[51]:


chosen_note = transform_from_words_note_to_graph_vector(graph_notes[2634], 4)
dice_metric = list()
for note in graph_notes:
    test_note = transform_from_words_note_to_graph_vector(note, 4)
    X_Y = 0
    X = len(test_note)
    Y = len(chosen_note)
    for key in chosen_note:
        if key in test_note:
            X_Y += 1
    dice_metric.append(1-(2*X_Y/(X+Y)))

dice_distribution = Counter([metric for metric in dice_metric if metric != 1.0 and metric != 0.0])
plt.scatter(list(dice_distribution.keys()), list(dice_distribution.values()), s=9)
plt.show()


# In[52]:


for i in range(len(dice_metric)):
    if dice_metric[i] < 0.9999:
        indices['graph5'].append(i)
print("Number of similar notes: " + str(len(indices['graph5'])))


# In[56]:


all_indices = set()
for key in indices:
    for val in indices[key]:
        all_indices.add(val)


# In[60]:


all_indices


# In[62]:


for ind in all_indices:
    print('\n'+splitted_notes[ind])

