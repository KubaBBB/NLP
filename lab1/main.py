import time
import re
from English import English
from Finnish import Finnish
from German import German
from Italian import Italian
from Polish import Polish
from Spanish import Spanish
import random

N = [2, 3, 4, 5, 6, 7];
path_to_test_file = "./data/test/";
test_files = ["engt.txt", "fin.txt", "ger.txt", "ita.txt", "pol.txt", "spa.txt"];

lang_collection = ["English", "Finnish", "German", "Italian", "Polish", "Spanish"]

num_of_right_lan = 12;
num_of_invalid = 7;

def create_ngram(input, n):
    vector = input.replace(" ", '');
    value = [];
    for index in range(len(vector)):
        chars = vector[index:index + n].lower();
        value.append(chars);

    return value

def get_lang_from_best_norm(languages):
    best = 0;
    best_lang = None;
    for lang in languages:
        if best == 0:
            best = lang.core.norm;
            best_lang = lang.__class__.__name__;
        if lang.core.norm < best:
            best = lang.core.norm;
            best_lang = lang.__class__.__name__;

    return best_lang;

def load_testing_set(file):
    fullpath = path_to_test_file + file
    test_set = []
    with open(fullpath, 'r') as f:
        if f != '\n':
            content = f.readlines();
            for row in content:
                clean_row = re.sub('[\\\n--,.\t]', '', row).lower()
                test_set.append(clean_row);
    return test_set;

if __name__ ==  '__main__':

    for n in N:
        start = time.time();
        ### Initialize
        eng = English(n);
        fin = Finnish(n);
        ger = German(n);
        ita = Italian(n);
        pol = Polish(n);
        spa = Spanish(n);

        languages = [];
        languages.append(eng);
        languages.append(fin);
        languages.append(ger);
        languages.append(ita);
        languages.append(pol);
        languages.append(spa);

        for lang in languages:
            lang.calculate_n_grams();
            lang.create_dictionary();

        true_positive = 0;
        false_positive = 0;
        true_negative = 0;
        false_negative = 0;

        for i in range(lang_collection.__len__()):
            actual_lang = lang_collection[i];
            test_set = load_testing_set(test_files[i]);
            #print(f'testing language: {actual_lang}')
            index = 0;
            for row in test_set:
                ngram = create_ngram(row, n);
                for lang in languages:
                    lang.calculate_cos_norm(ngram)
                recognized_lang = get_lang_from_best_norm(languages);
                #print(recognized_lang)
                if index < num_of_right_lan:
                    if recognized_lang == actual_lang:
                        true_positive +=1;
                    else:
                        false_negative+=1;
                elif index <= num_of_right_lan + num_of_invalid:
                    if recognized_lang == actual_lang:
                        false_positive +=1;
                    else:
                        true_negative +=1;
                index+=1;
            #print("")

        precision = true_positive / (true_positive+false_positive);
        recall = true_positive/(true_positive+false_negative);

        print(f'N: {n}')
        print(f'Precision: {precision}')
        print(f'Recall: {recall}')

        end = time.time()
        print("I took me: " + str(end-start) + " seconds");
        print("");
