import requests



def get_headers(client_id, client_secret):
    

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    #En json:
    auth_response_data = auth_response.json()

    #Access token:
    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    return headers



def canciones_de_playlist(playlist_id, headers):
    #playlist_id = "5N0FXofu4qF1wq5Ss5P0Dy"
    BASE_URL = 'https://api.spotify.com/v1/'
    r2 = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', 
                    headers=headers, 
                    params={'include_groups': 'artist', 'limit': 50})
    json_canciones = r2.json()
    return json_canciones

def traer_canciones(json_canciones):

    #Extrae las canciones del json respuesta
    canciones = []
    already = []
    for track_fake in json_canciones["items"]:
        track = track_fake["track"]
        album_id = track["album"]["id"]
        id_lista_artistas = [x["id"] for x in track["artists"]]
        string_lista_artistas = "_".join(id_lista_artistas)
        track_duration = track["duration_ms"]
        track_id = track["id"]
        track_name = track["name"]
        track_number = track["track_number"]

        dicti = {"spotify_id": track_id, "track_name": track_name, "track_number": track_number,
                "track_duration": track_duration, "artists_id_list": string_lista_artistas,
                "spotify_album_id": album_id}
        
        #fila = [track_id, track_name, track_number, track_duration,
        #        string_lista_artistas,
        #        album_id]
        if track_id not in already:

            canciones.append(dicti)
            already.append(track_id)

    return canciones

def traer_albumes(json_canciones):

    #Extrae los albumes del json respuesta
    albumes = []
    already = []
    for track_fake in json_canciones["items"]:
        track = track_fake["track"]
        album_id = track["album"]["id"]
        album_name = track["album"]["name"]
        id_lista_artistas = [x["id"] for x in track["album"]["artists"]]
        string_lista_artistas = '_'.join(id_lista_artistas)
        total_tracks = track["album"]["total_tracks"]
        release_date = track["album"]["release_date"]

        dicti = {"spotify_id": album_id, "album_name": album_name, "list_id_artists":string_lista_artistas,
            "total_tracks": total_tracks, "release_date": release_date} 
        #fila = [album_id, album_name, id_lista_artistas, total_tracks,
        #        release_date]

        #Evitando duplicados:
        if album_id not in already:

            albumes.append(dicti)
            already.append(album_id)

    return albumes
    

def traer_artistas(json_canciones):

    #Extrae los artistas del json respuesta
    artistas = []
    already = []
    for track_fake in json_canciones["items"]:
        track = track_fake["track"]

        id_lista_artistas = [x["id"] for x in track["artists"]]
        nombre_lista_artistas = [x["name"] for x in track["artists"]]

        for i in range(len(id_lista_artistas)):
            
            if id_lista_artistas[i] not in already:
                #fila = [id_lista_artistas[i], nombre_lista_artistas[i]]
                dicti = {"spotify_id": id_lista_artistas[i], "artist_name": nombre_lista_artistas[i]}
                artistas.append(dicti)
                already.append(id_lista_artistas[i])

    return artistas


def playlists_de_usuario(headers, user_id):
    #De un usuario me traigo las playlists:
    #user_id = "76sc36295vmrppbhrpmvuddmw"
    BASE_URL = 'https://api.spotify.com/v1/'
    r3 = requests.get(BASE_URL + 'users/' + user_id + '/playlists', 
                    headers=headers, 
                    params={'include_groups': 'track', 'limit': 50})

    json_playlists = r3.json()

    return json_playlists

def traer_playlists(json_playlists):
    playlists = []
    already = []
    for playlist in json_playlists['items']:
        id_playlist = playlist["id"]
        playlist_name = playlist["name"]
        owner_id = playlist["owner"]["id"]
        total_tracks = playlist["tracks"]["total"]

        if id_playlist not in already:

            dicti = {"spotify_id": id_playlist, "playlist_name": playlist_name,
                    "owner_id": owner_id, "total_tracks": total_tracks}
            #playlists.append([id_playlist, playlist_name, owner_id, total_tracks])
            playlists.append(dicti)
            already.append(id_playlist)

    return playlists
