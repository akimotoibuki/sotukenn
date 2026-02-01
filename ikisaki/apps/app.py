from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import BaseConfig

db = SQLAlchemy()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "ikisaki.login"
login_manager.login_message = ""

#↓が無いとログイン処理でエラーが出る
@login_manager.user_loader
def load_user(user_id):
    from apps.ikisaki.models import User
    try:
        return User.query.get(user_id)
    except ValueError:
        return None


def create_app(config_key):
	app = Flask(__name__)

	app.config.from_object(BaseConfig)
	login_manager.init_app(app)

	from apps.ikisaki import views as ikisaki_views

	csrf.init_app(app)

	db.init_app(app)
	Migrate(app, db)

	app.register_blueprint(ikisaki_views.ikisaki, url_prefix="/")

	return app
