from typing import List, Any
import multiprocessing

import pandas as pd
import numpy as np
from fastapi import FastAPI, Query, Body
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error

from decorators import logger_method
from variables import logger
import ml_models


app = FastAPI()


@app.post(
          '/file_handler/'
          '{cv}/'
          '{scoring}/'
          '{logical_cores}/'
          )
@logger_method(logger)
def predict_data(
                 cv: int,
                 scoring: str,
                 logical_cores: int,
                 list_names_models: List[str] = Query(...),
                 pod_prepared_data: dict = Body(...)
                 ) -> dict:
    """Returns:
            dict: гиперпараметры лучшей ML модели.
            best_params_."""
    X_train, X_test = pd.DataFrame(pod_prepared_data['X_train']), pd.DataFrame(pod_prepared_data['X_test'])
    y_train, y_test = pd.DataFrame(pod_prepared_data['y_train']), pd.DataFrame(pod_prepared_data['y_test'])

    models = ModelGridCreator.prepare_framework_models(list_names_models, cv, scoring, X_train, y_train)
    grid_models = ModelGridCreator.manage_processes_create_model(logical_cores, models)
    best_grid_model = ModelGridCreator.search_best_model(grid_models, X_test, y_test, scoring)
    return {'best_grid_model': best_grid_model.best_params_}


class ModelGridCreator:
    """Класс содержит методы стандартрного пайплайна работы с ML моделью."""
    @staticmethod
    @logger_method(logger)
    def prepare_framework_models(list_names_models, cv, scoring, X_train, y_train) -> dict:
        """Returns:
                dict: объекты ML моделей, и список перебираемых гиперпараметров."""
        models_temp = ml_models.Models.models
        models = dict()
        for key in models_temp:
            if key in list_names_models:
                models[key] = models_temp[key]
                models[key]['cv'] = cv
                models[key]['scoring'] = scoring
                models[key]['X_train'] = X_train
                models[key]['y_train'] = y_train
        return models

    @staticmethod
    @logger_method(logger)
    def manage_processes_create_model(logical_cores, models) -> list:
        """Returns:
                list: обученные ML модели с выбранными гиперпараметрами."""
        with multiprocessing.Pool(logical_cores) as pool:
            grid_models = pool.map(ModelGridCreator.create_model, models.items())
        return grid_models

    @staticmethod
    @logger_method(logger)
    def create_model(data_model) -> GridSearchCV:
        """Returns:
                GridSearchCV: ML модель с установленными гиперпараметрами, определенными в ходе кросс-валидации."""
        grid_model = GridSearchCV(
            data_model[1]['model'],
            param_grid=data_model[1]['param_grid'],
            cv=data_model[1]['cv'],
            scoring=data_model[1]['scoring']
        )
        return grid_model.fit(data_model[1]['X_train'], data_model[1]['y_train'].squeeze())

    @staticmethod
    @logger_method(logger)
    def search_best_model(grid_models, X_test, y_test, scoring) -> GridSearchCV:
        """Returns:
                GridSearchCV: лучшая ML модель по метрике из config.yaml."""
        metric_value = float('inf')
        best_grid_model = None
        for grid_model in grid_models:
            y_pred = ModelGridCreator.predict_model(grid_model, X_test)
            metric_value_grid_model = ModelGridCreator.error_model(y_test, y_pred, scoring)
            if metric_value_grid_model < metric_value:
                metric_value = metric_value_grid_model
                best_grid_model = grid_model
        return best_grid_model

    @staticmethod
    @logger_method(logger)
    def predict_model(grid_model, X_test) -> pd.DataFrame:
        """Returns:
                DataFrame: Результат прогнозирования на тестовой выборке."""
        return grid_model.predict(X_test)

    @staticmethod
    @logger_method(logger)
    def error_model(y_test, y_pred, scoring) -> float:
        """Returns:
                float: Ошибка модели из config.yaml."""
        if scoring == 'neg_mean_absolute_error':
            metric_value = mean_absolute_error(y_test, y_pred)
        elif scoring == 'neg_mean_squared_error':
            metric_value = mean_squared_error(y_test, y_pred)
        else:
            metric_value = np.sqrt(mean_squared_error(y_test, y_pred))
        return metric_value
