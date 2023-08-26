from nltk.tokenize import word_tokenize  # для токенизации по словам

import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

PATTERNS = "[A-Za-z!#$%&'()*+/:;,.<=>?@[\]^_`{|}~\"\-]+"

_stopwords_ru = stopwords.words("russian")
stopwords_ru = {}
for word in _stopwords_ru:

    if len(word) in stopwords_ru:
        stopwords_ru[len(word)].add(word)
    else:
        stopwords_ru[len(word)] = {word}

morph = MorphAnalyzer()


def lemmatize(doc) -> str:
    """


    :param doc:
    :return:
    """
    doc = re.sub(PATTERNS, ' ', doc)
    tokens = []

    for token in word_tokenize(doc):

        count = len(token)
        if token and not (count in stopwords_ru and token in stopwords_ru[count]):
            # TODO Упрощение обработки токена

            token = ' ' + token + ' '

            token = token.replace(' д ', 'дом').replace(' ул ', 'улица').replace(' г ', 'город')
            token = token.replace('д.', 'дом').replace('ул.', 'улица').replace('г.', 'город')

            token = token.strip()
            token = token.lower()

            # Убираю индексы
            if token.isdigit() and count == 6:
                continue

            if count > 2:
                token = morph.normal_forms(token)[0]

            tokens.append(token)

    string = ' '.join(tokens)
    return string
