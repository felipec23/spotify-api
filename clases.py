from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, request
from flask_restful import reqparse, abort, Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import requests
import config
from funciones import *
from settings import db

db_model = db.Model

class Album(db_model):
    __tablename__ = 'Albums'
    #se van a heredar unas propiedades que vienen de db
    #las siguientes líneas crean una tabla en sql con ese nombre y con estos parámetros (esquema):
    spotify_id = db.Column(db.String(100), primary_key=True)
    #id = db.Column(db.Integer)
    album_name = db.Column(db.String(100), nullable=False)
    list_id_artists = db.Column(db.String(1000000), nullable=False)
    total_tracks = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    
    #Cuando se instancie la clase:
    #Se definen los atributos del nuevo album que se añadirá:
    def __init__(self, spotify_id, album_name, list_id_artists, total_tracks, release_date):
        self.spotify_id = spotify_id
        self.album_name = album_name
        self.list_id_artists = list_id_artists
        self.total_tracks = total_tracks
        self.release_date = release_date        


class Track(db_model):
    __tablename__ = 'tracks'
    #se van a heredar unas propiedades que vienen de db
    #las siguientes líneas crean una tabla en sql con ese nombre y con estos parámetros (esquema):
    spotify_id = db.Column(db.String(100), primary_key=True)
    #id = db.Column(db.Integer)
    track_name = db.Column(db.String(100), nullable=False)
    track_number = db.Column(db.Integer, nullable=False)
    track_duration = db.Column(db.Integer, nullable=False)
    artists_id_list = db.Column(db.String(100000), nullable=False)
    spotify_album_id = db.Column(db.String(100), nullable=False)
    
    #Cuando se instancie la clase:
    #Se definen los atributos del nuevo album que se añadirá:
    def __init__(self, spotify_id, track_name, track_number, track_duration, artists_id_list, spotify_album_id):
        self.spotify_id = spotify_id
        self.track_name = track_name
        self.track_number = track_number
        self.track_duration = track_duration
        self.artists_id_list = artists_id_list
        self.spotify_album_id = spotify_album_id


class Artist(db_model):
    __tablename__ = 'artists'
    #se van a heredar unas propiedades que vienen de db
    #las siguientes líneas crean una tabla en sql con ese nombre y con estos parámetros (esquema):
    spotify_id = db.Column(db.String(100), primary_key=True)
    #id = db.Column(db.Integer)
    artist_name = db.Column(db.String(100), nullable=False)
    
    #Cuando se instancie la clase:
    #Se definen los atributos del nuevo album que se añadirá:
    def __init__(self, spotify_id, artist_name):
        self.spotify_id = spotify_id
        self.artist_name = artist_name


class Playlist(db_model):
    __tablename__ = 'Playlists'
    #se van a heredar unas propiedades que vienen de db
    #las siguientes líneas crean una tabla en sql con ese nombre y con estos parámetros (esquema):
    spotify_id = db.Column(db.String(100), primary_key=True)
    #id = db.Column(db.Integer)
    playlist_name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.String(100000), nullable=False)
    total_tracks = db.Column(db.Integer, nullable=False)

    
    #Cuando se instancie la clase:
    #Se definen los atributos del nuevo album que se añadirá:
    def __init__(self, spotify_id, playlist_name, owner_id, total_tracks):
        self.spotify_id = spotify_id
        self.playlist_name = playlist_name
        self.owner_id = owner_id
        self.total_tracks = total_tracks


class User(db_model):
    __tablename__ = 'Users'
    #se van a heredar unas propiedades que vienen de db
    #las siguientes líneas crean una tabla en sql con ese nombre y con estos parámetros (esquema):
    spotify_id = db.Column(db.String(100), primary_key=True)
    #id = db.Column(db.Integer)
    user_name = db.Column(db.String(100), nullable=False)

    #Cuando se instancie la clase:
    #Se definen los atributos del nuevo album que se añadirá:
    def __init__(self, spotify_id, user_name):
        self.spotify_id = spotify_id
        self.user_name = user_name


#Código para crear las tablas de todas las clases:
#Solo se tiene que correr una vez:
db.create_all()
