import pickle
import os
import sys
from typing import Optional

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .processing.text_normalization import lemmatize
from .processing.text_analysis import encoding

from .constants import (
    EXIT_CODES,
    RESPONSE_COUNT,
    BEST_COUNT,
)

import time

ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
MODEL_PATH = os.path.join(ROOT_PATH, "model", "base_data.pkl")


def get_similarity_df(base_data: dict,
                      embedding: np.array,
                      k_best: int) -> pd.DataFrame:
    """
    Сравнение текущего эмбеддинга с базой данных и поиск k-подходящих адресов

    :param base_data: Словарь-справочник адресов
    :param embedding: Результаты преобразований
    :param k_best: Количество результатов, которые необходимо вывести
    :return: Фрейм данных с результатами работы модели
    """

    lst_target_building_id = []
    lst_value = []

    # Опишем счётчики

    keys_counter = 0
    count_keys = len(base_data.keys())

    for target_building_id in base_data.keys():
        emb_counter = 0
        count_emb = len(base_data[target_building_id])

        for emb in base_data[target_building_id]:
            # value = cosine_similarity([embedding], [emb])[0][0]
            similarity = np.dot(embedding, emb) / (np.linalg.norm(embedding) * np.linalg.norm(emb))

            lst_target_building_id.append(target_building_id)
            # lst_value.append(value)
            lst_value.append(similarity)

            emb_counter += 1
            # print(f'Embeddings: {emb_counter}/{count_emb} done')

        keys_counter += 1
        # print(f'Targets: {keys_counter}/{count_keys} done')

    df_result = pd.DataFrame(
        {
            'target_building_id': lst_target_building_id,
            'value': lst_value,
        }
    )
    df_result = df_result.sort_values(by=['value'], ascending=False)
    df_result = df_result.head(k_best)

    return df_result


def get_similarity_df_unified(base_data: dict,
                              embedding: np.array,
                              k_best: int) -> pd.DataFrame:
    """
    Сравнение текущего эмбеддинга с базой данных и поиск k-подходящих адресов

    Данная функция берёт унифицированный адрес для одного идентификатора

    :param base_data: Словарь-справочник адресов
    :param embedding: Результаты преобразований
    :param k_best: Количество результатов, которые необходимо вывести
    :return: Фрейм данных с результатами работы модели
    """

    lst_target_building_id = []
    lst_value = []

    # Опишем счётчики

    keys_counter = 0
    count_keys = len(base_data.keys())

    for target_building_id in base_data.keys():
        emb_counter = 0
        count_emb = len(base_data[target_building_id])

        emb = base_data[target_building_id][0]
        # value = cosine_similarity([embedding], [emb])[0][0]
        similarity = np.dot(embedding, emb) / (np.linalg.norm(embedding) * np.linalg.norm(emb))

        lst_target_building_id.append(target_building_id)
        # lst_value.append(value)
        lst_value.append(similarity)

        emb_counter += 1
        print(f'Embeddings: {emb_counter}/{count_emb} done')

        keys_counter += 1
        print(f'Targets: {keys_counter}/{count_keys} done')

    df_result = pd.DataFrame(
        {
            'target_building_id': lst_target_building_id,
            'value': lst_value,
        }
    )
    df_result = df_result.sort_values(by=['value'], ascending=False)
    df_result = df_result.head(k_best)

    return df_result


def checker(base_data: dict,
            embeddings: pd.DataFrame) -> Optional[pd.DataFrame]:
    """


    :param base_data:
    :param embeddings:
    :return:
    """
    score = 0  # TODO Использование переменной
    df = None

    for emb in embeddings:
        df = get_similarity_df(base_data, emb, RESPONSE_COUNT)
        break  # Пройдём 1 раз

    return df


def find_address(model_path: str, address: Optional[str] = None) -> Optional[pd.DataFrame]:
    """


    :param model_path:
    :param address: Пользовательский ввод адреса
    :return:
    """
    print(f'Запуск модели по пути {model_path}')
    load_model_time = time.time()
    try:
        with open(model_path, 'rb') as f:
            base_data = pickle.load(f)
        print('Модель загружена')
    except FileNotFoundError:
        print(f'Модель не существует')
        exit(EXIT_CODES[FileNotFoundError])
    print(f'Время загрузки модели: {time.time() - load_model_time}')

    if address is None:
        input_time = time.time()
        try:
            address = input('Введите адрес: ')
        except KeyboardInterrupt:
            print('\nЗапущен процесс выхода')
            exit(EXIT_CODES[KeyboardInterrupt])
        print(f'Время ввода: {time.time() - input_time}')

    lemma_time = time.time()
    token_string = lemmatize(address)
    print(f'Время лемматизации: {time.time() - lemma_time}')

    emb_time = time.time()
    embeddings = encoding(pd.Series(token_string))
    print(f'Время создания эмбеддингов: {time.time() - emb_time}')

    check_time = time.time()
    result = checker(base_data, embeddings)
    print(f'Время поиска результатов: {time.time() - check_time}')
    return result


if __name__ == "__main__":
    func_time = time.time()
    print(f'Результат работы:\n{find_address(MODEL_PATH)}')
    print(f'Время работы: {time.time() - func_time}')
