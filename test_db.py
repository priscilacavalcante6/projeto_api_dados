from api_dados.models import User
from api_dados.database import SessionLocal
import psycopg2

conn = psycopg2.connect(
    host="db.jnngozrvwigcwebokxbx.supabase.co",
    database="postgres",
    user="postgres",
    password="kFYt8n!VD#2j6@c",
    port=5432
)

print("CONECTADO COM SUCESSO 🚀")
conn.close()


db = SessionLocal()

user = User(
    username="teste_api",
    password_hash="123"
)

db.add(user)
db.commit()

print("OK")

db.close()
