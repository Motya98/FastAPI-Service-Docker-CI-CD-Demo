from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import requests
import pandas as pd

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
        response = requests.post("http://file_handler:8001/file_handler", files=files)
    return {'a': response.text}
