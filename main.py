from flask import Flask, request, Response
from flask_restful import reqparse, abort, Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from clases import Album, Track, Artist, Playlist, User
from settings import db, api, app
from flask_marshmallow import Marshmallow
from argumentos_y_fields import *


db_model = db.Model

#Para manejar elementos no encontrados:
def abortar_si_no_existe(elemento_encontrado):
    if elemento_encontrado == None:
        abort("No se encuentra un elemento con el id especificado.")

#Para manejar elementos  encontrados:
def abortar_si_existe(elemento_encontrado):
    if elemento_encontrado != None:
        abort("El elemento con el id especificado ya existe. Para actualizar un elemento por favor use el método PUT o PATCH.")

from datetime import datetime
def check_date(string_date):
    print(string_date)
    try:
        datetime.strptime(string_date, "%Y-%m-%d")
    except Exception as e:
        print(e)
        abort("Formato de fecha incorrecto. Por favor revisar.")

class AlbumResource(Resource):
    print("\n")
    #Cuando devuelva el resultado, devuelvalo en forma de json
    @marshal_with(resource_fields_album)
    def get(self, spotify_id):
        encontrado = Album.query.filter_by(spotify_id=spotify_id).first()
        print(encontrado)
        abortar_si_no_existe(encontrado)
        #return Response(encontrado, status=201, mimetype='application/json')
        print(encontrado)
        return encontrado

    @marshal_with(resource_fields_album)
    def delete(self, spotify_id):

        encontrado = Album.query.get(spotify_id)

        abortar_si_no_existe(encontrado)
        db.session.delete(encontrado)
        db.session.commit()

        return encontrado
        
    @marshal_with(resource_fields_album)
    def post(self, spotify_id):
        args = crear_album_args.parse_args()
        args["spotify_id"] = spotify_id

        check_date(args["release_date"])
        #titulo = args["titulo"]
        #fecha_lanzamiento = args["fecha_lanzamiento"]
        #spotify_id = args["spotify_id"]
        
        #Si ya existe, debería abortar
        encontrado = Album.query.get(spotify_id)
        abortar_si_existe(encontrado)

        #Creo el objeto del album
        #nuevo_elemento = Album(titulo, fecha_lanzamiento, spotify_id)
        nuevo_elemento = Album(**args)

        #Ejecutando el guardado
        db.session.add(nuevo_elemento)
        db.session.commit()

        return nuevo_elemento

    @marshal_with(resource_fields_album)
    def put(self, spotify_id):
        #Con put exige todos los argumentos
        args = crear_album_args.parse_args()
        #titulo_nuevo = args["titulo"]
        #fecha_lanzamiento_nuevo = args["fecha_lanzamiento"]
        #id_album_nuevo = args["id_spotify"]

        #encontrando el elemento que quiero actualizar:
        encontrado = Album.query.get(spotify_id)

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)

        #actualizando:
        #encontrado.titulo = titulo_nuevo
        #encontrado.fecha_lanzamiento = fecha_lanzamiento_nuevo
        for key, value in args.items():
            print(key, value)
            setattr(encontrado, key, value)     

        #esquema a devolver
        #esquema_devolver = album_schema.jsonify(encontrado)

        db.session.commit()

        return encontrado

    @marshal_with(resource_fields_album)
    def patch(self, spotify_id):
        #Patch permite actualizar así no estén todos los argumentos
        args = update_album_args.parse_args()
        encontrado = Album.query.filter_by(spotify_id=spotify_id).first()

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)  

        #Actualizando entidad, si esta es no nula
        for key, value in args.items():
            print(key, value)
            if args[key]:
                setattr(encontrado, key, value)


        db.session.commit()
        return encontrado

# tracks:
ma = Marshmallow(app)
#Esquemas:
class TrackSchema(ma.Schema):
    class Meta:
        fields = ('spotify_id', 'track_name', 'track_number', 'track_duration', 'artists_id_list', 'spotify_album_id')

track_schema = TrackSchema()

class TrackResource(Resource):
    print("\n")
    #Cambiar args de parse, en create y update
    #Cambiar el nombre de la clase, para que busque en la tabla que es
    #Cambiar el esquema
    esquema = track_schema
    args_obligatorios = crear_track_args
    args_opcionales = update_track_args

    def get(self, spotify_id, esquema=esquema):
        encontrado = Track.query.filter_by(spotify_id=spotify_id).first()
        print(encontrado)
        abortar_si_no_existe(encontrado)

        esquema_devolver = esquema.jsonify(encontrado)
        print(esquema_devolver)
        return esquema_devolver

    def delete(self, spotify_id, esquema=esquema):

        encontrado = Track.query.get(spotify_id)

        abortar_si_no_existe(encontrado)
        db.session.delete(encontrado)
        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver
        
    def post(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        args = args_obligatorios.parse_args()
        args["spotify_id"] = spotify_id

        #Si ya existe, debería abortar
        encontrado = Track.query.get(spotify_id)
        abortar_si_existe(encontrado)

        #Creo el objeto de la entidad
        nuevo_elemento = Track(**args)

        #Ejecutando el guardado
        db.session.add(nuevo_elemento)
        db.session.commit()

        esquema_devolver = esquema.jsonify(nuevo_elemento)

        return esquema_devolver

    def put(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        #Con put exige todos los argumentos
        args = args_obligatorios.parse_args()

        #encontrando el elemento que quiero actualizar:
        encontrado = Track.query.get(spotify_id)

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)

        #actualizando:
        for key, value in args.items():
            print(key, value)
            setattr(encontrado, key, value)     

        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver

    def patch(self, spotify_id, esquema=esquema, args_opcionales=args_opcionales):
        #Patch permite actualizar así no estén todos los argumentos
        args = args_opcionales.parse_args()
        encontrado = Track.query.filter_by(spotify_id=spotify_id).first()

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)  

        #Actualizando entidad, si esta es no nula
        for key, value in args.items():
            print(key, value)
            if args[key]:
                setattr(encontrado, key, value)


        db.session.commit()
        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver


# Artists:
#Esquemas:
class ArtistSchema(ma.Schema):
    class Meta:
        fields = ('spotify_id', 'artist_name')

artist_schema = ArtistSchema()

class ArtistResource(Resource):
    print("\n")
    #Cambiar nombre de clase y cambiar y añadir ruta de recurso
    #Cambiar args de parse, en create y update
    #Cambiar el nombre de la clase, para que busque en la tabla que es
    #Cambiar el esquema
    esquema = artist_schema
    args_obligatorios = crear_artist_args
    args_opcionales = update_artist_args

    def get(self, spotify_id, esquema=esquema):
        encontrado = Artist.query.filter_by(spotify_id=spotify_id).first()
        print(encontrado)
        abortar_si_no_existe(encontrado)

        esquema_devolver = esquema.jsonify(encontrado)
        print(esquema_devolver)
        return esquema_devolver

    def delete(self, spotify_id, esquema=esquema):

        encontrado = Artist.query.get(spotify_id)

        abortar_si_no_existe(encontrado)
        db.session.delete(encontrado)
        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver
        
    def post(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        args = args_obligatorios.parse_args()
        args["spotify_id"] = spotify_id

        #Si ya existe, debería abortar
        encontrado = Artist.query.get(spotify_id)
        abortar_si_existe(encontrado)

        #Creo el objeto de la entidad
        nuevo_elemento = Artist(**args)

        #Ejecutando el guardado
        db.session.add(nuevo_elemento)
        db.session.commit()

        esquema_devolver = esquema.jsonify(nuevo_elemento)

        return esquema_devolver

    def put(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        #Con put exige todos los argumentos
        args = args_obligatorios.parse_args()

        #encontrando el elemento que quiero actualizar:
        encontrado = Artist.query.get(spotify_id)

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)

        #actualizando:
        for key, value in args.items():
            print(key, value)
            setattr(encontrado, key, value)     

        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver

    def patch(self, spotify_id, esquema=esquema, args_opcionales=args_opcionales):
        #Patch permite actualizar así no estén todos los argumentos
        args = args_opcionales.parse_args()
        encontrado = Artist.query.filter_by(spotify_id=spotify_id).first()

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)  

        #Actualizando entidad, si esta es no nula
        for key, value in args.items():
            print(key, value)
            if args[key]:
                setattr(encontrado, key, value)


        db.session.commit()
        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver

########################################################################

# Artists:
#Esquemas:
class PlaylistSchema(ma.Schema):
    class Meta:
        fields = ('spotify_id', 'playlist_name', 'owner_id', 'total_tracks')

playlist_schema = PlaylistSchema()

class PlaylistResource(Resource):
    print("\n")
    #Cambiar nombre de clase y cambiar y añadir ruta de recurso
    #Cambiar args de parse, en create y update
    #Cambiar el nombre de la clase, para que busque en la tabla que es
    #Cambiar el esquema
    esquema = playlist_schema
    args_obligatorios = crear_playlist_args
    args_opcionales = update_playlist_args

    def get(self, spotify_id, esquema=esquema):
        encontrado = Playlist.query.filter_by(spotify_id=spotify_id).first()
        print(encontrado)
        abortar_si_no_existe(encontrado)

        esquema_devolver = esquema.jsonify(encontrado)
        print(esquema_devolver)
        return esquema_devolver

    def delete(self, spotify_id, esquema=esquema):

        encontrado = Playlist.query.get(spotify_id)

        abortar_si_no_existe(encontrado)
        db.session.delete(encontrado)
        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver
        
    def post(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        args = args_obligatorios.parse_args()
        args["spotify_id"] = spotify_id

        #Si ya existe, debería abortar
        encontrado = Playlist.query.get(spotify_id)
        abortar_si_existe(encontrado)

        #Creo el objeto de la entidad
        nuevo_elemento = Playlist(**args)

        #Ejecutando el guardado
        db.session.add(nuevo_elemento)
        db.session.commit()

        esquema_devolver = esquema.jsonify(nuevo_elemento)

        return esquema_devolver

    def put(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        #Con put exige todos los argumentos
        args = args_obligatorios.parse_args()

        #encontrando el elemento que quiero actualizar:
        encontrado = Playlist.query.get(spotify_id)

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)

        #actualizando:
        for key, value in args.items():
            print(key, value)
            setattr(encontrado, key, value)     

        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver

    def patch(self, spotify_id, esquema=esquema, args_opcionales=args_opcionales):
        #Patch permite actualizar así no estén todos los argumentos
        args = args_opcionales.parse_args()
        encontrado = Playlist.query.filter_by(spotify_id=spotify_id).first()

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)  

        #Actualizando entidad, si esta es no nula
        for key, value in args.items():
            print(key, value)
            if args[key]:
                setattr(encontrado, key, value)


        db.session.commit()
        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver


########################################################################

# Userse:
#Esquemas:
class UserSchema(ma.Schema):
    class Meta:
        fields = ('spotify_id', 'user_name')

user_schema = UserSchema()

class UserResource(Resource):
    print("\n")
    #Cambiar nombre de clase y cambiar y añadir ruta de recurso
    #Cambiar args de parse, en create y update
    #Cambiar el nombre de la clase, para que busque en la tabla que es
    #Cambiar el esquema
    esquema = user_schema
    args_obligatorios = crear_user_args
    args_opcionales = update_user_args

    def get(self, spotify_id, esquema=esquema):
        encontrado = User.query.filter_by(spotify_id=spotify_id).first()
        print(encontrado)
        abortar_si_no_existe(encontrado)

        esquema_devolver = esquema.jsonify(encontrado)
        print(esquema_devolver)
        return esquema_devolver

    def delete(self, spotify_id, esquema=esquema):

        encontrado = User.query.get(spotify_id)

        abortar_si_no_existe(encontrado)
        db.session.delete(encontrado)
        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver
        
    def post(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        args = args_obligatorios.parse_args()
        args["spotify_id"] = spotify_id

        #Si ya existe, debería abortar
        encontrado = User.query.get(spotify_id)
        abortar_si_existe(encontrado)

        #Creo el objeto de la entidad
        nuevo_elemento = User(**args)

        #Ejecutando el guardado
        db.session.add(nuevo_elemento)
        db.session.commit()

        esquema_devolver = esquema.jsonify(nuevo_elemento)

        return esquema_devolver

    def put(self, spotify_id, esquema=esquema, args_obligatorios=args_obligatorios):
        #Con put exige todos los argumentos
        args = args_obligatorios.parse_args()

        #encontrando el elemento que quiero actualizar:
        encontrado = User.query.get(spotify_id)

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)

        #actualizando:
        for key, value in args.items():
            print(key, value)
            setattr(encontrado, key, value)     

        db.session.commit()

        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver

    def patch(self, spotify_id, esquema=esquema, args_opcionales=args_opcionales):
        #Patch permite actualizar así no estén todos los argumentos
        args = args_opcionales.parse_args()
        encontrado = User.query.filter_by(spotify_id=spotify_id).first()

        #Si no existe, abortar, porque no hay qué actualizar:
        abortar_si_no_existe(encontrado)  

        #Actualizando entidad, si esta es no nula
        for key, value in args.items():
            print(key, value)
            if args[key]:
                setattr(encontrado, key, value)


        db.session.commit()
        esquema_devolver = esquema.jsonify(encontrado)

        return esquema_devolver

@app.route('/ping', methods=["POST", "GET"])
def health():
    db.engine.execute("select 1")
    return {"data": "todo ok"}


#Añadiendo recursos:

api.add_resource(AlbumResource, "/albumes/<string:spotify_id>")
api.add_resource(TrackResource, "/tracks/<string:spotify_id>")
api.add_resource(ArtistResource, "/artists/<string:spotify_id>")
api.add_resource(PlaylistResource, "/playlists/<string:spotify_id>")
api.add_resource(UserResource, "/users/<string:spotify_id>")


if __name__ == "__main__":
    app.run(debug=True)