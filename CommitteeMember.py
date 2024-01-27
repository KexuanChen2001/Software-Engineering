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


class CommitteeMember(db.Model):
    __bind_key__ = 'committee'
    # chairman/dean, only for lucky draw
    username = db.Column('username', db.String(50), primary_key=True)
    # username should be primary since we could find the password from username
    password = db.Column('password', db.String(50))

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def genRandomPwd(length):
        numCount = random.randint(1, length - 1)
        lettercount = length - numCount
        numList = [random.choice(string.digits) for _ in range(numCount)]
        letterList = [random.choice(string.ascii_letters) for _ in range(lettercount)]
        allList = numList + letterList
        result = "".join([i for i in allList])
        return result
    
    def generateAllPwd(numOfJudges, numOfHeadJudge):
        # generate password
        # check whether already have the password generated
        if CommitteeMember.query.filter(CommitteeMember.username.startswith('Judge')).count() == 0 \
                and CommitteeMember.query.filter(CommitteeMember.username.startswith('HeadJudge')).count() == 0 \
                and CommitteeMember.query.filter(CommitteeMember.username.startswith('Dean')).count == 0:
            for i in range(1, numOfJudges + 1):
                m = CommitteeMember(1, 1)
                m.username = "Judge" + str(i)
                m.password = CommitteeMember.genRandomPwd(10)
                db.session.add(m)
                db.session.commit()
            for j in range(1, numOfHeadJudge + 1):
                m = CommitteeMember(1, 1)
                m.username = "HeadJudge" + str(j)
                m.password = CommitteeMember.genRandomPwd(10)
                db.session.add(m)
                db.session.commit()
            for k in range(1,2):
                m = CommitteeMember(1,1)
                m.username = "Dean"
                m.password = CommitteeMember.genRandomPwd(10)
                db.session.add(m)
                db.session.commit()
            flash('The password generated.')
        else:
            # refresh the database
            while CommitteeMember.query.filter(CommitteeMember.username.startswith('Judge')).count() != 0:
                c = CommitteeMember.query.filter(CommitteeMember.username.startswith('Judge')).first()
                db.session.delete(c)
                db.session.commit()
            while CommitteeMember.query.filter(CommitteeMember.username.startswith('HeadJudge')).count() != 0:
                c = CommitteeMember.query.filter(CommitteeMember.username.startswith('HeadJudge')).first()
                db.session.delete(c)
                db.session.commit()
            while CommitteeMember.query.filter(CommitteeMember.username.startswith("Dean")).count()!=0:
                c = CommitteeMember.query.filter(CommitteeMember.username.startswith("Dean")).first()
                db.session.delete(c)
                db.session.commit()
            # generate new one
            for i in range(1, numOfJudges + 1):
                m = CommitteeMember(1, 1)
                m.username = "Judge" + str(i)
                m.password = CommitteeMember.genRandomPwd(10)
                db.session.add(m)
                db.session.commit()
            for j in range(1, numOfHeadJudge + 1):
                m = CommitteeMember(1, 1)
                m.username = "HeadJudge" + str(j)
                m.password = CommitteeMember.genRandomPwd(10)
                db.session.add(m)
                db.session.commit()
            for k in range(1,2):
                m = CommitteeMember(1,1)
                m.username = "Dean"
                m.password = CommitteeMember.genRandomPwd(10)
                db.session.add(m)
                db.session.commit()
            flash('The password generated.')