class DictionaryPL:
    def __init__(self, path):
        self.pathToFile = path;
        self.dictionary = dict();

    def read_rules(self):
        with open(self.pathToFile, 'r', encoding='utf-8') as f:
            if f != '\n':
                content = f.readlines();
        content = [x for x in content if x != '\n']

        self.content = clean_rows(content);

    def create_dictionary(self):
        for row in self.content:
            listOfWords = row.split();
            for word in listOfWords:
                self.dictionary[word] = listOfWords[0];

def clean_rows(content):
        return [x.lower().replace(',', '').replace('\n', '') for x in content];