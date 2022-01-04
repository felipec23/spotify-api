from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flaskmysql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



class Album(db.Model):
    #__tablename__ = 'albumes'
    #se van a heredar unas propiedades que vienen de db
    #las siguientes líneas crean una tabla en sql con ese nombre y con estos parámetros (esquema):
    id = db.Column(db.Integer)
    titulo = db.Column(db.String(100), unique=True)
    fecha_lanzamiento = db.Column(db.String(100))
    id_album = db.Column(db.String(100), primary_key=True)

    #Cuando se instancie la clase:
    #Se definen los atributos del nuevo album que se añadirá:
    def __init__(self, titulo, fecha_lanzamiento, id_album):
        self.titulo = titulo
        self.fecha_lanzamiento = fecha_lanzamiento
        self.id_album = id_album




#Código para crear las tablas de todas las clases:
db.create_all()

#Esquemas:
class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'titulo', 'fecha_lanzamiento', 'id_album')

album_schema = AlbumSchema()

@app.route('/crear_album', methods=["POST"])
def crear_album():
    request_json = request.json

    titulo = request_json["titulo"]
    fecha_lanzamiento = request_json["fecha_lanzamiento"]
    id_album = request_json["id_album"]

    #creo el objeto del album
    nuevo_album = Album(titulo, fecha_lanzamiento, id_album)

    #ejecutando el guardado
    db.session.add(nuevo_album)
    db.session.commit()


    print(request.json)
    return album_schema.jsonify(nuevo_album)



def faltan_argumentos(request_json, nombre_entidad):
    #Revisando si tiene todos los argumentos

    if nombre_entidad == "album":
        args_esperados = ["titulo", "fecha_lanzamiento", "id_album"]
        no_estan = [x for x in args_esperados if x not in request_json]
        print("no estan:")
        print(no_estan)
        return len(no_estan) > 0, ', '.join(no_estan)

"""
crear_album_args = reqparse.RequestParser()
crear_album_args.add_argument("titulo", type=str, help="Error: se requiere el título del álbum.", required=True)
crear_album_args.add_argument("fecha_lanzamiento", type=str, help="Error: se requiere la fecha de lanzamiento del álbum.", required=True)
crear_album_args.add_argument("id_spotify", type=str, help="Error: se requiere el id asignado por Spotify al álbum.")


@app.route('/crear/<string:nombre_entidad>', methods=["POST"])
def crear_en_entidad(nombre_entidad):
    print(nombre_entidad)
    if nombre_entidad == "album":

        args = crear_album_args.parse_args(request)
        respuesta = {"data": args}
        print(args)
        print(nombre_entidad, args)
        titulo = args["titulo"]
        fecha_lanzamiento = args["fecha_lanzamiento"]
        id_album = args["id_spotify"]

        #creo el objeto del album
        nuevo_elemento = Album(titulo, fecha_lanzamiento, id_album)

        #esquema a devolver
        esquema_devolver = album_schema.jsonify(nuevo_elemento)

    #ejecutando el guardado
    db.session.add(nuevo_elemento)
    db.session.commit()

    return respuesta, 201
"""
@app.route('/actualizar/<string:nombre_entidad>', methods=["PUT"])
def actualizar_en_entidad(nombre_entidad):
    request_json = request.json

    #revisando si es una entidad valida
    if nombre_entidad not in ["album", "playlist", "cancion", "artista"]:
        return {"data": f"No se encuentra '{nombre_entidad}' en la lista de entidades disponibles."}

    #revisando si cumple con todos los argumentos
    faltan = faltan_argumentos(request_json, nombre_entidad)
    print(faltan)
    if faltan[0]:
        #si no tiene los argumentos correctos:
        print("faltan argumentos")
        return {"data" : "No se enviaron los siguientes argumentos: {}".format(faltan[1])}

    #el nombre de la entidad como un argumento

    if nombre_entidad == "album":

        titulo_nuevo = request_json["titulo"]
        fecha_lanzamiento_nuevo = request_json["fecha_lanzamiento"]
        id_album_nuevo = request_json["id_album"]

        #encontrando el elemento que quiero actualizar:
        encontrado = Album.query.get(id_album_nuevo)

        #actualizando:
        encontrado.titulo = titulo_nuevo
        encontrado.fecha_lanzamiento = fecha_lanzamiento_nuevo

        #esquema a devolver
        esquema_devolver = album_schema.jsonify(encontrado)

        db.session.commit()
        return esquema_devolver


    pass





"""
delete_args = reqparse.RequestParser(bundle_errors=True)
delete_args.add_argument("id_spotify", type=str, help="No se detecta como parametro el Spotify-id del elemento que desea eliminar", required=True)


@app.route('/eliminar/<string:nombre_entidad>', methods=["DELETE"])
def eliminar_de_entidad(nombre_entidad):

    args = delete_args.parse_args()
    valor_eliminar = args["id_spotify"]

    if nombre_entidad == "album":

        encontrado = Album.query.get(valor_eliminar)
        #esquema_devolver = album_schema.jsonify(encontrado)

    abortar_si_no_existe(encontrado)
    db.session.delete(encontrado)
    db.session.commit()

    return args
    #trayendo objeto según entidad y según 
    #encontrado = Album.query.get()
    #
"""
#Para iniciar la app como tal:
if __name__ == "__main__":
    app.run(debug=True)