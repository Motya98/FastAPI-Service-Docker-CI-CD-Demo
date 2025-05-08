import abstract

from fastapi import FastAPI, File, UploadFile
from sklearn.model_selection import train_test_split
import pandas as pd

from decorators import logger_method
from variables import logger

app = FastAPI()
@app.post('/file_handler/'
          '{number_of_x_columns}/'
          '{number_of_y_columns}/'
          '{random_seed}/'
          '{test_size}/'
          '{logical_cores}/'
          '{lower_quantile}/'
          '{upper_quantile}/')
@logger_method(logger)
def upload_file(number_of_x_columns: int,
                number_of_y_columns: int,
                random_seed: int,
                test_size: float,
                logical_cores: int,
                lower_quantile: float,
                upper_quantile: float,
                file: UploadFile = File(...)):
    filename = file.filename
    prepare_data = PrepareData(file, number_of_x_columns, number_of_y_columns, random_seed, test_size, logical_cores,lower_quantile, upper_quantile)
    prepare_data.preprocess_data()
    temp = prepare_data.train_test_split_data()
    # config_models = list()
    # with multiprocessing.Pool(logical_cores) as pool:
    #     res = pool.starmap(prepare_data.fit_model, config_models)
    return {"filename": temp, 'res3': 'res'}


class PrepareData(abstract.Structure):
    @logger_method(logger)
    def __init__(self, file,
                 number_of_x_columns,
                 number_of_y_columns,
                 random_seed,
                 test_size,
                 logical_cores,
                 lower_quantile,
                 upper_quantile):
        self.df = pd.read_csv(file.file)
        self.X = self.df[self.df.columns[0:number_of_x_columns]]
        self.y = self.df[self.df.columns[number_of_x_columns:number_of_y_columns]]
        self.number_of_x_columns = number_of_x_columns
        self.number_of_y_columns = number_of_y_columns
        self.random_seed = random_seed
        self.test_size = test_size
        self.logical_cores = logical_cores
        self.lower_quantile = lower_quantile
        self.upper_quantile = upper_quantile

    @logger_method(logger)
    def preprocess_data(self):
        q1 = self.df[self.df.columns[-1]].quantile(self.lower_quantile)
        q3 = self.df[self.df.columns[-1]].quantile(self.upper_quantile)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        self.df = self.df[(self.df[self.df.columns[-1]] > lower_bound) & (self.df[self.df.columns[-1]] < upper_bound)]

    @logger_method(logger)
    def polyniminal_model(self):
        pass

    @logger_method(logger)
    def train_test_split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test \
            = train_test_split(self.X,
                               self.y,
                               test_size=self.test_size,
                               random_state=self.random_seed)
        return len(self.df)

    def standartization_data(self):
        pass

    def create_grid_model(self):
        pass

    @staticmethod
    def fit_model():
        pass

    @staticmethod
    def pred_model():
        pass

    @staticmethod
    def error_model():
        pass
