from numba import njit
import numba
import numpy as np


class CountVectorizer:
    """The class can make the same as CountVectorizer from sklearn. Methods get_feature_names and fit_transform are
    realized """

    def __init__(self):
        self.unique_words = None
        self.prepared_corpus = None
        self.unique_words = None

    @staticmethod
    def _prepare_str(string):
        """
        :param string: some string
        :return: the same string that is lowered.
        All chars, unequal to eng/rus letters or numbers or '_' are replaced by spaces
        """
        for char in string:
            char = char.lower()
            # Hard to read conditions below works faster than create set of allowed chars
            # and check if char stay in this set
            if ord('a') <= ord(char) <= ord('z') or ord('0') <= ord(char) <= ord('9') or char == ' ' or \
                    char == '_' or ord('а') <= ord(char) <= ord('я'):
                pass
            else:
                string = string.replace(char, ' ')
        # Remove double spaces
        while '  ' in string:
            string = string.replace('  ', ' ')
        return string.lower()

    @staticmethod
    def _prepare_corpus(corpus):
        """
        :param corpus: initial corpus
        :return: Apply _prepare_str method to each string in corpus and split each string to list of words
        """
        # Use numpy for speedup
        ans = np.array([CountVectorizer._prepare_str(string) for string in np.array(corpus)])
        return list(np.char.split(ans))

    def _unique_words(self, corpus):
        """
        :param Corpus: prepared corpus
        :return: Unique words of len > 1 from prepared corpus
        """
        # 1. Transform _prepare_corpus(corpus) that is 2D list of words to 1D list
        # 2. Apply set() to leave only unique words
        # 3. Apply list to make list for further sort()
        self.prepared_corpus = CountVectorizer._prepare_corpus(corpus)
        uword_list = list(set(np.concatenate(self.prepared_corpus)))
        uword_list.sort()
        return [word for word in uword_list if len(word) > 1]

    def get_feature_names(self):
        """
        :return: Unique words of len > 1 from prepared corpus
        """
        return self.unique_words

    @staticmethod
    @njit
    def term_doc_matrix(uword_list, corpus):
        """
        :param  uword_list: _unique_words(corpus)
        :param corpus: prepared corpus
        :return: term-doc matrix
        Here we use numba to speedup matrix creation. We treat this operation as a static method
        because it is easier to apply numba only for one function rather than to all class. Below you can see steps
        1. Create a dict where key is a unique word and value is a number of the word. We have to use loop
        because numba does not support python dicts
        2. Create zero term-doc matrix
        3. Take a word from the corpus_prepared_str_to_list, find it in the dict and add 1 to
        the corresponding element of the matrix."""

        k = 0
        uwords_dict = {}
        for i in uword_list:
            uwords_dict[i] = k
            k = k + 1

        matrix = [[0] * len(uwords_dict)] * len(corpus)
        matrix = np.array(matrix)

        for j in range(len(corpus)):
            for i in range(len(corpus[j])):
                if len(corpus[j][i]) > 1:
                    matrix[j, uwords_dict[corpus[j][i]]] += 1
        return matrix

    def fit_transform(self, corpus):
        """
        :param corpus: prepared corpus
        :return: term-doc matrix
        1. We need this method to call term_doc_matrix that is @static method on @njit.
           Also, we convert required data to numba data type here
        2. We create nb_corpus that is numba 2D list
        3. We apply term_doc_matrix and get answer
        """
        self.unique_words = self._unique_words(corpus)
        nb_corpus = numba.typed.List()

        [nb_corpus.append(['']) if len(lst) == 0 else nb_corpus.append(lst)
         for lst in self.prepared_corpus]

        # for lst in CountVectorizer._prepare_corpus(corpus):
        #     if len(lst) == 0:
        #         nb_corpus.append([''])
        #     else:
        #         nb_corpus.append(lst)

        return self.term_doc_matrix(self.unique_words, nb_corpus)


# Below we provide a test. The first is accuracy test.
# For these purposes we use file wp.txt where part of the book 'War and Peace' is presented.
# We apply get_feature_names and fit_transform with argument wp[:n] (first n lines of the wp.txt).
# Further we compare result with the original one from sklearn.
# Note, the book contains over 28000 lines and more than 20000 different words.
# Further we provide speed test. We compare time of creating term-doc matrix via our class and sklearn realization.
if __name__ == '__main__':
    import warnings
    import time
    from sklearn.feature_extraction.text import CountVectorizer as SKCountVectorizer

    warnings.filterwarnings('ignore')

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
