from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .models import db
from .register import register_bp
from .login import login_bp
from .home import home_bp  # ← Blueprintのインポートだけ先に

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

db.init_app(app)
migrate = Migrate(app, db)

# Blueprintの登録は Flaskインスタンス生成後に！
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)

if __name__ == '__main__':
    app.run(debug=True)