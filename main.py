from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from yaml_ import CRUDYaml
from parameters import Parameter


app = FastAPI()

@app.get("/")
def read_root():
    p = Parameter(**CRUDYaml.read('config.yaml'))
    return {'a': p.processes}
