from src.common.astra_client import get_astra_session


session, cluster = get_astra_session()
print(f"✅ Conectado com sucesso ao keyspace: {session.keyspace}")


def list_tables():
    session, cluster = get_astra_session()

    print(f"🔍 Verificando tabelas no keyspace: {session.keyspace}...")

    # Consulta ao catálogo do sistema para listar as tabelas do seu keyspace
    query = f"SELECT table_name FROM system_schema.tables WHERE keyspace_name='{session.keyspace}'"

    try:
        rows = session.execute(query)
        tables = [row.table_name for row in rows]
        
        if tables:
            print(f"✅ Tabelas encontradas:")
            for table in tables:
                print(f"  - {table}")
        else:
            print(f"⚠️ Nenhuma tabela encontrada no keyspace '{session.keyspace}'.")

    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")
    finally:
        cluster.shutdown()

if __name__ == "__main__":
    list_tables()