import time;
from textprocessor import TextProcessor
from bayes_classifier import BayesClassifier

form_file = 'formy'
polish_texts = ['dramat', 'popul', 'proza', 'publ', 'wp']
path_to_files = './data/'
show_simmilar = True;
num_of_simmilar = 4

if __name__ == '__main__':
    textprocessor = TextProcessor()
    textprocessor.create_dictionary(path_to_file = path_to_files, form_file=form_file)
    textprocessor.improve_dictionary(path_to_files = path_to_files, polish_texts=polish_texts)
    dict_of_words = textprocessor.dict_of_words;

    input_word = input('Napisz pojedyncze slowo:\n')
    start = time.time();
    input_word = textprocessor.map_chars(input_word)
    if not input_word in dict_of_words:
        bayes_classifier = BayesClassifier()
        simmilar_words = bayes_classifier.calculate(f'{input_word}', dict_of_words)
        unmapped_words = []
        for word in simmilar_words:
            unmapped_words.append(textprocessor.unmap_words(word))
        print(f'Slowo nie wystepuje w polskim jezyku.')
        print(f'Moze chodzilo o \'{unmapped_words[0]}\'?')
        show_hints = input('Chcesz zobaczyc inne mozliwosci? t/n\n')
        if(show_hints == 't'):
            print(f'Inne możliwosci {unmapped_words[1:num_of_simmilar]}\n')
    else:
        print(f'Slowo {input_word} wystepuje w polskim jezyku.')

    end = time.time()
    print(f'Czas egzekucji: {end-start}')
