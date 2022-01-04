from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, request
from flask_restful import reqparse, abort, Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import requests
import config
from funciones import *
from clases import Album, Track, Artist, Playlist

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flaskmysql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

db = SQLAlchemy(app)
# an Engine, which the Session will use for connection
# resources
engine = create_engine("mysql+pymysql://root@localhost/flaskmysql")

CLIENT_ID = config.client_id
CLIENT_SECRET = config.client_secret

db_model = db.Model

#Código para crear las tablas de todas las clases:
#Solo se tiene que correr una vez:
db.create_all()


# json de canciones:
headers = get_headers(CLIENT_ID, CLIENT_SECRET)
playlist_id = "5N0FXofu4qF1wq5Ss5P0Dy"
json_canciones = canciones_de_playlist(playlist_id, headers)

#Extrayendo entidades del json
#albumes:
lista_diccionarios_albumes = traer_albumes(json_canciones)
lista_objetos_albumes = [Album(**dicti) for dicti in lista_diccionarios_albumes]

#canciones, tracks:
lista_diccionarios_tracks = traer_canciones(json_canciones)
lista_objetos_tracks = [Track(**dicti) for dicti in lista_diccionarios_tracks]

# artistas:
lista_diccionarios_artistas = traer_artistas(json_canciones)
lista_objetos_artistas = [Artist(**dicti) for dicti in lista_diccionarios_artistas]

#json con playlists de usuario:
user_id = "76sc36295vmrppbhrpmvuddmw"
json_playlists = playlists_de_usuario(headers, user_id)

# extrayendo las playlists como tal:
lista_diccionarios_playlists = traer_playlists(json_playlists)
lista_objetos_playlists = [Playlist(**dicti) for dicti in lista_diccionarios_playlists]

# create session and add objects
# trayendo datos de albumes:

with Session(engine) as session:
    #objects = [Album(titulo="titulooo", fecha_lanzamiento="2020-03-23", id_spotify="idUnicoS")]
    #Si voy a ingresarlos de forma bulk, en la fuente me debo asegurar de que no haya duplicados en el key
    
    #session.bulk_save_objects(lista_objetos_albumes)
    #session.bulk_save_objects(lista_objetos_tracks)
    #session.bulk_save_objects(lista_objetos_artistas)
    #session.bulk_save_objects(lista_objetos_playlists)
    session.commit()
    