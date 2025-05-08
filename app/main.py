import pandas as pd
from fastapi import FastAPI
import requests

from yaml_ import CRUDYaml
from parameters import Parameter
from decorators import logger_method
from variables import logger


app = FastAPI()

@app.get("/")
@logger_method(logger)
def read_root() -> dict:
    """Метод управляет контейнером для очистки и подготовки данных для обучения;
       метод управляет контейнером для поиска лучших гиперпараметров моделей sklearn;
       метод управляет контейнером для выбора наиболее точной прогнозной модели.
       """
    params = Parameter(**CRUDYaml.read('config.yaml'))
    with open('data/data.csv', 'rb') as file:
        files = {'file': ('data.csv', file, 'text/csv')}
        model_data = requests.post(f"http://file_handler:8001/file_handler/"
                                 f"{params.number_of_x_columns}/"
                                 f"{params.number_of_y_columns}/"
                                 f"{params.random_seed}/"
                                 f"{params.test_size}/"
                                 f"{params.logical_cores}/"
                                 f"{params.lower_quantile}/"
                                 f"{params.upper_quantile}/"
                                 f"{params.degree}/",
                                 files=files)
    result_model_data = model_data.json()
    X_train, X_test = pd.DataFrame(result_model_data['X_train']), pd.DataFrame(result_model_data['X_test'])
    y_train, y_test = pd.DataFrame(result_model_data['y_train']), pd.DataFrame(result_model_data['y_test'])
    return {'y_test': y_test.to_dict('records')}
