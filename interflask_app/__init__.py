from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from interflask_app.config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
ma = Marshmallow(app)
bp = Blueprint('api', __name__)
login = LoginManager(app)
login.login_view = 'login'

from interflask_app import routes, models