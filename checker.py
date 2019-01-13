from htmldom import htmldom
from hashlib import md5
from flask import render_template, redirect, url_for
from flask_app import app, db
from forms import LoginForm, RegistrationForm, UrlForm
from models import User,  Url
from flask_login import login_required, login_user, current_user, logout_user



def check_url(url, atribute, old_hash):
    dom = htmldom.HtmlDom(url)
    dom.createDom()
    content = dom.find('*.' + atribute).text()
    hash = md5(bytearray(content, encoding='utf-8'))
    res = hash.hexdigest()
    if res != old_hash:
        print('WTF??????')
    print(res)



urls = Url.query.filter_by(user_id=3).all()
for url in urls:
    print(str(url.url) + '  ---  ' + str(type(url.hash)))
    update = Url.query.filter_by(id=url.id).first()
    new_url = Url(url=update.url, user_id=3, hash='')
    db.session.add(new_url)
    db.session.delete(update)
    db.session.commit()



dom = htmldom.HtmlDom('https://vk.com/im?peers=119176043&sel=139532734')
dom.createDom()
content = dom.find('*.' + 'hui').text()
if content == '':
    print('hui')