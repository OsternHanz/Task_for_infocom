import pydantic
import datetime
from typing import List

class Rulon_output(pydantic.BaseModel):
    id: int
    length: float = pydantic.Field(allow_none=False)
    weight: float = pydantic.Field(allow_none=False)
    date_of_insert: datetime.datetime
    date_of_delete: datetime.datetime = pydantic.Field(allow_none=True)

class List_of_rulons(pydantic.BaseModel):
    list_output: List[Rulon_output]
