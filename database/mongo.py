from os import environ

import pymongo

uri = environ.get('MONGO_MASTER_URI')


def client():
    assert uri, 'Undefined Mongo Atlas Uri'
    return pymongo.MongoClient(uri).base_dados


def send_cia_aberta_cad(data):
    db = client()
    cia_aberta_cad = db['cia_aberta_cad']
    cia_aberta_cad.drop()
    cia_aberta_cad.insert_many(data)


def send_cia_aberta_doc(data):
    db = client()
    cia_aberta_doc = db['cia_aberta_doc']
    cia_aberta_doc.insert_many(data)
