import os
from pathlib import Path

import statsmodels.api as sm
from pydantic import BaseModel, Field, field_validator


class Parameter(BaseModel):
    parser: str = None
    logical_cores: int = Field(default=1)
    relative_data_path: str = None

    @field_validator('logical_cores')
    def validate_logical_cores(cls, value) -> int:
        return value if 1 <= value <= os.cpu_count() else os.cpu_count()

    @field_validator('relative_data_path')
    def validate_relative_data_path(cls, value) -> str:
        if not Path(value).exists():
            data = sm.datasets.get_rdataset("Boston", "MASS").data
            data.to_csv('data/data.csv')
            return 'data/data.csv'
        return value
