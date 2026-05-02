import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Carrega variáveis do .env
load_dotenv()

def setup_cassandra():
    # Configurações de conexão (ajuste os nomes das variáveis conforme seu .env)
    bundle_path = os.getenv('SECURE_CONNECT_BUNDLE_PATH')
    client_id = os.getenv('ASTRA_DB_CLIENT_ID')
    client_secret = os.getenv('ASTRA_DB_CLIENT_SECRET')
    keyspace = os.getenv('KEYSPACE')

    cloud_config = {'secure_connect_bundle': bundle_path}
    auth_provider = PlainTextAuthProvider(client_id, client_secret)
    
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    print(f"🛠️ Iniciando configuração das tabelas no Keyspace: {keyspace}...")

    tables = [
        # Tabela Q1: Histórico completo (Time Series)
        f"""
        CREATE TABLE IF NOT EXISTS {keyspace}.telemetria_por_caminhao (
            id_caminhao text,
            data_hora timestamp,
            gps text,
            velocidade int,
            rpm int,
            temperatura_motor float,
            nivel_combustivel float,
            PRIMARY KEY (id_caminhao, data_hora)
        ) WITH CLUSTERING ORDER BY (data_hora DESC);
        """,

        # Tabela Q2: Foco em performance para excesso de velocidade
        f"""
        CREATE TABLE IF NOT EXISTS {keyspace}.alerta_por_excesso_velocidade (
            dia date,
            velocidade int,
            data_hora timestamp,
            id_caminhao text,
            gps text,
            PRIMARY KEY (dia, velocidade, data_hora)
        ) WITH CLUSTERING ORDER BY (velocidade DESC, data_hora DESC);
        """,

        # Tabela Q3: Status atual (Apenas o último registro de cada caminhão)
        f"""
        CREATE TABLE IF NOT EXISTS {keyspace}.telemetria_atual (
            id_caminhao text PRIMARY KEY,
            data_hora timestamp,
            gps text,
            velocidade int,
            rpm int,
            temperatura_motor float,
            nivel_combustivel float
        );
        """
    ]

    for query in tables:
        try:
            session.execute(query)
            print(f"✅ Comando executado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao criar tabela: {e}")

    cluster.shutdown()
    print("🚀 Infraestrutura do Cassandra pronta!")

if __name__ == "__main__":
    setup_cassandra()