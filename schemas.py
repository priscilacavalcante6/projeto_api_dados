from pydantic import BaseModel
from typing import Optional


# =========================
# USERS
# =========================

class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


# =========================
# POKEMON
# =========================

class PokemonCreate(BaseModel):
    name: str
    type: str


class PokemonOut(BaseModel):
    id: int
    name: str
    type: str
    owner_id: Optional[int]

    class Config:
        from_attributes = True


# ------------------------------------------------------------------------
# from pydantic import BaseModel


# class UserCreate(BaseModel):
#     username: str
#     password: str


# class UserOut(BaseModel):
#     id: int
#     username: str
#     is_admin: bool

#     class Config:
#         orm_mode = True


# ---------------------------------------------------------------------
# from pydantic import BaseModel


# class UserCreate(BaseModel):
#     username: str
#     password: str


# class PokemonCreate(BaseModel):
#     name: str
#     type: str


# class PokemonResponse(BaseModel):
#     id: int
#     name: str
#     type: str

#     class Config:
#         orm_mode = True
