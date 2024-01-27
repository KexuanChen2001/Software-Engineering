from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
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

class Rule(db.Model):
    __bind_key__ = 'info'
    numOfJudges = db.Column('numOfJudges', db.Integer, primary_key=True)
    numOfHeadJudge = db.Column('numOfHeadJudge', db.Integer)
    numOfFirstPrize = db.Column('numOfFirstPrize', db.Integer)
    numOfSecondPrize = db.Column('numOfSecondPrize', db.Integer)
    numOfThirdPrize = db.Column('numOfThirdPrize', db.Integer)
    numOfLuckyDraw = db.Column('numOfLuckyDraw', db.Integer)
    info = db.Column('info', db.String(100))

    def __init__(self, numOfJudges, numOfHeadJudge, numOfFirstPrize, numOfSecondPrize, numOfThirdPrize,
                 numOfLuckyDraw, info):
        self.__numOfJudges = numOfJudges
        self.__numOfHeadJudge = numOfHeadJudge
        self.__numOfFirstPrize = numOfFirstPrize
        self.__numOfSecondPrize = numOfSecondPrize
        self.__numOfThirdPrize = numOfThirdPrize
        self.__numOfLuckyDraw = numOfLuckyDraw
        self.__info = info
    
    def setUpRule(numOfJudges, numOfHeadJudge, numOfFirstPrize,numOfSecondPrize, numOfThirdPrize, numOfLuckyDraw, info):
        if Rule.query.count() == 0:
            ruleDemo = Rule(1, 1, 1, 1, 1, 1, 1)
            ruleDemo.numOfJudges = numOfJudges
            ruleDemo.numOfHeadJudge = numOfHeadJudge
            ruleDemo.numOfFirstPrize = numOfFirstPrize
            ruleDemo.numOfSecondPrize = numOfSecondPrize
            ruleDemo.numOfThirdPrize = numOfThirdPrize
            ruleDemo.numOfLuckyDraw = numOfLuckyDraw
            ruleDemo.info = info
            db.session.add(ruleDemo)
            db.session.commit()
        else:
            r = Rule.query.first()
            r.numOfJudges = numOfJudges
            r.numOfHeadJudge = numOfHeadJudge
            r.numOfFirstPrize = numOfFirstPrize
            r.numOfSecondPrize = numOfSecondPrize
            r.numOfThirdPrize = numOfThirdPrize
            r.numOfLuckyDraw = numOfLuckyDraw
            r.info = info
            db.session.commit()