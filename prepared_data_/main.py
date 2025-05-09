import abstract
from typing import Any

from fastapi import FastAPI, File, UploadFile
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import pandas as pd

from decorators import logger_method
from variables import logger

app = FastAPI()

@app.post(
          '/file_handler/'
          '{number_of_x_columns}/'
          '{number_of_y_columns}/'
          '{random_seed}/'
          '{test_size}/'
          '{logical_cores}/'
          '{lower_quantile}/'
          '{upper_quantile}/'
          '{degree}/'
           )
@logger_method(logger)
def prepare_data(
                 number_of_x_columns: int,
                 number_of_y_columns: int,
                 random_seed: int,
                 test_size: float,
                 logical_cores: int,
                 lower_quantile: float,
                 upper_quantile: float,
                 degree: int,
                 file: UploadFile = File(...)
                 ) -> dict[str, list[dict[Any, Any]]]:
    """Returns:
            dict: Подготовленные тренировочная и тестовая выборки."""
    prepared_data = PreparedData(
                                 file,
                                 number_of_x_columns,
                                 number_of_y_columns,
                                 random_seed,
                                 test_size,
                                 logical_cores,
                                 lower_quantile,
                                 upper_quantile,
                                 degree
                                 )
    prepared_data.preprocess_data()
    prepared_data.train_test_split_data()
    if degree != 1:
        prepared_data.polynomial_model()
    prepared_data.standartization_data()
    return {
            "X_train": prepared_data.X_train.to_dict('records'),
            "X_test": prepared_data.X_test.to_dict('records'),
            "y_train": prepared_data.y_train.to_dict('records'),
            "y_test": prepared_data.y_test.to_dict('records'),
            }


class PreparedData(abstract.Structure):
    """Методы класса подготавливают данные (очистка -> разбиение -> полиномизация -> стандартизация)
       для дальнейших этапов обучения."""
    @logger_method(logger)
    def __init__(self,
                 file,
                 number_of_x_columns,
                 number_of_y_columns,
                 random_seed,
                 test_size,
                 logical_cores,
                 lower_quantile,
                 upper_quantile,
                 degree):

        self.df = pd.read_csv(file.file)
        self.X = self.df[self.df.columns[0:number_of_x_columns]]
        self.y = self.df[self.df.columns[number_of_x_columns:number_of_x_columns + number_of_y_columns]]
        self.number_of_x_columns = number_of_x_columns
        self.number_of_y_columns = number_of_y_columns
        self.random_seed = random_seed
        self.test_size = test_size
        self.logical_cores = logical_cores
        self.lower_quantile = lower_quantile
        self.upper_quantile = upper_quantile
        self.degree = degree

    @logger_method(logger)
    def preprocess_data(self):
        q1 = self.df[self.df.columns[-1]].quantile(self.lower_quantile)
        q3 = self.df[self.df.columns[-1]].quantile(self.upper_quantile)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        self.df = self.df[(self.df[self.df.columns[-1]] > lower_bound) & (self.df[self.df.columns[-1]] < upper_bound)]

    @logger_method(logger)
    def train_test_split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test \
            = train_test_split(self.X,
                               self.y,
                               test_size=self.test_size,
                               random_state=self.random_seed)
        return self.df[self.df.columns[self.number_of_x_columns:self.number_of_y_columns]]

    @logger_method(logger)
    def polynomial_model(self):
        poly = PolynomialFeatures(degree=self.degree, include_bias=False)
        self.X_train =  poly.fit_transform(self.X_train)
        self.X_test = poly.transform(self.X_test)

    @logger_method(logger)
    def standartization_data(self):
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

        self.X_train = pd.DataFrame(self.X_train)
        self.X_test = pd.DataFrame(self.X_test)
