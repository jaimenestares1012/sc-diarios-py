from pymongo import MongoClient
import os


client = MongoClient('mongodb://localhost:27017')
# client = MongoClient("mongodb+srv://user_jaime:XhA7pqTDWKfQy6Nh@micluster.pns9q58.mongodb.net")

db  = client.get_database("pruebadiarios")

def insertarMongo(valor, coleccion):
    col = db[coleccion]
    id =col.insert_one(valor)
    return id

def buscarMongo(valor, parametro , coleccion):
    col = db[coleccion]
    id =col.find_one({parametro: valor})
    return id

def deletearMongo(valor, parametro, coleccion):
    col = db[coleccion]
    id =col.delete_one({parametro: valor})
    return id