import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

load_dotenv()

def list_tables():
    client_id = os.getenv('ASTRA_DB_CLIENT_ID')
    client_secret = os.getenv('ASTRA_DB_CLIENT_SECRET')
    bundle_path = os.getenv('SECURE_CONNECT_BUNDLE_PATH')
    keyspace = os.getenv('KEYSPACE')

    cluster = Cluster(
        cloud={'secure_connect_bundle': bundle_path},
        auth_provider=PlainTextAuthProvider(client_id, client_secret)
    )
    session = cluster.connect()

    print(f"🔍 Verificando tabelas no keyspace: {keyspace}...")

    # Consulta ao catálogo do sistema para listar as tabelas do seu keyspace
    query = f"SELECT table_name FROM system_schema.tables WHERE keyspace_name='{keyspace}'"
    
    try:
        rows = session.execute(query)
        tables = [row.table_name for row in rows]
        
        if tables:
            print(f"✅ Tabelas encontradas:")
            for table in tables:
                print(f"  - {table}")
        else:
            print(f"⚠️ Nenhuma tabela encontrada no keyspace '{keyspace}'.")

    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")
    finally:
        cluster.shutdown()

if __name__ == "__main__":
    list_tables()