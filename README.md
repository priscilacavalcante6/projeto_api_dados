# 📊 Projeto API de Dados

API desenvolvida em Python com o objetivo de gerenciar dados, autenticação de usuários e integração com banco de dados, seguindo uma estrutura modular e organizada.

---

## 🚀 Tecnologias Utilizadas

- Python
- FastAPI (ou Flask, ajuste se necessário)
- SQLAlchemy
- Pydantic
- SQLite / PostgreSQL (ajuste conforme o banco usado)
- Pytest

---

## 📁 Estrutura do Projeto

```bash
projeto_api_dados/
│
├── auth.py            # Autenticação e controle de acesso
├── create_admin.py    # Criação de usuário administrador
├── database.py        # Configuração do banco de dados
├── main.py            # Ponto de entrada da aplicação
├── models.py          # Modelos do banco de dados
├── schemas.py         # Schemas de validação
├── services.py        # Regras de negócio
├── test_db.py         # Testes de banco de dados
├── requirements.txt   # Dependências do projeto
└── README.md
