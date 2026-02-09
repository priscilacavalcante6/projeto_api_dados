import requests
from .models import Pokemon


def get_local_pokemon(name: str, db):

    return db.query(Pokemon).filter(Pokemon.name == name).first()


def import_pokemon_api(name: str, db):

    # Primeiro: tenta no banco
    existing = get_local_pokemon(name, db)

    if existing:
        return existing

    # Busca na API externa
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Pokemon não encontrado na API externa")

    data = response.json()

    pokemon = Pokemon(
        name=data["name"],
        type=data["types"][0]["type"]["name"]
    )

    db.add(pokemon)
    db.commit()
    db.refresh(pokemon)

    return pokemon


# --------------------------------------------------------------
# import requests
# from .models import Pokemon


# def fetch_pokemon(name: str, db):

#     # 1️⃣ Primeiro: tenta buscar no banco
#     existing = db.query(Pokemon).filter(Pokemon.name == name).first()

#     if existing:
#         return existing

#     # 2️⃣ Se não existir → busca na API externa
#     url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         raise Exception("Pokemon não encontrado na API externa")

#     data = response.json()

#     # 3️⃣ Cria no banco
#     pokemon = Pokemon(
#         name=data["name"],
#         type=data["types"][0]["type"]["name"]
#     )

#     db.add(pokemon)
#     db.commit()
#     db.refresh(pokemon)

#     # 4️⃣ Retorna
#     return pokemon

# --------------------------------------------------------------------------
# import requests
# from .models import Pokemon
# from .database import SessionLocal


# # def fetch_pokemon(name):
# #     db = SessionLocal()
# def fetch_pokemon(name, db):
#     return db.query(Pokemon).filter(Pokemon.name == name).first()

#     existing = db.query(Pokemon).filter(Pokemon.name == name).first()
#     if existing:
#         db.close()
#         return existing

#     url = f"https://pokeapi.co/api/v2/pokemon/{name}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         db.close()
#         raise Exception("Pokemon não encontrado na API externa")

#     data = response.json()

#     pokemon = Pokemon(
#         name=data["name"],
#         type=data["types"][0]["type"]["name"]
#     )

#     db.add(pokemon)
#     db.commit()
#     db.refresh(pokemon)
#     db.close()

#     return pokemon


# import requests
# from .models import Pokemon
# from .database import SessionLocal

# def fetch_pokemon(name):
#     url = f"https://pokeapi.co/api/v2/pokemon/{name}"
#     response = requests.get(url)
#     data = response.json()

#     pokemon = Pokemon(
#         name=data["name"],
#         type=data["types"][0]["type"]["name"]
#     )

#     db = SessionLocal()
#     db.add(pokemon)
#     db.commit()
#     db.close()

#     return pokemon

# def fetch_pokemon(name):
#         url = f"https://pokeapi.co/api/v2/pokemon/{name}"
#         data = requests.get(url).json()

#         pokemon = Pokemon(
#             name=data["name"],
#             type=data["types"][0]["type"]["name"]
#         )

#         db = SessionLocal()
#         db.add(pokemon)
#         db.commit()
#         db.close()

#         return pokemon
