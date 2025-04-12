from abstract import Structure
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import mean_absolute_error, mean_squared_error
import random
import joblib
import pickle
import uuid
import seaborn as sns

class FrameWork(Structure):
    def __init__(self, data_path, number_of_x, number_of_y_column, model, percent_train, random_seed, param_grid, cv, scoring, poly_bool, alias_model):
        self.number_of_x = number_of_x
        self.number_of_y_column = number_of_y_column
        self.df = pd.read_csv(data_path)

        up, low = np.percentile(self.df[self.df.columns[-1]], [75, 25])
        temp = (up - low)
        low_limit = low - 1.5 * temp
        up_limit = up + 1.5 * temp
        self.df = self.df[self.df[self.df.columns[-1]] > low_limit]
        self.df = self.df[self.df[self.df.columns[-1]] < up_limit]

        self.x = self.df[self.df.columns[0:number_of_x]]
        self.y = self.df[self.df.columns[number_of_x + number_of_y_column]]
        self.model = model
        self.percent_train = percent_train
        self.random_seed = random_seed
        self.param_grid = param_grid
        self.cv = cv
        self.scoring = scoring
        self.poly_bool = poly_bool
        self.alias_model = alias_model

    def polyniminal_model(self):
        if self.poly_bool != 1:
            polynominal_converter = PolynomialFeatures(degree=self.poly_bool)
            polynominal_converter.fit(self.x)
            self.x = polynominal_converter.transform(self.x)

    def train_test_split_model(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=(1 - self.percent_train / 100), random_state=self.random_seed)


    def standartization_data(self):
        scaler = Normalizer()
        scaler.fit(self.x_train)
        self.x_train = scaler.transform(self.x_train)
        self.x_test = scaler.transform(self.x_test)

        self.x_train = pd.DataFrame(self.x_train)
        self.x_test = pd.DataFrame(self.x_test)


    def create_grid_model(self):
        self.grid_model = GridSearchCV(self.model, param_grid=self.param_grid, cv=self.cv, scoring=self.scoring)


    def fit_model(self):
        self.grid_model.fit(self.x_train, self.y_train)
        self.best_param = self.grid_model.best_params_
        # print(len(self.x_train.columns), self.poly_bool)


    def pred_model(self):
        self.y_pred = self.grid_model.predict(self.x_test)


    def error_model(self):
        self.mae = mean_absolute_error(self.y_test, self.y_pred)
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        self.rmse = np.sqrt(mean_squared_error(self.y_test, self.y_pred))
        #print(f'{self.alias_model}({self.grid_model.best_params_})(degree:{self.poly_bool}): mae = {round(self.mae, 3)}, mse = {round(self.mse, 3)}, rmse = {round(self.rmse, 3)},'
        #      f' {self.df.columns[self.number_of_x + self.number_of_y_column]}')

    def save_test(self):
        self.y_pred = pd.DataFrame(self.y_pred)
        self.y_test.reset_index(drop=True, inplace=True)
        self.y_pred.reset_index(drop=True, inplace=True)
        self.y_concat = pd.concat([self.y_test, self.y_pred], axis=1)
        #self.y_concat.columns = ['mass_test', 'mass_pred']

        uu_id = uuid.uuid1().hex
        #self.y_concat.to_csv(f'data\\{self.alias_model}Degree{self.poly_bool}.csv')
        self.name_y = self.df.columns[self.number_of_x + self.number_of_y_column]
        name_model = f'{self.alias_model}{self.grid_model.best_params_}_Degree:{self.poly_bool}_{self.name_y}.pkl'
        symbols = ['(', ')', ':', ',', "'", ' ']
        for i in symbols:
            name_model = name_model.replace(i, '')
        with open(f"models\\{name_model}", 'wb') as f:
            pickle.dump(self.grid_model, f)

        #return [name_model, round(self.mae, 5), round(self.mse, 5), round(self.rmse, 5), self.df.columns[self.number_of_x + self.number_of_y_column], uu_id]
        return {name_model: {'mae': round(self.mae, 5), 'mse': round(self.mse, 5), 'rmse': round(self.rmse, 5), 'name_y': self.name_y,
                             'degree': self.poly_bool}}




