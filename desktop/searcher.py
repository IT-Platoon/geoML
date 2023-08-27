"""Модуль поиска адреса в справочнике"""
import pickle
from typing import Optional
from collections import Counter

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean

from desktop.processing.text_normalization import lemmatize
from desktop.processing.text_analysis import encoding

from desktop.constants import (
    EXIT_CODES,
    RESPONSE_COUNT,
    BEST_COUNT,
    SINGLE_COUNT,
    MODEL_PATH,
    DATA_PATH,
    DATA_TEST_PATH,
    BUILDINGS_DB_PATH,
)

import time


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

    for target_building_id in base_data.keys():
        for emb in base_data[target_building_id]:
            similarity = euclidean(embedding, emb)

            lst_target_building_id.append(target_building_id)
            lst_value.append(similarity)

    df_result = pd.DataFrame(
        {
            'target_building_id': lst_target_building_id,
            'value': lst_value,
        }
    )
    df_result = df_result.sort_values(by=['value'], ascending=False)
    df_result = df_result.head(k_best)

    return df_result


def get_similarity_df_one(base_data: dict,
                          embedding: np.array,
                          k_best: int) -> pd.DataFrame:
    """
    Сравнение текущего эмбеддинга с базой данных и поиск k-подходящих адресов

    Данная функция берёт только один вариант для каждого идентификатора

    :param base_data: Словарь-справочник адресов
    :param embedding: Результаты преобразований
    :param k_best: Количество результатов, которые необходимо вывести
    :return: Фрейм данных с результатами работы модели
    """

    lst_target_building_id = []
    lst_value = []

    for target_building_id in base_data.keys():
        emb = base_data[target_building_id][0]
        similarity = euclidean(embedding, emb)

        lst_target_building_id.append(target_building_id)
        lst_value.append(similarity)

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
            embeddings: pd.DataFrame,
            responses: int = RESPONSE_COUNT) -> Optional[pd.DataFrame]:
    """
    Проверка адреса в справочнике

    :param base_data: Словарь-справочник адресов
    :param embeddings: Мера схожести
    :param responses: Количество возможных вариантов для вывода
    :return: Фрейм с найденными совпадениями
    """
    df = None

    for emb in embeddings:
        df = get_similarity_df_one(base_data, emb, responses)
        break  # Пройдём 1 раз

    return df


def get_report_dataframe(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Создание фрейма данных для отчёта

    :param df: Фрейм данных pandas
    :param columns: Колонки, которые используются в отчёте
    :return: Фрейм данных pandas только с нужными колонками
    """
    return df[columns]


def save_id_csv(df: pd.DataFrame,
                filename: str = 'test_id_predictions.csv') -> None:
    """
    Сохранение фрейма данных в файл с расширением .csv

    :param df: Фрейм данных pandas
    :param filename: Название файла сохранения
    :return: None
    """
    report = get_report_dataframe(df, ['id', 'predicted'])
    report = report.rename(columns={
        "predicted": "target_building_id",
    })
    report.to_csv(path_or_buf=filename, encoding='utf-8', sep=';', index=False)


def get_addresses(base_data: dict,
                  address: Optional[str] = None,
                  responses: int = RESPONSE_COUNT) -> pd.DataFrame:
    """
    Сохранение фрейма данных в файл с расширением .csv

    :param base_data: Словарь-справочник адресов
    :param address: Пользовательский ввод адреса
    :param responses: Количество возможных вариантов
    :return: None
    """
    buildings_id = find_address(base_data, address, responses=responses)
    target_id = list(buildings_id['target_building_id'])

    buildings_db = pd.read_csv(BUILDINGS_DB_PATH)
    addresses = [
        list(buildings_db.loc[buildings_db.id == target]['full_address'])[0]
        for target in target_id
    ]

    report = pd.DataFrame({'target_building_id': target_id, 'target_address': addresses})
    return report


def unification(df: pd.DataFrame,
                accomplishment: bool = False) -> pd.DataFrame:
    """
    Унификация вывода

    :param df: Фрейм данных для унификации
    :param accomplishment: Необходимость выполнения
    :return: Унифицированный фрейм данных
    """
    if accomplishment:
        id_results = list(df['target_building_id'])
        freq_id = Counter(id_results).most_common()[0][0]
        df = df.loc[df['target_building_id'] == freq_id].head(1)
    else:
        df = df.head(1)
    return df


def full_find_address(model_path: str,
                      address: Optional[str] = None,
                      responses: int = RESPONSE_COUNT) -> Optional[pd.DataFrame]:
    """
    Весь процесс поиска адреса по справочнику

    :param model_path: Путь до модели-справочника
    :param address: Пользовательский ввод адреса
    :param responses: Количество возможных вариантов
    :return:
    """
    if responses < 1:
        raise ValueError('Недопустимое количество результатов')

    print(f'Запуск модели по пути {model_path}')
    try:
        with open(model_path, 'rb') as f:
            base_data = pickle.load(f)
        print('Модель загружена')
    except FileNotFoundError:
        print(f'Модель не существует')
        exit(EXIT_CODES[FileNotFoundError])
    if address is None:
        try:
            address = input('Введите адрес: ')
        except KeyboardInterrupt:
            print('\nЗапущен процесс выхода')
            exit(EXIT_CODES[KeyboardInterrupt])

    token_string = lemmatize(address)

    embeddings = encoding(pd.Series(token_string))

    result = checker(base_data, embeddings, responses=responses)
    return result


def find_address(base_data: dict,
                 address: Optional[str] = None,
                 responses: int = RESPONSE_COUNT) -> Optional[pd.DataFrame]:
    """
    Поиск адреса по справочнику

    :param base_data: Словарь-справочник адресов
    :param address: Пользовательский ввод адреса
    :param responses: Количество возможных вариантов
    :return:
    """
    if responses < 1:
        raise ValueError('Недопустимое количество результатов')
    if address is None:
        try:
            address = input('Введите адрес: ')
        except KeyboardInterrupt:
            print('\nЗапущен процесс выхода')
            exit(EXIT_CODES[KeyboardInterrupt])

    token_string = lemmatize(address)

    embeddings = encoding(pd.Series(token_string))

    check_time = time.time()
    result = checker(base_data, embeddings, responses=responses)
    result['address'] = address
    print(f'Время поиска результатов: {time.time() - check_time}')
    return result


def start_search_csv(model_path: str) -> pd.DataFrame:
    """
    Поиск всех указанных в csv-файле адресов

    :param model_path: Путь до модели-справочника
    :return: Фрейм с предсказанием и истинным значением
    """
    print(f'Запуск модели по пути {model_path}')
    try:
        with open(model_path, 'rb') as f:
            base_data = pickle.load(f)
        print('Модель загружена')
    except FileNotFoundError:
        print(f'Модель не существует')
        exit(EXIT_CODES[FileNotFoundError])

    df = pd.DataFrame(columns=['address', 'target_building_id', 'value'])
    valid = pd.read_csv(
        DATA_TEST_PATH,
        sep=';',
        encoding='utf-8',
        encoding_errors='ignore',
        on_bad_lines='skip',
    )

    valid_id, valid_addresses, valid_target_id = (
        valid['id'].astype('int'),
        list(valid['address']),
        valid['target_building_id'].astype('int'),
    )

    # Обрежем данные для упрощения процесса
    valid_id, valid_addresses, valid_target_id = (
        valid_id[:1500],
        valid_addresses[:1500],
        valid_target_id[:1500],
    )

    addresses_counter = 0
    count_addresses = len(valid_addresses)
    for address in valid_addresses:
        building = find_address(base_data, address, responses=RESPONSE_COUNT)
        building = unification(building)
        df = pd.concat([df, building], ignore_index=True)
        addresses_counter += 1
        print(f'{addresses_counter}/{count_addresses} адресов пройдено')
    df.reset_index()

    results = pd.DataFrame(
        {
            'id': valid_id,
            'address': df['address'],
            'predicted': df['target_building_id'],
            'target': valid_target_id
        }
    )
    del df

    save_id_csv(results)

    return results


if __name__ == "__main__":
    print(f'Результат работы:\n{start_search_csv(MODEL_PATH)}')
    """try:
        with open(MODEL_PATH, 'rb') as f:
            guide = pickle.load(f)
        print('Модель загружена')
    except FileNotFoundError:
        print(f'Модель не существует')
        exit(EXIT_CODES[FileNotFoundError])
    print(get_addresses(guide, 'Санкт-Петербург, Яхтеная у. 18-16-4'))"""
    # print(f'Результат работы:\n{find_address(MODEL_PATH)}')
