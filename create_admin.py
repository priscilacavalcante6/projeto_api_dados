# create_admin.py

from api_dados.models import User  # seu modelo de usuário
from api_dados.database import SessionLocal  # sua sessão do banco
from passlib.context import CryptContext

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Criando a sessão do banco
db = SessionLocal()

# Crie o usuário admin
admin_user = User(
    username="admin",
    # troque para a senha que quiser
    password_hash=pwd_context.hash("senha_super_secreta"),
    is_admin=True
)

# Adiciona no banco
db.add(admin_user)
db.commit()
db.close()

print("Admin criado com sucesso!")
