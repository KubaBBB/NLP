from weighted_levenshtein import lev
import numpy as np
from textprocessor import TextProcessor

polish_lang_mapper = {'ą': 'A', 'ć': 'C', 'ę': 'E', 'ł': 'L', 'ó': 'O', 'ń': 'N', 'ś': 'S', 'ź': 'X', 'ż': 'Z'}

class BayesClassifier:
    def __init__(self):
        self.textprocessor = TextProcessor()
        self.low_weight = 0.001
        self.missclick_weight = 0.1
        self.insert_weight = 0.1
        self.delete_weight = 0.1

    def get_change_costs(self):
        low_weight = []
        low_weight.append((ord('a'), ord('A'))) # a -> ą
        low_weight.append((ord('c'), ord('C'))) # c -> ć
        low_weight.append((ord('e'), ord('E'))) # e -> ę
        low_weight.append((ord('l'), ord('L'))) # l -> ł
        low_weight.append((ord('o'), ord('O'))) # o -> ó
        low_weight.append((ord('n'), ord('N'))) # n -> ń
        low_weight.append((ord('s'), ord('S'))) # s -> ś
        low_weight.append((ord('z'), ord('X'))) # z -> ź
        low_weight.append((ord('z'), ord('Z'))) # z -> ż
        low_weight.append((ord('O'), ord('u'))) # ó -> u
        low_weight.append((ord('u'), ord('O'))) # u -> ó

        missclick = []
        missclick.append((ord('r'), ord('s'))) # sz -> rz
        missclick.append((ord('p'), ord('b'))) # p -> b
        missclick.append((ord('j'), ord('i'))) # j -> i
        missclick.append((ord('t'), ord('d'))) # t -> d
        missclick.append((ord('f'), ord('g'))) # f -> g
        missclick.append((ord('v'), ord('c'))) # v -> c
        missclick.append((ord('p'), ord('o'))) # p -> o
        missclick.append((ord('e'), ord('w'))) # e -> w

        change_costs = np.ones((128, 128), dtype=np.float64)
        for item in low_weight:
            change_costs[item[0], item[1]] = self.low_weight
        for item in missclick:
            change_costs[item[0],item[1]] = self.missclick_weight

        return change_costs

    def get_insert_cost(self):
        insert_char = []
        insert_char.append(ord('r'))
        insert_char.append(ord('c'))

        insert_costs = np.ones(128, dtype=np.float64)
        for item in insert_char:
            insert_costs[item] = self.insert_weight;

        return insert_costs;

    def get_delete_cost(self):
        delete_char = []
        delete_char.append(ord('r'))# rz -> ż
        delete_char.append(ord('c'))# ch -> h

        delete_costs = np.ones(128, dtype=np.float64)
        for item in delete_char:
            delete_costs[item] = self.delete_weight;

        return delete_costs;

    def calculate(self, wrong_word, words_dict):
        change_costs = self.get_change_costs()
        insert_costs = self.get_insert_cost()
        delete_costs = self.get_delete_cost()

        ### https://weighted-levenshtein.readthedocs.io/en/master/

        lev_dict = {cnd: lev(wrong_word, cnd, insert_costs=insert_costs,
                             delete_costs=delete_costs, substitute_costs=change_costs) for cnd in words_dict}

        top_rated = sorted(lev_dict.items(), key=lambda kv: kv[1])[:300] ### Dictionary -> Word : Levenstein metric
        ranking = [x[0] for x in top_rated]
        max_levenstein = max(top_rated, key=lambda vector: vector[1])[1]
        Pwc = [(x[0], 1 - x[1] / max_levenstein) for x in top_rated] ### sorted probability -> word : p

        dict_count = [(x, words_dict[x] + 1) for x in ranking]
        max_count = max(dict_count, key=lambda v: v[1])[1]

        Pc = [(x[0], x[1] / max_count) for x in dict_count]

        Pcw_probability = self.calculate_probability(Pwc=Pwc, Pc=Pc)

        return Pcw_probability


    def calculate_probability(self, Pwc, Pc):
        Pcw = []
        for index in range(len(Pwc)):
            word = self.textprocessor.map_chars(Pwc[index][0])
            probability = (Pwc[index][1] * Pc[index][1])/(Pwc.__len__()*Pc.__len__())
            Pcw.append((word, probability))
        return [x[0] for x in sorted(Pcw, key=lambda vector: vector[1], reverse=True)[:7]]