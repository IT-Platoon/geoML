"""Константы, описывающие пути до файлов"""

import os
from pathlib import Path

MODEL_PATH = os.path.join(Path(__file__).parents[1], "model", "base_data.pkl")
DATA_PATH = os.path.join(Path(__file__).parents[1], "data_baseline", "valid_data", "test_example.csv")
BUILDINGS_DB_PATH = os.path.join(Path(__file__).parents[1], "data_baseline", "additional_data", "building_20230808.csv")
