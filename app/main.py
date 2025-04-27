from fastapi import FastAPI
import requests

from yaml_ import CRUDYaml
from parameters import Parameter
from decorators import logger_method
from variables import logger


app = FastAPI()

@app.get("/")
@logger_method(logger)
def read_root():
    params = Parameter(**CRUDYaml.read('config.yaml'))
    with open('data/data.csv', 'rb') as file:
        files = {'file': ('data.csv', file, 'text/csv')}
        model_data = requests.post(f"http://file_handler:8001/file_handler/"
                                 f"{params.number_of_x_columns}/"
                                 f"{params.number_of_y_columns}/"
                                 f"{params.random_seed}/"
                                 f"{params.test_size}/"
                                 f"{params.logical_cores}/"
                                 f"{params.lower_quantile}/"
                                 f"{params.upper_quantile}/",
                                 files=files)
    return {'a': model_data.json()}
