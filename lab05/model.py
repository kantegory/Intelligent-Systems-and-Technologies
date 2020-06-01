from nltk.corpus import stopwords
from string import punctuation
import nltk
import pymorphy2
import db_intents

morph = pymorphy2.MorphAnalyzer()
# nltk.download('stopwords')
db = db_intents.Shelf()


def distance(a, b):
    """Считаем расстояние Левенштейна"""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


class Tokenizer:

    def __init__(self, message):
        self.message = message.lower()
        self.tokens = set()
        self.t = []
        self.prob = {'advice': 0, 'problem': 0, 'appointment': 0, 'other': 0}

    """ Генерируем ngramm для обработанного текста"""
    def ngrams(self, key, n=3, k=4):
        if len(key) < k:
            n = len(key)
            k = len(key)
        for i in range(len(key) - k + 1):
            self.gen_collocation(key[i:i + k], n)

    def gen_collocation(self, arr, n):
        self.tokens.add(' '.join(self.t))
        if len(self.t) == n:
            return
        else:
            for i in range(len(arr)):
                self.t.append(arr[i])
                self.gen_collocation(arr[:i] + arr[i + 1:], n)
                self.t.pop()

    def normalization(self):
        """Удаляем знаки пунктуации, стоп слова и ненужные части речи. Генерируем токены"""
        del_punct = ''.join(c for c in self.message if c not in punctuation).split(' ')
        w = [word for word in del_punct if word not in stopwords.words('russian')]

        # Проверяем слова на ошибки
        temp = [morph.parse(word)[0].normal_form for word in w if
                morph.parse(word)[0].tag.POS not in {'NPRO', 'INTJ', 'PRCL',
                                                     'CONJ', 'PREP', 'PRED', 'NUMR'}]
        # for elem in temp:
        #     for key in keys:
        #         if distance(elem, key) == 1:
        #             elem = key

        self.ngrams(temp)
        self.t = []

    def probably_intent(self):
        for key in self.prob:
            temp = db.get(key)
            for token in self.tokens:
                if token in temp:
                    self.prob[key] += 1
        s = 0
        for key in self.prob:
            s += self.prob[key]
        if s == 0:
            self.prob['other'] = 1.0
        else:
            for key in self.prob:
                self.prob[key] /= s

        return self.prob


# mes = 'Скажите пожалуйста, могу ли я записаться к терапевту на завтра? И работают ли у вас детские стоматологи?
# T = Tokenizer(mes)
# T.normalization()
# print(T.probably_intent())
