import json
from pathlib import Path
from src.common.mongo_db_client import get_mongo_client # Ajustado para o nome do seu arquivo

def ingest_motoristas_raw():
    client, db = get_mongo_client()
    col = db["motoristas"]
    
    # Busca pasta raw de motoristas.
    raw_path = Path("/app/data/raw/example_motoristas")
    
    if not raw_path.exists():
        print(f"⚠️ Pasta {raw_path} não encontrada.")
        return

    json_files = list(raw_path.glob("*.json"))
    
    if not json_files:
        print(f"📁 Nenhum arquivo JSON encontrado em: {raw_path}")
        return

    print(f"🚀 Processando {len(json_files)} arquivo(s) de motoristas...")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Esta parte garante que 1 arquivo de x motoristas funcione!
                records = data if isinstance(data, list) else [data]
                
                for record in records:
                    if "cpf" in record:
                        col.update_one(
                            {"cpf": record["cpf"]},
                            {"$set": record},
                            upsert=True
                        )
                
            print(f"  ✅ {file_path.name} ingerido com sucesso.")
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {file_path.name}: {e}")

    client.close()
    print("🏁 Ingestão de motoristas concluída.")

if __name__ == "__main__":
    ingest_motoristas_raw()