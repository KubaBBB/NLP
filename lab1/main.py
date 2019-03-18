import collections
import time
from English import English
from Finnish import Finnish
from German import German
from Italian import Italian
from Polish import Polish
from Spanish import Spanish

n = 3;

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

if __name__ ==  '__main__':
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

    ### INPUT TEXT
    #input = input("What is your age? ")
    # print("You entered " + str(input))

    ### TEST TEXT
    input = "Oh, che ti succede amico? Hai fatto tutto come dovrebbe essere? Fuori piove";
    input_ngram = create_ngram(input,n);
    collection = collections.Counter(input_ngram);

    for lang in languages:
        lang.calculate_n_grams();
        lang.create_dictionary();
        lang.calculate_cos_norm(input_ngram)

    recognized_lang = get_lang_from_best_norm(languages);
    end = time.time()
    print("I recognize it as a: " + str(recognized_lang) + " language");
    print("I took me: " + str(end-start) + " seconds");
