import time
import random

from datetime import datetime
from dotenv import load_dotenv
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from src.common.astra_client import get_astra_session


session, cluster = get_astra_session()

def simulate_fleet(num_trucks=15):
    
    # Lista fixa de caminhões para simular a frota da ACME LTDA
    truck_ids = [f"BR-{random.randint(1000, 9999)}" for _ in range(num_trucks)]
    
    print(f"🚛 Simulação iniciada para {num_trucks} veículos. Pressione Ctrl+C para parar.")

    try:
        while True:
            for truck_id in truck_ids:
                # Gerando dados fictícios de sensores
                agora = datetime.now()
                velocidade = random.randint(40, 130) # Simula variação de velocidade
                gps = f"{random.uniform(-25.4, -25.5):.4f}, {random.uniform(-49.2, -49.3):.4f}" # Região de Curitiba/Litoral PR
                
                # Dados básicos de telemetria
                telemetria = {
                    'id': truck_id,
                    'ts': agora,
                    'v': velocidade,
                    'gps': gps,
                    'rpm': random.randint(1500, 3500),
                    'temp': float(random.randint(85, 105)),
                    'comb': float(random.uniform(5, 100))
                }

                # --- 1. Histórico Completo (Q1) ---
                query_hists = f"INSERT INTO {session.keyspace}.telemetria_por_caminhao (id_caminhao, data_hora, gps, velocidade, rpm, temperatura_motor, nivel_combustivel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                
                # --- 2. Status Atual (Q3 - Upsert) ---
                query_atual = f"INSERT INTO {session.keyspace}.telemetria_atual (id_caminhao, data_hora, gps, velocidade, rpm, temperatura_motor, nivel_combustivel) VALUES (%s, %s, %s, %s, %s, %s, %s)"

                # Execução das principais
                session.execute(query_hists, (telemetria['id'], telemetria['ts'], telemetria['gps'], telemetria['v'], telemetria['rpm'], telemetria['temp'], telemetria['comb']))
                session.execute(query_atual, (telemetria['id'], telemetria['ts'], telemetria['gps'], telemetria['v'], telemetria['rpm'], telemetria['temp'], telemetria['comb']))

                # --- 3. Lógica de Alerta de Velocidade (Nova Q2) ---
                # Só insere se exceder o benchmark de 80km/h
                if velocidade > 80:
                    query_alerta = f"INSERT INTO {session.keyspace}.alerta_por_excesso_velocidade (dia, velocidade, data_hora, id_caminhao, gps) VALUES (%s, %s, %s, %s, %s)"
                    dia_atual = agora.date()
                    session.execute(query_alerta, (dia_atual, telemetria['v'], telemetria['ts'], telemetria['id'], telemetria['gps']))
                    print(f"⚠️  ALERTA: {truck_id} a {velocidade} km/h!")
                else:
                    print(f"✅ {truck_id}: {velocidade} km/h (Normal)")

            time.sleep(10) # Intervalo de 10s conforme o projeto original[cite: 1]

    except KeyboardInterrupt:
        print("\n🛑 Simulação encerrada.")
    finally:
        cluster.shutdown()

if __name__ == "__main__":
    simulate_fleet()