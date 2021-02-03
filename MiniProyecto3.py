import pymongo
import requests
import json

# conexion motor mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
print(client.list_database_names())
# creacion db
mydb = client['feriados2020']
# url api filtrada por anno
url = "https://apis.digital.gob.cl/fl/feriados/2020"
# extracion data con requests y user agent para que api no se bloquee
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
# carga de texto de api a formato json
responseJSON = json.loads(response.text)
# imprime formato texto y formato json
print(response.text)
print(responseJSON)
# creacion de coleccion feriados2020
coleccion = mydb['feriados2020']
# inserta lista de objetos json
coleccion.insert_many(responseJSON)

# queries solicitadas
print("\n===== Todos los Feriados de 2020 =====")
for x in coleccion.find():
    print("El día de " + x['nombre'] + " es un feriado de tipo " + x['tipo'] + " y se celebra el " + x['fecha'])

print("\n===== Solos los Feriados Civiles de 2020 =====")
for x in coleccion.find({'tipo': 'Civil'}):
    print("El día de " + x['nombre'] + " es un feriado de tipo " + x['tipo'] + " y se celebra el " + x['fecha'])

print("\n===== Solos los Feriados Irrenunciables de 2020 =====")
for x in coleccion.find({'irrenunciable': '1'}):
    print("El día de " + x['nombre'] + " es un feriado de tipo " + x['tipo'] + " y se celebra el " + x['fecha'])

print("\n===== Solos los Feriados que incluyen \"Santo\" o \"Santos\" =====")
for x in coleccion.find({'nombre': {'$regex':'\w*Santo\w*'}}):
    print("El día de " + x['nombre'] + " es un feriado de tipo " + x['tipo'] + " y se celebra el " + x['fecha'])

print("\n===== Leyes relacionadas con el Plebiscito de Abril =====")
x = coleccion.find_one({'nombre': 'Plebiscito Constitucional'})
print("Las leyes involucradas en el día del " + x['nombre'] + " son las siguientes:")
for i in x['leyes']:
    print(i['nombre'] + " Revisar en: " + i['url'])
