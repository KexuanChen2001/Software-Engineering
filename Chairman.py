from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# import os, cv2
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from werkzeug.datastructures import FileStorage
import string
import random

from CommitteeMember import CommitteeMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poster.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite3"
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hanzi8888@126.com'
app.config['MAIL_PASSWORD'] = 'CUORWDHUWJIUABJK'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)


class Chairman(CommitteeMember):
    def __init__(self, chairmanID, password):
        self.__chairmanID = chairmanID
        self.__password = password
