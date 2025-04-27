import sys
import os

from fastapi import FastAPI, File, UploadFile
from sklearn.model_selection import train_test_split
import pandas as pd

import abstract


app = FastAPI()
@app.post('/file_handler/{number_of_x_columns}/{number_of_y_columns}/{random_seed}/{test_size}/')
def upload_file(number_of_x_columns: int, number_of_y_columns: int, random_seed: int, test_size: float, file: UploadFile = File(...)):
    filename = file.filename
    prepare_data  = PrepareData(file, number_of_x_columns, number_of_y_columns, random_seed, test_size)
    temp = prepare_data.train_test_split_data()
    return {"filename": temp}


class PrepareData(abstract.Structure):
    def __init__(self, file, number_of_x_columns, number_of_y_columns, random_seed, test_size):
        self.df = pd.read_csv(file.file)
        self.X = self.df[self.df.columns[0:number_of_x_columns]]
        self.y = self.df[self.df.columns[number_of_x_columns:number_of_y_columns]]
        self.number_of_x_columns = number_of_x_columns
        self.number_of_y_columns = number_of_y_columns
        self.random_seed = random_seed
        self.test_size = test_size

    def preprocess_data(self):
        pass

    def polyniminal_model(self):
        pass

    def train_test_split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test \
            = train_test_split(self.X,
                               self.y,
                               test_size=self.test_size,
                               random_state=self.random_seed)
        return 11

    def standartization_data(self):
        pass

    def create_grid_model(self):
        pass

    def fit_model(self):
        pass

    def pred_model(self):
        pass

    def error_model(self):
        pass
