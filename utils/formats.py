from typing_extensions import TypedDict
from typing import List
from pydantic import BaseModel, Field,model_serializer
from pydantic import TypeAdapter
from typing import List

class GraphState(TypedDict):
    query : str
    action : List[str]
    observation : List[str]
    generate: str


class keyword(BaseModel):
    keyword:str

class Output_format(BaseModel):
    keywords: List[keyword]

class UserInput(BaseModel):
    user_input: str