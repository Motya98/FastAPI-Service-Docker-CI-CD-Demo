from fastapi import FastAPI, File, UploadFile
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import pandas as pd
import pydantic

from decorators import logger_method
from variables import logger

app = FastAPI()
@app.post(
          '/file_handler/'
          '{number_of_x_columns}/'
           )
@logger_method(logger)
def prepare_data(
                 number_of_x_columns: int,
                 ):

    pass