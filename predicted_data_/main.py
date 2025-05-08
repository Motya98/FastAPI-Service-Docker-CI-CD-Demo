from typing import Any

from fastapi import FastAPI, File, UploadFile
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import pandas as pd
import pydantic

from decorators import logger_method
from variables import logger

app = FastAPI()


@app.post('/file_handler/')
@logger_method(logger)
def prepare_data(pod_prepared_data: dict[Any, Any]):
    return {'X_train': pod_prepared_data['X_train']}
