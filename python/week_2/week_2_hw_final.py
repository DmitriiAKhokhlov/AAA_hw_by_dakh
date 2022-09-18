from numba import njit
import numba
import numpy as np
import time


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
            if ord('a') <= ord(i) <= ord('z') or ord('0') <= ord(i) <= ord('9') or i == ' ' or i == '_' or ord(
                    'а') <= ord(i) <= ord('я'):
                pass
            else:
                s = s.replace(i, ' ')
        while '  ' in s:
            s = s.replace('  ', ' ')
        return s

    @staticmethod
    def _prepare_corpus(self, corp):
        """Apply _only_letters method to each string in corpus and split each string to list of words"""
        ans = np.array([self._only_letters(i) for i in np.array(corp)])
        ans = np.char.lower(ans)
        return list(np.char.split(ans))

    @staticmethod
    def _unique_w(self, corpus):
        """Create list of unique words from corpus"""
        s = list(set(list(np.concatenate(list(self._prepare_corpus(self, corpus))).flat)))
        s.sort()
        return [i for i in s if len(i) > 1]

    def get_feature_names(self):
        """Create set of words in the corpus."""
        return self._unique_w(self, self.corpus)

    @staticmethod
    @njit
    def mat(s, corp):
        """Here we use numba to speedup matrix creation. We treat this operation as a static method
        because it is easier to apply numba only for one function.
        1. Create a dict where key is a unique word and value is a number of the word. 2. Create
        zero term-doc matrix 3. take a word from the corpus_prepared_str_to_list, find it in the dict and add one to
        the corresponding element of the matrix. """

        k = 0
        unique_words = {}
        for i in s:
            if len(i) > 1:
                unique_words[i] = k
                k = k + 1

        matrix = [[0] * len(unique_words)] * len(corp)
        matrix = np.array(matrix)

        for j in range(len(corp)):
            for i in range(len(corp[j])):
                if len(corp[j][i]) > 1:
                    matrix[j, unique_words[corp[j][i]]] += 1
        return matrix

    def fit_transform(self, corpus):
        """ Here we calculate term-doc matrix"""
        self.corpus = corpus
        s = self._unique_w(self, corpus)

        co = self._prepare_corpus(self, corpus)
        nb_co = numba.typed.List()
        for lst in co:
            if len(lst) == 0:
                nb_co.append([''])
            else:
                nb_co.append(lst)

        return self.mat(s, nb_co)


# Below we provide a test. The first is accuracy test.
# For these purposes we use file wp.txt where part of the book 'War and Peace' is presented.
# We apply get_feature_names and fit_transform with argument wp[:n] (first n lines of the wp.txt).
# Further we compare result with the original one from sklearn.
# Note, the book contains over 28000 lines and more than 20000 different words.
# Further we provide speed test. We compare time of creating term-doc matrix via our class and sklearn realization.
if __name__ == '__main__':
    import warnings
    from sklearn.feature_extraction.text import CountVectorizer as SKCountVectorizer

    warnings.filterwarnings("ignore")

    fp = open(r'wp.txt', mode='r', buffering=-1, encoding=None,
              errors=None, newline=None, closefd=True, opener=None)
    wp = fp.readlines()

    v = CountVectorizer()

    skv = SKCountVectorizer()

    diff_el_matrix = np.sum(np.array(skv.fit_transform(wp[:1000]).toarray()) != np.array(v.fit_transform(wp[:1000])))
    print(
        f'Number of different elements in sklearn term-doc matrix and our realization is equal to {diff_el_matrix}')
    diff_el_words = sum(np.array(skv.get_feature_names_out()) != np.array(v.get_feature_names()))
    print(
        f'Number of different elements in sklearn unique words and our realization is equal to {diff_el_words}')

    if diff_el_words == 0 and diff_el_matrix == 0:
        print('Result of our realization is equal to realization in sklearn!')
    else:
        print('result of our realization is NOT equal to realization in sklearn!')

    print('--------------------------------')
    start = time.time()
    v.fit_transform(wp[:10000])
    end = time.time()
    print(f'Our realization takes {end - start} s to crate term-doc matrix')

    print('--------------------------------')
    start = time.time()
    skv.fit_transform(wp[:10000])
    end = time.time()
    print(f'Sklearn realization takes {end - start} s to crate term-doc matrix')
    print('--------------------------------')
