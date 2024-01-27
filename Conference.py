from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# import os, cv2
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from werkzeug.datastructures import FileStorage
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poster.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite3"
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hanzi8888@126.com'
app.config['MAIL_PASSWORD'] = 'CUORWDHUWJIUABJK'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

class Conference(db.Model):
    conferenceID = db.Column('conferenceID', db.Integer, primary_key=True)
    date = db.Column('date', db.Date)
    time = db.Column('time', db.Time)
    venue = db.Column('venue', db.String(50))
    announcements = db.Column('announcements', db.String(50))
    # winner = db.Column('winner', db.String(50))
    content = db.Column('content', db.String(50))

    # numOfPoster = db.Column('numOfPoster', db.Integer)
    # remove some useless attributes in detailed design

    def __init__(self, date, time, venue, announcements, content):
        self.__date = date
        self.__time = time
        self.__venue = venue
        self.__announcements = announcements
        self.__content = content