from Language import Language

path = "./data/";
files = ["polish1.txt", "polish2.txt", "polish3.txt"];


class Polish(Language):
    def __init__(self, n_len):
        self.core = Language(path, n_len);

    def calculate_n_grams(self):
        for file in files:
            self.core.open_and_remove_bad_chars(file);

    def create_dictionary(self):
        self.core.create_dictionary();

    def get_sorted_dict(self):
        return self.core.get_sorted_dict();

    def get_dict(self):
        return self.core.get_dict();

    def get_ngram_vec(self):
        return self.core.get_ngram_vec();

    def calculate_cos_norm(self, input_ngram):
        return self.core.calculate_cos_norm(input_ngram);

    def share_dataset(self):
        return self.core.share_dataset();