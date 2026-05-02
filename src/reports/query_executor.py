import os
from pathlib import Path
from datetime import date
from src.common.astra_client import get_astra_session

BASE_DIR = Path(__file__).resolve().parent.parent.parent
QUERIES_DIR = BASE_DIR / "queries"

def load_query(filename):
    with open(QUERIES_DIR / filename, "r") as f:
        return f.read().strip()

def run():
    session, cluster = get_astra_session()
    
    print("\n--- RESULTADOS ACME LTDA ---")
    print("1: Histórico | 2: Infratores | 3: Real-time")
    opcao = input("Opção: ")

    try:
        if opcao == '1':
            id_cam = input("ID: ")
            data_hora_inicio = input("Data/Hora Início (YYYY-MM-DD HH:MM:SS): ")
            rows = session.execute(load_query("q1_historico_veiculo.cql.sql"), [id_cam, data_hora_inicio])
            print("DATA_HORA | VELOCIDADE | RPM | TEMPERATURA | GPS")
            for r in rows:
                print(f"{r.data_hora} | {r.velocidade} | {r.rpm} | {r.temperatura_motor} | {r.gps}")

        elif opcao == '2':
            dia = input("Data (YYYY-MM-DD): ")
            velocidade = input("Velocidade acima de (km/h): ")
            rows = session.execute(load_query("q2_monitoramento_velocidade.cql.sql"), [dia, int(velocidade)])
            print("ID_CAMINHAO | VELOCIDADE | DATA_HORA | GPS")
            for r in rows:
                print(f"{r.id_caminhao} | {r.velocidade} | {r.data_hora} | {r.gps}")

        elif opcao == '3':
            id_cam = input("ID: ")
            r = session.execute(load_query("q3_monitoramento_atual.cql.sql"), [id_cam]).one()
            if r:
                print("ID | DATA_HORA | GPS | COMBUSTÍVEL | VELOCIDADE | RPM | TEMPERATURA")
                print(f"{r.id_caminhao} | {r.data_hora} | {r.gps} | {r.nivel_combustivel} | {r.velocidade} | {r.rpm} | {r.temperatura_motor}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cluster.shutdown()

if __name__ == "__main__":
    run()