"""Константы, описывающие пути до файлов"""

import os
from pathlib import Path

MODEL_PATH = os.path.join(Path(__file__).parents[1], "model", "base_data.pkl")
