from flask import Flask, request
from flask_restful import reqparse, abort, Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flaskmysql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

db = SQLAlchemy(app)