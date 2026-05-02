import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# 1. Carrega as variáveis do arquivo .env que está na raiz
load_dotenv()

def test_astra_connection():
    # 2. Recupera os valores das variáveis de ambiente
    # Certifique-se que os nomes coincidem com o que você escreveu no seu .env
    client_id = os.getenv('ASTRA_DB_CLIENT_ID')
    client_secret = os.getenv('ASTRA_DB_CLIENT_SECRET')
    bundle_path = os.getenv('SECURE_CONNECT_BUNDLE_PATH')
    keyspace = os.getenv('KEYSPACE') # Nome do keyspace que você confirmou estar ativo

    # 3. Configuração da conexão
    cloud_config = {
        'secure_connect_bundle': bundle_path
    }
    auth_provider = PlainTextAuthProvider(client_id, client_secret)
    
    try:
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()

        # 4. Validação direta no seu Keyspace
        session.set_keyspace(keyspace)
        print(f"✅ Conexão estabelecida com sucesso ao Keyspace: {keyspace}")
        
        # Teste de query simples
        row = session.execute("SELECT release_version FROM system.local").one()
        print(f"✅ Consulta de teste funcionou! Versão do servidor: {row[0]}")

    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
    finally:
        if 'cluster' in locals():
            cluster.shutdown()

if __name__ == "__main__":
    test_astra_connection()