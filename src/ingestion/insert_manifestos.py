import json
from pathlib import Path
from src.common.mongo_db_client import get_mongo_client # Ajustado para o nome do seu arquivo

def ingest_manifestos_raw():
    client, db = get_mongo_client()
    col = db["manifestos"]

    # Ajustado para a pasta que você mencionou (certifique-se que ela existe no Linux)
    raw_path = Path("/app/data/raw/example_manifestos")
    
    if not raw_path.exists():
        print(f"⚠️ Pasta {raw_path} não encontrada.")
        return

    json_files = list(raw_path.glob("*.json"))
    
    if not json_files:
        print(f"📁 Nenhum arquivo JSON encontrado em: {raw_path}")
        return

    print(f"🚀 Processando {len(json_files)} arquivo(s) de manifestos...")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Esta parte garante que 1 arquivo de x manifestos funcione!
                records = data if isinstance(data, list) else [data]
                
                for record in records:
                    if "id_manifesto" in record:
                        col.update_one(
                            {"id_manifesto": record["id_manifesto"]},
                            {"$set": record},
                            upsert=True
                        )
                
            print(f"  ✅ {file_path.name} ingerido com sucesso.")
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {file_path.name}: {e}")

    client.close()
    print("🏁 Ingestão de manifestos concluída.")

if __name__ == "__main__":
    ingest_manifestos_raw()