from flask import Flask, request, flash, url_for, redirect, render_template, send_file, Response
from flask_sqlalchemy import SQLAlchemy
# import os, cv2
import io
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import xlrd
import flask_excel as excel


app = Flask(__name__)
excel.init_excel(app)

# Some database
SQLALCHEMY_BINDS = {
    'Poster': 'sqlite:///poster.sqlite3',
    'info': 'sqlite:///info.sqlite3',
    'stu': 'sqlite:///stu.sqlite3',
    'committee': 'sqlite:///committee.sqlite3',
    'attendee': 'sqlite:///attendee.sqlite3'
}

# Default database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poster.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hanzi8888@126.com'
app.config['MAIL_PASSWORD'] = 'CUORWDHUWJIUABJK'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

numJ = 0

class Poster(db.Model):
    __bind_key__ = 'Poster'
    posterID = db.Column('poster_id', db.Integer, primary_key = True)
    author = db.Column(db.String(50))
    email = db.Column(db.String(50))
    programmeName = db.Column(db.String(50))
    abstract = db.Column(db.String(100))
    Score_s = db.Column(db.Integer)
    Score_j = db.Column(db.Integer)
    Score_h = db.Column(db.Integer)

    def __init__(self, posterID, author, email, programmeName, abstract):
        self.posterID = posterID
        self.author = author
        self.email = email
        self.programmeName = programmeName
        self.abstract = abstract
        self.Score_s = 0
        self.Score_j = 0
        self.Score_h = 0

    def addAllPoster(fi, upload_path):
        fi.save(upload_path)
        clinic_file = xlrd.open_workbook(upload_path)
        table = clinic_file.sheet_by_index(0)
        nrows = table.nrows
        for i in range(1, nrows):
            new = Poster(1, 1, 1, 1, 1)
            row_date = table.row_values(i)
            new.posterID = str(row_date[0])
            new.programmeName = str(row_date[1])
            new.author = str(row_date[2])
            new.email = str(row_date[3])
            new.abstract = str(row_date[4])
            db.session.add(new)
            db.session.commit()
            db.session.close()

    def addPosterInfo(poster):
        db.session.add(poster)
        db.session.commit()
        flash('Record was successfully added')

    def delPosterInfo(poster):
        db.session.delete(poster[0])
        db.session.commit()
        flash('Record was successfully deleted')

    def editPosterInfo(result):
        db.session.delete(result[0])
        db.session.commit()
        poster = Poster(request.form['posterID'],
                        request.form['author'],
                        request.form['email'],
                        request.form['programmeName'],
                        request.form['abstract'])
        db.session.add(poster)
        db.session.commit()
        flash("Edit successfully!")

    def giveScore(id, score):
        s = Poster.query.filter(Poster.posterID == id).first()
        s1 = s.Score_j
        global numJ
        numJ = numJ + 1
        if s.Score_j == 0:
            Poster.query.filter(Poster.posterID == id).update({'Score_j': score})
            db.session.commit()
        else:
            Poster.query.filter(Poster.posterID == id).update(
                {'Score_j': s1 * ((numJ - 1) / numJ) + float(score) * 1 / numJ})
            db.session.commit()

    def giveScoreh(id, score):
        Poster.query.filter(Poster.posterID == id).update({'Score_h': score})
        db.session.commit()
        flash("Score successfully!")

    def giveVote(id):
        s = Poster.query.filter(Poster.posterID == id).first()
        s.Score_s = s.Score_s + 1
        db.session.commit()
        flash("Vote successfully!")
