import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
from pathlib import Path

# Localiza o .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

def get_mongo_client():
    """
    Estabelece conexão com o MongoDB usando as credenciais do .env.
    Retorna o objeto 'client' (para fechar a conexão) e o objeto 'db' (para operações).
    """
    # Monta a URI usando as variáveis que definimos para o Docker
    # mongodb://admin:senha@mongodb:27017/
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DATABASE", "acme_fleet")

    try:
        # serverSelectionTimeoutMS impede que o script fique "pendurado" se o banco estiver fora
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # O comando 'ping' força a verificação real da conexão
        client.admin.command('ping')
        
        db = client[db_name]
        return client, db

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ Falha crítica: Não foi possível conectar ao MongoDB.")
        print(f"🔍 Verifique se o container 'mongodb_acme' está rodando.")
        print(f"⚠️ Erro detalhado: {e}")
        raise

def close_mongo_client(client):
    """Fecha a conexão com segurança."""
    if client:
        client.close()

if __name__ == "__main__":
    # Teste de fumaça (Smoke Test)
    print("--- Testando Conexão MongoDB (Ambiente Docker) ---")
    try:
        conn, database = get_mongo_client()
        print(f"✅ Sucesso! Conectado ao banco: {database.name}")
        close_mongo_client(conn)
    except Exception:
        print("🔴 Teste de conexão falhou.")