from pydantic import BaseModel 
from pydantic import Field , ConfigDict
from typing import Annotated 

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]

    model_config = ConfigDict(from_attributes=True)