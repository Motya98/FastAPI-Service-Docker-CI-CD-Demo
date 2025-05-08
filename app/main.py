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
    """Метод управляет контейнером очистки и подготовки данных для обучения;
       метод управляет контейнером поиска лучших гиперпараметров моделей sklearn;
       метод управляет контейнером выбора наиболее точной прогнозной модели.
       """
    pod_prepared_data = Pods.call_pod_prepared_data()   # Запуск первого контейнера.
    return {'y_test': pod_prepared_data['y_test'].to_dict('records')}

class Pods:
    @staticmethod
    def call_pod_prepared_data() -> dict[str, pd.DataFrame]:
        """Контейнер выполняет очистку и подготовку данных для обучения.
                Returns: dict[str, pd.DataFrame] - X_train, X_test, y_train, y_test"""
        params = Parameter(**CRUDYaml.read('config.yaml'))
        with open('data/data.csv', 'rb') as file:
            files = {'file': ('data.csv', file, 'text/csv')}
            model_data = requests.post(
                                   f"http://prepared_data:8001/file_handler/"
                                       f"{params.number_of_x_columns}/"
                                       f"{params.number_of_y_columns}/"
                                       f"{params.random_seed}/"
                                       f"{params.test_size}/"
                                       f"{params.logical_cores}/"
                                       f"{params.lower_quantile}/"
                                       f"{params.upper_quantile}/"
                                       f"{params.degree}/",
                                       files=files
                                       )
        result_model_data = model_data.json()
        X_train, X_test = pd.DataFrame(result_model_data['X_train']), pd.DataFrame(result_model_data['X_test'])
        y_train, y_test = pd.DataFrame(result_model_data['y_train']), pd.DataFrame(result_model_data['y_test'])
        return {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}