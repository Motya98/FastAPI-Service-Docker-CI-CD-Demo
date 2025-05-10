from typing import Any

from fastapi import FastAPI
import requests

from decorators import logger_method
from variables import logger, get_params


app = FastAPI()
params = get_params()


@app.get("/")
@logger_method(logger)
def read_root() -> dict[Any, Any]:
    """Контейнер управляет:
            Контейнером подготовки данных для обучения;
            Контейнером обучения ML моделей;
       """
    pod_prepared_data = Pods.call_pod_prepared_data()   # Запуск первого контейнера.
    pod_predicted_data = Pods.call_pod_predicted_data(pod_prepared_data)    # Запуск второго контейнера.
    return pod_predicted_data


class Pods:
    """Содержит методы вызова контейнеров."""
    @staticmethod
    @logger_method(logger)
    def call_pod_prepared_data() -> dict[str, list[dict[str, Any]]]:
        """Контейнер выполняет очистку и подготовку данных для обучения.
                Returns: dict.
                    X_train, X_test, y_train, y_test."""
        with open(params.relative_data_path, 'rb') as file:
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
        return model_data.json()    # X_train, X_test, y_train, y_test

    @staticmethod
    @logger_method(logger)
    def call_pod_predicted_data(pod_prepared_data) -> dict:
        """Контейнер обучает ML-модели; подбирает гиперпараметры; выбирает лучшую ML модель.
                Returns: dict.
                    best_params_."""
        model_data = requests.post(
                               f"http://predicted_data:8002/file_handler/"
                                   f"{params.cv}/"
                                   f"{params.scoring}/"
                                   f"{params.logical_cores}/",
                                   params={'list_names_models': params.list_names_models},
                                   json=pod_prepared_data
                                   )
        return model_data.json()
