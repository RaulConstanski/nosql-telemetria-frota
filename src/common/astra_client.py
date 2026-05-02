import os
from pathlib import Path
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Localiza a raiz do projeto para garantir que o .env seja lido de qualquer subpasta
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

def get_astra_session():
    """
    Retorna (session, cluster) já configurados com o Keyspace do seu .env.
    """
    client_id = os.getenv('ASTRA_DB_CLIENT_ID')
    client_secret = os.getenv('ASTRA_DB_CLIENT_SECRET')
    bundle_path = os.getenv('SECURE_CONNECT_BUNDLE_PATH')
    # Utiliza sua variável já existente
    keyspace = os.getenv('ASTRA_DB_KEYSPACE')

    cloud_config = {'secure_connect_bundle': bundle_path}
    auth_provider = PlainTextAuthProvider(client_id, client_secret)
    
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    
    # Define o contexto do Keyspace globalmente para a sessão
    if keyspace:
        session.set_keyspace(keyspace)
    
    return session, cluster