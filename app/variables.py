from logger_ import create_logger
from yaml_ import CRUDYaml


logger = create_logger()


def get_params():
    from parameters import Parameter

    return Parameter(**CRUDYaml.read('config.yaml'))
