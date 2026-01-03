from pymongo import MongoClient
from datetime import datetime, timezone

#Conexão direta com o MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client['crypto_db']
collection = db['prices']

#Documentos para inserção
documento = {
    "bitcoin": 0,
    "ethereum": 0,
    "created_at": datetime.now(timezone.utc),
    "status": "inicial"
}

collection.insert_one(documento)

print("Banco criado com sucesso!", db.name)
print("Coleção criada com sucesso!", collection.name)
print("Documento inserido com sucesso!")