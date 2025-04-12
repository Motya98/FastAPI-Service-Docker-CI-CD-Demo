import os
from pathlib import Path

import statsmodels.api as sm
from pydantic import BaseModel, Field, field_validator

from variables import logger
from decorators import logger_method


class Parameter(BaseModel):
    parser: str = None
    logical_cores: int = Field(default=1)
    relative_data_path: str = None
    target_variables: list = None

    @field_validator('logical_cores')
    @logger_method(logger)
    def validate_logical_cores(cls, value) -> int:
        return value if 1 <= value <= os.cpu_count() else os.cpu_count()

    @field_validator('relative_data_path')
    @logger_method(logger)
    def validate_relative_data_path(cls, value) -> str:
        if not Path(value).exists():
            data = sm.datasets.get_rdataset("Boston", "MASS").data
            data.to_csv(Path(__file__).parent / 'data/data.csv')
            return str(Path(__file__).parent / 'data/data.csv')
        return value
