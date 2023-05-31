from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager
from .methods import mine_block

import sys
db = SQLAlchemy()
DB_NAME = "database.db"
PORT =  sys.argv[1]
from .blockchain import Blockchain

blockchain = Blockchain()
blockchain1 = Blockchain()


mine_block(blockchain, 0,"Ellen Geller", "10.10.1990", "zapalenie stawów","covid")
mine_block(blockchain1, 1, "John Silva", "01.01.1980", "brak", "brak")


blocks = [blockchain, blockchain1]
for b in blocks:
    b.add_node("http://127.0.0.1:5000")
    b.add_node("http://127.0.0.1:5001")
    b.add_node("http://127.0.0.1:5002")
    b.add_node("http://127.0.0.1:5003")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .blockchain_func import blockchain_func

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(blockchain_func, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app
