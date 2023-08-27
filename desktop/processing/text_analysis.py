"""Модуль анализа текста"""
import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer('sentence-transformers/LaBSE')
print('Инициализирована модель BERT')


def encoding(data_string: pd.Series):
    """
    Преобразование входных данных в числа

    :param data_string: Серия с данными о запросе
    :return: Результат обработки лингво-моделью
    """
    embeddings = MODEL.encode(data_string.values)
    return embeddings
