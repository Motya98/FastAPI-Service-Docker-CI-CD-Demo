from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from yaml_ import CRUDYaml
from parameters import Parameter
from decorators import logger_method, create_logger


app = FastAPI()
logger = create_logger()

@app.get("/")
@logger_method(logger)
def read_root():
    p = Parameter(**CRUDYaml.read('config.yaml'))
    return {'a': p.relative_data_path}
