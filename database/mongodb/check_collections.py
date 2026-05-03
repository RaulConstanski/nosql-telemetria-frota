from src.common.mongo_db_client import get_mongo_client

def check_mongo_collections():
    client, db = get_mongo_client()
    
    print("🔍 Verificando Coleções no MongoDB (acme_fleet):")
    print("-" * 45)
    
    try:
        collections = db.list_collection_names()
        
        if not collections:
            print("⚠️ Nenhuma coleção encontrada no banco de dados.")
        else:
            for col_name in collections:
                count = db[col_name].count_documents({})
                print(f"📦 Coleção: {col_name:15} | Documentos: {count}")
                
                # Opcional: Listar índices da coleção
                indexes = db[col_name].index_information()
                idx_names = ", ".join(indexes.keys())
                print(f"   ∟ Índices: {idx_names}")

    except Exception as e:
        print(f"❌ Erro ao verificar coleções: {e}")
    finally:
        print("-" * 45)
        client.close()

if __name__ == "__main__":
    check_mongo_collections()