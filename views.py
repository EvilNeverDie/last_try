from flask import render_template, redirect, url_for, jsonify, request
from flask_app import app, db
from forms import LoginForm, RegistrationForm, UrlForm
from models import User,  Url
from flask_login import login_required, login_user, current_user, logout_user
from htmldom import htmldom
from hashlib import md5
import datetime, threading, time, random


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user:
           if user.password == form.password.data:
               login_user(user, remember=form.remember_me.data)
               return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():

        selector = str(form.username.data) + '_' + str(random.randint(0, 1000))
        new_user = User(login=form.username.data, password=form.password.data, email=form.email.data, user_selector=selector )
        db.session.add(new_user)
        db.session.commit()

        return '<h1> User created successfuly </h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = UrlForm()

    if form.validate_on_submit():
        new_url = Url(url=form.Url.data, user_id=current_user.id, hash='', flag=0)
        db.session.add(new_url)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('dashboard.html',  form=form, name=current_user.login, selector=current_user.user_selector)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/startCheck', methods=['GET', 'POST'])
@login_required
def startCheck():
    id_user = current_user.id

    atribut = current_user.user_selector
    urls = Url.query.filter_by(user_id=id_user).all()
    def check_the_urls(urls, atribute, id):
        next_call = time.time()
        while True:
            for url in urls:
                hash = None
                content = None
                print(url.url)
                print(url.id)
                dom = htmldom.HtmlDom(url.url)
                dom.createDom()
                content = dom.find('*.' + atribute).text()
                print(content)
                if content != '':
                    hash = md5(bytearray(content, encoding='utf-8'))
                    res = hash.hexdigest()

                    if url.hash == '':
                        print('empty hash')
                        update = Url.query.filter_by(id=url.id).first()
                        new_url = Url(url=update.url, user_id=id, hash=str(res))
                        db.session.add(new_url)
                        db.session.delete(update)
                        db.session.commit()
                        print('Jonny, hash sucsessfuly updated')
                        continue

                    elif str(res) != str(url.hash):
                        rem = Url.query.filter_by(id=url.id).first()
                        new_url = Url(url=rem.url, user_id=id, hash=rem.hash, flag=1)
                        db.session.add(new_url)
                        db.session.delete(rem)
                        db.session.commit()
                        print('WTF Jonny, this shit is not same')
                        continue

            datetime.datetime.now()
            next_call = next_call + 60
            time.sleep(next_call - time.time())
    timerThread = threading.Thread(target=check_the_urls, args=(urls, atribut, id_user))
    timerThread.start()
    return '<h1> Now check is working </h1>'


@app.route('/api_login', methods=['POST'])
def api_login():
    user = User.query.filter_by(login=request.json['login']).first()
    if user:
        if user.password != request.json['password']:
            login_user(user)

            return jsonify({'auth': 'no'})
        else:
            urls = Url.query.filter_by(user_id=user.id).all()
            resp = []
            for url in urls:
                resp.append({"url": url.url, "flag": str(url.flag)})

            return jsonify(resp)


@app.route('/api_get_new_password', methods=['POST'])
def api_get_new_password():
    user = User.query.filter_by(login=request.json['login']).first()
    if user:
        new_user = User(login=user.login, id=user.id, password=request.json['password'], email=user.email
                        , user_selector=user.user_selector)

        urls = Url.query.filter_by(user_id=user.id).all()

        db.session.delete(user)
        db.session.add(new_user)

        for url in urls:
            new_url = Url(url=url.url, user_id=new_user.id, hash=url.hash, flag=url.flag)
            db.session.delete(url)
            db.session.add(new_url)

        db.session.commit()
        return jsonify({'update': 'true'})
    else:
        return jsonify({'login': 'no'})

