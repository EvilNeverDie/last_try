from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)

db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from views import *


if __name__ == '__main__':
    app.run(debug=True)


