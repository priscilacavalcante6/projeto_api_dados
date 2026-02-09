from fastapi import Depends, HTTPException, status
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .database import Base, engine, SessionLocal
from .models import Pokemon, User
from .schemas import PokemonCreate, UserCreate
from .services import get_local_pokemon, import_pokemon_api
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================
# DATABASE
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# AUTH
# =========================

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    exists = db.query(User).filter(
        User.username == user.username
    ).first()

    if exists:
        raise HTTPException(400, "Usuário já existe")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        is_admin=False
    )

    db.add(new_user)
    db.commit()

    return {"message": "Usuário criado com sucesso"}


@app.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form.username
    ).first()

    if not user:
        raise HTTPException(401, "Login inválido")

    if not verify_password(
        form.password,
        user.password_hash
    ):
        raise HTTPException(401, "Login inválido")

    token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = decode_token(token)

    if not payload:
        raise HTTPException(401, "Token inválido")

    username = payload.get("sub")

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(401, "Usuário inválido")

    return user


def get_current_admin(
    user: User = Depends(get_current_user)
):

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Acesso restrito a administradores"
        )

    return user


# =========================
# ROTAS
# =========================

@app.get("/")
def home():
    return {"status": "API Pokemon rodando 🚀"}


@app.get("/pokemon")
def list_pokemons(db: Session = Depends(get_db)):
    return db.query(Pokemon).all()


@app.get("/pokemon/{name}")
def get_pokemon(name: str, db: Session = Depends(get_db)):

    pokemon = get_local_pokemon(name, db)

    if not pokemon:
        raise HTTPException(404, "Pokemon não encontrado")

    return pokemon


@app.get("/me/pokemons")
def my_pokemons(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(Pokemon).filter(
        Pokemon.owner_id == user.id
    ).all()

# =========================
# DELETE POKEMON (ADMIN)
# =========================


@app.delete("/pokemon/{name}")
def delete_pokemon(
    name: str,
    admin: User = Depends(get_current_admin),  # só admins podem deletar
    db: Session = Depends(get_db)
):
    # Busca o Pokémon pelo nome
    pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()

    if not pokemon:
        raise HTTPException(404, "Pokemon não encontrado")

    # Deleta do banco
    db.delete(pokemon)
    db.commit()

    return {"detail": f"Pokemon '{name}' deletado com sucesso!"}

# =========================
# CREATE POKEMON (USER)
# =========================


@app.post("/pokemon")
def create_pokemon(
    pokemon: PokemonCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing = db.query(Pokemon).filter(
        Pokemon.name == pokemon.name
    ).first()

    if existing:
        raise HTTPException(400, "Pokemon já existe")

    novo = Pokemon(
        name=pokemon.name,
        type=pokemon.type,
        owner_id=user.id
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# =========================
# IMPORT (ADMIN)
#

# -----------------------------------------------------------------------------
# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session

# from .database import Base, engine, SessionLocal
# from .models import Pokemon
# from .services import fetch_pokemon
# from .schemas import PokemonCreate


# Base.metadata.create_all(bind=engine)

# app = FastAPI()


# # Dependency (conexão automática)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Home
# @app.get("/")
# def home():
#     return {"status": "API Pokemon rodando 🚀"}


# # Listar todos
# @app.get("/pokemon")
# def list_pokemons(db: Session = Depends(get_db)):
#     return db.query(Pokemon).all()


# # Buscar por nome
# @app.get("/pokemon/{name}")
# def get_pokemon(name: str, db: Session = Depends(get_db)):

#     pokemon = fetch_pokemon(name, db)

#     if not pokemon:
#         raise HTTPException(status_code=404, detail="Pokemon não encontrado")

#     return pokemon

# @app.post("/pokemon/import/{name}")
# def import_pokemon(name: str, db: Session = Depends(get_db)):

#     pokemon = fetch_pokemon(name, db)

#     if not pokemon:
#         raise HTTPException(404, "Não foi possível importar")

#     return pokemon


# # Criar
# @app.post("/pokemon")
# def create_pokemon(
#     pokemon: PokemonCreate,
#     db: Session = Depends(get_db)
# ):

#     novo = Pokemon(
#         name=pokemon.name,
#         type=pokemon.type
#     )

#     db.add(novo)
#     db.commit()
#     db.refresh(novo)

#     return novo


# # Atualizar
# @app.put("/pokemon/{name}")
# def update_pokemon(
#     name: str,
#     pokemon: PokemonCreate,
#     db: Session = Depends(get_db)
# ):

#     db_pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()

#     if not db_pokemon:
#         raise HTTPException(status_code=404, detail="Pokemon não encontrado")

#     db_pokemon.name = pokemon.name
#     db_pokemon.type = pokemon.type

#     db.commit()
#     db.refresh(db_pokemon)

#     return db_pokemon


# Deletar
# @app.delete("/pokemon/{name}")
# def delete_pokemon(name: str, db: Session = Depends(get_db)):

#     pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()

#     if not pokemon:
#         raise HTTPException(status_code=404, detail="Pokemon não encontrado")

#     db.delete(pokemon)
#     db.commit()

#     return {"message": "Pokemon removido"}


# @app.delete("/pokemon/{name}")
# def delete_pokemon(name: str, current_user: User = Depends(get_current_admin)):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=403, detail="Não autorizado")

#     pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()
#     if not pokemon:
#         raise HTTPException(status_code=404, detail="Pokémon não encontrado")

#     db.delete(pokemon)
#     db.commit()
#     return {"detail": f"{name} deletado com sucesso!"}

# -------------------------------------------------------------------------
# from fastapi import FastAPI, HTTPException
# from .database import Base, engine, SessionLocal
# from .models import Pokemon
# from .services import fetch_pokemon

# Base.metadata.create_all(bind=engine)

# app = FastAPI()


# @app.get("/")
# def home():
#     return {"status": "API Pokemon rodando 🚀"}


# @app.get("/pokemon")
# def list_pokemons():
#     db = SessionLocal()
#     pokemons = db.query(Pokemon).all()
#     db.close()
#     return pokemons


# @app.get("/pokemon/{name}")
# def get_pokemon(name: str):
#     try:
#         pokemon = fetch_pokemon(name)
#         return {
#             "id": pokemon.id,
#             "name": pokemon.name,
#             "type": pokemon.type
#         }
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))

# ----------------------------------------------------------------------
# from fastapi import FastAPI, HTTPException
# from .services import fetch_pokemon
# from .database import SessionLocal
# from .models import Pokemon

# app = FastAPI()


# @app.get("/")
# def home():
#     return {"status": "API Pokemon rodando 🚀"}


# @app.get("/pokemon")
# def list_pokemons():
#     db = SessionLocal()
#     pokemons = db.query(Pokemon).all()
#     db.close()
#     return pokemons


# @app.get("/pokemon/{name}")
# def get_pokemon(name: str):
#     try:
#         pokemon = fetch_pokemon(name)
#         return {
#             "id": pokemon.id,
#             "name": pokemon.name,
#             "type": pokemon.type
#         }
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))
