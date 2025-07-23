from pydantic import BaseModel
from datetime import datetime
from schemas.user import UserOut
from pydantic import ConfigDict

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)


class PostWithVotes(Post):
    votes: int

    model_config = ConfigDict(from_attributes=True)

class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    published: bool
    owner: UserOut
    votes: int

    model_config = ConfigDict(from_attributes=True)
