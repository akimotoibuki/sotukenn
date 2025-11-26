from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    app.config.from_object("app.config.Config")  # ← config.py が必要

    db.init_app(app)
    Migrate(app, db)

    # Blueprint登録
    from .home import home_bp
    from .login import login_bp
    from .register import register_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)

    return app