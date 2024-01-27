from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# import os, cv2
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from werkzeug.datastructures import FileStorage
import string
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendee.sqlite3"
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

class Attendee(db.Model):
    __bind_key__ = 'attendee'
    # the use case of UICer/Attendee
    # the function in its html: vote poster; register
    # search poster (look poster: so that all members could do it: show the home.html);
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(50), primary_key=True)
    voteStatus = db.Column('voteStatus', db.Integer)

    # status as boolean
    def __init__(self, id, email, voteStatus):
        self.__id = id
        self.__email = email
        self.__voteStatus = voteStatus
        # if 1, has the pior to vote

    def giveVotes(self, n):
        user = Attendee(1, 1, 1)
        user.email = self.email
        user.id = self.id
        Attendee.query.filter_by(email = self.email).delete()
        db.session.commit()
        user.voteStatus = n
        db.session.add(user)
        db.session.commit()
