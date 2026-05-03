from src.common.mongo_db_client import get_mongo_client

def setup_mongodb():
    client, db = get_mongo_client()
    
    try:
        print("🚀 Iniciando Setup do MongoDB...")

        # 1. Criar/Validar Coleção de Motoristas e seu Índice
        if "motoristas" not in db.list_collection_names():
            db.create_collection("motoristas")
            print("✅ Coleção 'motoristas' criada.")
        
        db.motoristas.create_index("cpf", unique=True)
        print("📌 Índice único em 'cpf' garantido.")

        # 2. Criar/Validar Coleção de Manifestos e seu Índice
        if "manifestos" not in db.list_collection_names():
            db.create_collection("manifestos")
            print("✅ Coleção 'manifestos' criada.")
            
        db.manifestos.create_index("id_manifesto", unique=True)
        print("📌 Índice único em 'id_manifesto' garantido.")

        print("\n✨ Setup finalizado com sucesso!")

    except Exception as e:
        print(f"❌ Erro durante o setup: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    setup_mongodb()