from src.common.astra_client import get_astra_session


session, cluster = get_astra_session()

def setup_cassandra():
    print(f"🛠️ Iniciando configuração das tabelas no Keyspace: {session.keyspace}...")

    tables = [
        # Tabela Q1: Histórico completo (Time Series)
        f"""
        CREATE TABLE IF NOT EXISTS {session.keyspace}.telemetria_por_caminhao (
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
        CREATE TABLE IF NOT EXISTS {session.keyspace}.alerta_por_excesso_velocidade (
            dia date,
            velocidade int,
            data_hora timestamp,
            id_caminhao text,
            gps text,
            PRIMARY KEY (dia, velocidade, data_hora)
        ) WITH CLUSTERING ORDER BY (velocidade DESC, data_hora DESC);
        """,

        # Tabela Q3: Status atual (Apenas o último registro de cada caminhão)
        # Sendo o id_caminhao a chave primária, cada nova inserção irá sobrescrever a anterior (upsert), mantendo apenas o registro mais recente.
        f"""
        CREATE TABLE IF NOT EXISTS {session.keyspace}.telemetria_atual (
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