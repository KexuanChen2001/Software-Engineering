from flask import Flask, request, flash, url_for, redirect, render_template, send_file, Response
from flask_sqlalchemy import SQLAlchemy
# import os, cv2
import io
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import xlrd
# import flask_excel as excel

# Import py file
from CommitteeMember import *
from Conference import *
from Attendee import *
from Rule import *
from Poster import *
from DivisionWinnerPoster import *
from PopularPoster import *
from Poster_InternalUse import *
from Poster_PublicUse import *
from ProgrammeWinnerPoster import *
from Judge import *
from HeadJudge import *
from Chairman import *

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

app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hanzi8888@126.com'
app.config['MAIL_PASSWORD'] = 'CUORWDHUWJIUABJK'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

att = None


def uploadjpg():
    f = request.files['file']
    basepath = os.path.dirname(__file__)
    name = request.form.get('posterID')
    upload_path = os.path.join(basepath, 'static/images',
                               secure_filename(f.filename))
    f.save(upload_path)
    img = cv2.imread(upload_path)
    filename = name + '.jpg'
    cv2.imwrite(os.path.join(basepath, 'static/images', filename), img)

def sendEmail(email):
    msg = Message('LuckyDraw', sender='hanzi8888@126.com', recipients=[email])
    msg.body = "YEEEEEEEEEE! You are the lucky guy!"
    mail.send(msg)
    flash("Send Email Successfully")

def getWinnerList():
    dswinner = Poster.query.filter(Poster.email == 'DS').order_by(Poster.Score_j.desc()).first()
    cstwinner = Poster.query.filter(Poster.email == 'CST').order_by(Poster.Score_j.desc()).first()
    apsywinner = Poster.query.filter(Poster.email == 'APSY').order_by(Poster.Score_j.desc()).first()
    fstwinner = Poster.query.filter(Poster.email == 'FST').order_by(Poster.Score_j.desc()).first()
    statwinner = Poster.query.filter(Poster.email == 'STAT').order_by(Poster.Score_j.desc()).first()
    envswinner = Poster.query.filter(Poster.email == 'ENVS').order_by(Poster.Score_j.desc()).first()
    fmwinner = Poster.query.filter(Poster.email == 'FST').order_by(Poster.Score_j.desc()).first()
    list = [dswinner, cstwinner, apsywinner, fstwinner, statwinner, envswinner, fmwinner]
    return list

def getPopularPoster():
    popular = Poster.query.order_by(Poster.Score_s.desc()).first()
    return popular

def getBestPoster():
    best = Poster.query.order_by(Poster.Score_h.desc()).first()
    return best



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect(url_for('homea'))
        c = CommitteeMember.query.filter(CommitteeMember.username == request.form['username']).first()
        if c.password == request.form['password']:
            # this is judge or head judge
            if c.username[0] == 'J':
                return redirect(url_for('homej'))
            if c.username[0] == 'H':
                return redirect(url_for('homeh'))
            if c.username[0] == 'D':
                return redirect(url_for('draw'))
        else:
            return redirect(url_for('login'))
            # wrong password
        if CommitteeMember.query.filter(CommitteeMember.username.startswith('Judge')).count() == 0:
            return redirect(url_for('homea'))
        elif request.form['username'] == 'stu' and request.form['password'] == 'stu':
            return redirect(url_for('homes'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', error=error)


# For administrator
@app.route('/home_a', methods=['GET', 'POST'])
def homea():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Download':
            return redirect(url_for('downloadall'))
    return render_template('home_a.html', Poster=Poster.query.all())


@app.route('/searcha', methods=['GET', 'POST'])
def searcha():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Search':
            x = request.form.get('searchtext')
            return redirect(url_for('home_a', id=x))
    return render_template('search_a.html')


@app.route('/home_a/<int:id>', methods=['GET', 'POST'])
def home_a(id):
    result = Poster.query.filter(Poster.posterID == id).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Delete':
            Poster.delPosterInfo(result)
        elif request.form['submit_button'] == 'Edit':
            return redirect(url_for('edit'))
        elif request.form['submit_button'] == 'Home':
            return redirect(url_for('homea'))
        return redirect(url_for('homea'))
    return render_template('info_a.html', Poster=result)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            if not request.form['posterID'] or not request.form['programmeName'] or not request.form['author'] or not \
            request.form['email'] or not request.form['abstract']:
                flash('Please enter all the fields', 'error')
            else:
                uploadjpg()
                poster = Poster(request.form['posterID'], request.form['programmeName'], request.form['author'],
                                request.form['email'], request.form['abstract'])
                Poster.addPosterInfo(poster)
                return redirect(url_for('homea'))
        elif request.form['submit_button'] == 'SubmitExcel':
            fi = request.files['file1']
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static/excel', secure_filename(fi.filename))
            Poster.addAllPoster(fi, upload_path)
            return redirect(url_for('homea'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    results = Poster.query.filter(Poster.posterID == id).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Change':
            uploadjpg()
            Poster.editPosterInfo(results)
            return redirect(url_for('homea'))
        return render_template('home_a.html')
    return render_template("edit.html", Poster=results)


@app.route('/setupConferenceRules', methods=['GET', 'POST'])
def setupConferenceRules():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Set':
            if not request.form['numOfJudges'] or not request.form['numOfHeadJudge'] \
                    or not request.form['numOfFirstPrize'] or not request.form['numOfSecondPrize'] \
                    or not request.form['numOfThirdPrize'] or not request.form['numOfLuckyDraw'] \
                    or not request.form['info']:
                flash('Please enter all the fields', 'error')
            else:
                Rule.setUpRule(request.form['numOfJudges'], request.form['numOfHeadJudge'],
                               request.form['numOfFirstPrize'],
                               request.form['numOfSecondPrize'], request.form['numOfThirdPrize'],
                               request.form['numOfLuckyDraw'],
                               request.form['info'])
                flash('Rule was successfully set up')
                return redirect(url_for('homea'))
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homea'))
    return render_template("setupConferenceRules.html")


@app.route('/rulea', methods=['GET', 'POST'])
def rulea():
    return render_template("rule_a.html", Rule=Rule.query.all())


@app.route('/winnerlista', methods=['GET', 'POST'])
def winnerlista():
    list = getWinnerList()
    popular = getPopularPoster()
    best = getBestPoster()
    return render_template('winnerList_a.html', list=list, popular=popular, best=best)


@app.route('/passwordInfo', methods=['GET', 'POST'])
def passwordInfo():
    if request.method == 'POST':
        if request.form['submit_button'] == 'generate password':
            db.create_all()
            ruleDemo = Rule.query.first()
            numOfJudges = ruleDemo.numOfJudges
            numOfHeadJudge = ruleDemo.numOfHeadJudge
            CommitteeMember.generateAllPwd(numOfJudges, numOfHeadJudge)
            return redirect(url_for('passwordInfo'))
        elif request.form['submit_button'] == 'Send':
            return render_template('attendeeGetLink.html')
        else:
            pass
    return render_template("passwordInfo.html", CommitteeMember=CommitteeMember.query.all())

@app.route('/download', methods=['POST', 'GET'])
def upload():
    list_all = Poster.query.order_by(Poster.posterID).all()
    return render_template('download.html', tasks=list_all)

@app.route('/download/downloadall', methods=['GET', 'POST'])  # get the id of the daily task
def downloadall():
    content = [['id', 'author', 'Programme', 'programmeName', 'abstract']]
    activity = Poster.query.order_by(Poster.posterID).all()

    if activity:
        for value in activity:
            new = [value.posterID, value.author, value.email, value.programmeName, value.abstract]
            content.append(new)
        return excel.make_response_from_array(content, "xls", file_name="Poster_info.xls")
    else:
        return "Database empty!"
    for value in activity:
        new = []
        new = [value.posterID, value.author, value.email, value.programmeName, value.abstract]
        content.append(new)
    return excel.make_response_from_array(content, "xls", file_name="Poster_info.xls")


# For judge
@app.route('/home_j', methods=['GET', 'POST'])
def homej():
    return render_template('home_j.html', Poster=Poster.query.all())


@app.route('/searchj', methods=['GET', 'POST'])
def searchj():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Search':
            x = request.form.get('searchtext')
            return redirect(url_for('home_j', id=x))
    return render_template('search_j.html')


@app.route('/home_j/<int:id>', methods=['GET', 'POST'])
def home_j(id):
    result = Poster.query.filter(Poster.posterID == id).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homej'))
        elif request.form['submit_button'] == 'Score':
            s = request.form.get('score')
            Poster.giveScore(id, s)
            return redirect(url_for('homej'))
        return redirect(url_for('homej'))
    return render_template('info_j.html', Poster=result)


@app.route('/rulej', methods=['GET', 'POST'])
def rulej():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homej'))
        else:
            pass
    return render_template("rule_j.html", Rule=Rule.query.all())


@app.route('/winnerlistj', methods=['GET', 'POST'])
def winnerlistj():
    list = getWinnerList()
    popular = getPopularPoster()
    best = getBestPoster()
    return render_template('winnerList_j.html', list=list, popular=popular, best=best)


# For headjudge
@app.route('/home_h', methods=['GET', 'POST'])
def homeh():
    return render_template('home_h.html', Poster=Poster.query.all())


@app.route('/home_h/<int:id>', methods=['GET', 'POST'])
def home_h(id):
    result = Poster.query.filter(Poster.posterID == id).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homeh'))
        elif request.form['submit_button'] == 'Score':
            s = request.form.get('score')
            Poster.giveScoreh(id, s)
            return redirect(url_for('homeh'))
        return redirect(url_for('homeh'))
    return render_template('info_h.html', Poster=result)


@app.route('/winnerListh', methods=['GET', 'POST'])
def winnerListh():
    list = getWinnerList()
    popular = getPopularPoster()
    best = getBestPoster()
    return render_template('winnerList_h.html', list=list, popular=popular, best=best)


@app.route('/search_h', methods=['GET', 'POST'])
def searchh():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Search':
            x = request.form.get('searchtext')
            return redirect(url_for('home_h', id=x))
    return render_template('search_h.html')


@app.route('/ruleh', methods=['GET', 'POST'])
def ruleh():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homeh'))
        else:
            pass
    return render_template("rule_h.html", Rule=Rule.query.all())


def check_email_url(email_address):
    # check '@'
    at_count = 0
    for element in email_address:
        if element == '@':
            at_count = at_count + 1

    if at_count != 1:
        return 0

    # check ' '
    for element in email_address:
        if element == ' ':
            return 0

    # check 'uic mail'
    postfix = email_address[-15:]
    if postfix != 'mail.uic.edu.cn':
        return 0

    # check char
    for element in email_address:
        if element.isalpha() == False and element.isdigit() == False:
            if element != '.' and element != '@' and element != '_':
                return 0
    return 1


# For student is not vote
@app.route('/linkLogin/<name>', methods=['GET', 'POST'])
def attendeeLogin(name):
    if request.method == 'POST':
        if Attendee.query.filter(Attendee.email == request.form['Email']).count() != 0:
            if request.form['submit_button'] == 'SIGN IN':
                global att
                att = Attendee.query.filter(Attendee.email == request.form['Email']).first()
                print(att.voteStatus)
                if att.voteStatus == '1':
                    print('True')
                    return redirect(url_for('homesv'))
                else:
                    return redirect(url_for('homes'))
        else:
            flash('Wrong Email or the Account not activated', 'error')
    return render_template('linkLogin.html')


@app.route('/attendeeGetLink', methods=['GET', 'POST'])
def attendeeGetLink():
    if request.method == 'POST':
        # send email to the link
        if not request.form['Email']:
            flash('Please enter your email', 'error')
        elif check_email_url(request.form['Email']) == 0:
            print("Wrong")
        else:
            msg = Message('Website link for CMS', sender='hanzi8888@126.com', recipients=[request.form['Email']])
            msg.body = "localhost:5000/linkLogin/" + request.form['Email']
            mail.send(msg)
            # add the email into database
            if Attendee.query.filter(Attendee.email == request.form['Email']).count() == 0:
                a = Attendee(0, "p930026012@mail.uic.edu.cn", 0)
                a.voteStatus = 0
                idl = Attendee.query.order_by(-Attendee.id).first()
                a.id = idl.id + 1
                a.email = request.form['Email']
                db.session.add(a)
                db.session.commit()
            else:
                # already add it, do nothing
                pass
    return render_template('attendeeGetLink.html')


@app.route('/home_s', methods=['GET', 'POST'])
def homes():
    return render_template('home_s.html', Poster=Poster.query.all())


@app.route('/searchs', methods=['GET', 'POST'])
def searchs():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Search':
            x = request.form.get('searchtext')
            return redirect(url_for('home_s', id=x))
    return render_template('search_s.html')


@app.route('/home_s/<int:id>', methods=['GET', 'POST'])
def home_s(id):
    result = Poster.query.filter(Poster.posterID == id).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homes'))
        elif request.form['submit_button'] == 'Vote':
            Attendee.giveVotes(att, 1)
            Poster.giveVote(id)
            return redirect(url_for('homesv'))
        return redirect(url_for('homes'))
    return render_template('info_s.html', Poster=result)


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homes'))
        else:
            pass
    return render_template("rule_s.html", Rule=Rule.query.all())


# For student who is voted
@app.route('/home_s_v', methods=['GET', 'POST'])
def homesv():
    return render_template('home_s_v.html', Poster=Poster.query.all())


@app.route('/home_s_v/<int:id>', methods=['GET', 'POST'])
def home_s_v(id):
    result = Poster.query.filter(Poster.posterID == id).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homesv'))
        return redirect(url_for('homesv'))
    return render_template('info_s_v.html', Poster=result)


@app.route('/searchsv', methods=['GET', 'POST'])
def searchsv():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Search':
            x = request.form.get('searchtext')
            return redirect(url_for('home_s_v', id=x))
    return render_template('search_s_v.html')


@app.route('/rulesv', methods=['GET', 'POST'])
def rulesv():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Home':
            return redirect(url_for('homesv'))
        else:
            pass
    return render_template("rule_s_v.html", Rule=Rule.query.all())


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Search':
            x = request.form.get('searchtext')
            return redirect(url_for('home', id=x))
    return render_template('search.html')


@app.route('/luckydraw', methods=['GET', 'POST'])
def draw():
    value = Attendee.query.count()
    abc = Attendee.query.filter_by(id=random.randint(2, value)).first()
    s = abc.email
    if request.form.get('action2') == 'html2':
        stop = 1
        sendEmail(s)
        return render_template("luckydraw.html", s=s, stop=stop)
    else:
        stop = 0
        return render_template("luckydraw.html", s=s, stop=stop)

if __name__ == '__main__':
    db.create_all()
    # app.run(host='0.0.0.0',port=8000,debug = False)
    app.run(debug=True)
