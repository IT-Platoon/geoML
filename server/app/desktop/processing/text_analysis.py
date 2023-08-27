import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer('sentence-transformers/LaBSE')
print('Инициализировано')


def encoding(data_string: pd.Series):
    """


    :param data_string:
    :return:
    """
    embeddings = MODEL.encode(data_string.values)
    return embeddings
