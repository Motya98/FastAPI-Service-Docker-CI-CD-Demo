from typing import List, Any
import multiprocessing

from fastapi import FastAPI, Query, Body
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import pandas as pd
import pydantic

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
def prepare_data(
                 cv: int,
                 scoring: str,
                 logical_cores: int,
                 list_names_models: List[str] = Query(...),
                 pod_prepared_data: dict = Body(...)
                 ) -> dict:

    X_train, X_test = pod_prepared_data['X_train'], pod_prepared_data['X_test']
    y_train, y_test = pod_prepared_data['y_train'], pod_prepared_data['y_test']

    models = ml_models.Models.models
    models = {key: value for key, value in models.items() if key in list_names_models}
    for key in models:
        models[key]['scoring'] = 5

    with multiprocessing.Pool(logical_cores) as pool:
        res = pool.map(ModelGridCreator.create_model, list_names_models)

    return {'X_train': pod_prepared_data['X_train']}


class ModelGridCreator:
    @staticmethod
    def create_model(model_name):
        temp = ml_models.Models.models[model_name]

        return []
