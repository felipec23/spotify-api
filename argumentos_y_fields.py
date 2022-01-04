from flask_restful import reqparse, fields
#from settings import app
from flask_marshmallow import Marshmallow

crear_album_args = reqparse.RequestParser()
#crear_album_args.add_argument("spotify_id", type=str, help="Error: se requiere spotify id del album.", required=True)
crear_album_args.add_argument("album_name", type=str, help="Error: se requiere el nombre del album.", required=True)
crear_album_args.add_argument("list_id_artists", type=str, help="Error: se requiere la lista de ids de los artistas.", required=True)
crear_album_args.add_argument("total_tracks", type=int, help="Error: se requiere el numero total de tracks del album (int).", required=True)
crear_album_args.add_argument("release_date", type=str, help="Error: se requiere la fecha de lanzamiento del album.", required=True)

update_album_args = reqparse.RequestParser()
#update_album_args.add_argument("spotify_id", type=str, help="Error: se requiere spotify id del album.", required=False)
update_album_args.add_argument("album_name", type=str, help="Error: se requiere el nombre del album.", required=False)
update_album_args.add_argument("list_id_artists", type=str, help="Error: se requiere la lista de ids de los artistas.", required=False)
update_album_args.add_argument("total_tracks", type=int, help="Error: se requiere el numero total de tracks del album (int).", required=False)
update_album_args.add_argument("release_date", type=str, help="Error: se requiere la fecha de lanzamiento del album.", required=False)

#Devuelve la instancia de la base de datos en forma de json
resource_fields_album = {
    'spotify_id':fields.String,
    'album_name': fields.String,
    'list_id_artists': fields.String,
    'total_tracks': fields.Integer,
    'release_date': fields.DateTime
}


#spotify_id, track_name, track_number, track_duration, artists_id_list, spotify_album_id
crear_track_args = reqparse.RequestParser()
crear_track_args.add_argument("track_name", type=str, help="Error: se requiere el nombre del track.", required=True)
crear_track_args.add_argument("track_number", type=int, help="Error: se requiere el numero del track (int).", required=True)
crear_track_args.add_argument("track_duration", type=int, help="Error: se requiere la duracion del track (int).", required=True)
crear_track_args.add_argument("artists_id_list", type=str, help="Error: se requiere la lista de artistas del track.", required=True)
crear_track_args.add_argument("spotify_album_id", type=str, help="Error: se requiere el id del album al que pertenece el track.", required=True)

update_track_args = reqparse.RequestParser()
update_track_args.add_argument("track_name", type=str, help="Error: se requiere el nombre del track.", required=False)
update_track_args.add_argument("track_number", type=int, help="Error: se requiere el numero del track (int).", required=False)
update_track_args.add_argument("track_duration", type=int, help="Error: se requiere la duracion del track (int).", required=False)
update_track_args.add_argument("artists_id_list", type=str, help="Error: se requiere la lista de artistas del track.", required=False)
update_track_args.add_argument("spotify_album_id", type=str, help="Error: se requiere el id del album al que pertenece el track.", required=False)


# artistas:
#spotify_id, artist_name
crear_artist_args = reqparse.RequestParser()
crear_artist_args.add_argument("artist_name", type=str, help="Error: se requiere el nombre del artista.", required=True)

update_artist_args = reqparse.RequestParser()
update_artist_args.add_argument("artist_name", type=str, help="Error: se requiere el nombre del artista.", required=False)

# playlists:
#spotify_id, playlist_name, owner_id, total_tracks
crear_playlist_args = reqparse.RequestParser()
crear_playlist_args.add_argument("playlist_name", type=str, help="Error: se requiere el nombre de la playlist.", required=True)
crear_playlist_args.add_argument("owner_id", type=str, help="Error: se requiere el spotify id del dueño de la playlist.", required=True)
crear_playlist_args.add_argument("total_tracks", type=int, help="Error: se requiere el numero de tracks de la playlist.", required=True)

update_playlist_args = reqparse.RequestParser()
update_playlist_args.add_argument("playlist_name", type=str, help="Error: se requiere el nombre de la playlist.", required=False)
update_playlist_args.add_argument("owner_id", type=str, help="Error: se requiere el spotify id del dueño de la playlist.", required=False)
update_playlist_args.add_argument("total_tracks", type=int, help="Error: se requiere el numero de tracks de la playlist.", required=False)


# users:
#spotify_id, user_name
crear_user_args = reqparse.RequestParser()
crear_user_args.add_argument("user_name", type=str, help="Error: se requiere el nombre del usuario.", required=True)

update_user_args = reqparse.RequestParser()
update_user_args.add_argument("user_name", type=str, help="Error: se requiere el nombre del usuario.", required=False)