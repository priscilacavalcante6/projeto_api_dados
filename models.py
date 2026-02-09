from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)

    password_hash = Column(String, nullable=False)

    is_admin = Column(Boolean, default=False)

    pokemons = relationship("Pokemon", back_populates="owner")


class Pokemon(Base):

    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True, nullable=False)

    type = Column(String, nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship("User", back_populates="pokemons")

# -------------------------------------------------------------------------------
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from .database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     password_hash = Column(String)

#     pokemons = relationship("Pokemon", back_populates="owner")


# class Pokemon(Base):
#     __tablename__ = "pokemon"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     type = Column(String)

#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="pokemons")


# -------------------------------------------------------------------
# from sqlalchemy import Column, Integer, String
# from .database import Base
# from sqlalchemy import Column, Integer, String
# from .database import Base


# class Pokemon(Base):
#     __tablename__ = "pokemon"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     type = Column(String)


# class User(Base):

#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     password_hash = Column(String)
