from pydantic import BaseModel, Field, field_validator


class Parameter(BaseModel):
    parser: str = None
    processes: int = Field(default=1)

    @field_validator('processes')
    def validate_processes(cls, value):
        return value if 1 <= value <= 4 else 1
