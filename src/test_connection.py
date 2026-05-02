from src.common.astra_client import get_astra_session

session, cluster = get_astra_session()
print(f"✅ Conectado com sucesso ao keyspace: {session.keyspace}")
cluster.shutdown()