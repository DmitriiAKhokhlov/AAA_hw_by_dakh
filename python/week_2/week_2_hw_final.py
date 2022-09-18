import numpy as np


class CountVectorizer:
    """The class can make the same as CountVectorizer from sklearn. Methods get_feature_names and fit_transform are
    realized """

    def __init__(self):
        self.unique_words = None
        self.corpus = None

    @staticmethod
    def _only_letters(s):
        """Leave only eng letters in the argument string. Lower all letters."""
        for i in s:
            i = i.lower()
            if ord('a') <= ord(i) <= ord('z') or ord('0') <= ord(i) <= ord('9') or i == ' ':
                pass
            else:
                s = s.replace(i, ' ')
        while '  ' in s:
            s = s.replace('  ', ' ')
        return s

    @staticmethod
    def _prepare_corpus(self, corp):
        """Apply _only_letters method to each string in corpus"""
        c = []
        for i in corp:
            i.rstrip('\n')
            c.append(self._only_letters(i.lower()))
        return c

    def get_feature_names(self):
        """Create set of words in the corpus."""
        return list(self.unique_words.keys())

    def fit_transform(self, corpus):
        """1. Make from corpus new list corpus_prepared_str_to_list, that is 2D list, where each n line is list of
        words from n string 2. Create a dict where key is a unique word and value is a number of the word 3. Create
        zero term-doc matrix 4. take a word from the corpus_prepared_str_to_list, find it in the dict and add one to
        the corresponding element of the matrix. """
        self.corpus = corpus
        corpus_prepared = self._prepare_corpus(self, self.corpus)
        corpus_prepared_str_to_list = [i.split() for i in corpus_prepared]

        s = set({})
        for j in self.corpus:
            if self._only_letters(j.lower()) is not None:
                s = s.union(self._only_letters(j.lower()).split())
        s = list(s)
        s.sort()
        k = 0
        self.unique_words = {}
        for i in s:
            if len(i) > 1:
                self.unique_words[i] = k
                k = k + 1

        matrix = [[0] * len(self.unique_words)] * len(corpus_prepared_str_to_list)
        matrix = np.array(matrix)
        for j in range(len(corpus_prepared_str_to_list)):
            for i in range(len(corpus_prepared_str_to_list[j])):
                if len(corpus_prepared_str_to_list[j][i]) > 1:
                    matrix[j, self.unique_words[corpus_prepared_str_to_list[j][i]]] += 1
        return matrix


# Below we provide a test. For these purposes we use file wp.txt where part of the book 'War and Peace' is presented.
# We apply get_feature_names and fit_transform with argument wp[:n] (first n lines of the wp.txt).
# Further we compare result with the original one from sklearn.
# Note, the book contains over 28000 lines and more than 20000 different words.

if __name__ == '__main__':
    fp = open(r'wp.txt', mode='r', buffering=-1, encoding=None,
              errors=None, newline=None, closefd=True, opener=None)
    wp = fp.readlines()

    v = CountVectorizer()

    from sklearn.feature_extraction.text import CountVectorizer as SKCountVectorizer

    skv = SKCountVectorizer()

    diff_el_matrix = np.sum(np.array(skv.fit_transform(wp[0:1000]).toarray()) != np.array(v.fit_transform(wp[:1000])))
    print(
        f'Number of different elements in sklearn term-doc matrix and our realization is equal to {diff_el_matrix}')
    diff_el_words = sum(skv.get_feature_names_out() != v.get_feature_names())
    print(
        f'Number of different elements in sklearn unique words and our realization is equal to {diff_el_words}')

    if diff_el_words == 0 and diff_el_matrix == 0:
        print('Result of our realization is equal to realization in sklearn!')
    else:
        print('result of our realization is NOT equal to realization in sklearn!')
