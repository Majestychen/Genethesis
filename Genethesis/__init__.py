from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '01940eb0bb530930686cdcfe044c1ad3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message = '您的登陆状态太过久远已经自然死亡，请重新登陆。'

from Genethesis.main.routes import main
from Genethesis.users.routes import users
from Genethesis.articles.routes import articles
from Genethesis.illustrations.routes import illustrations

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(articles)
app.register_blueprint(illustrations)