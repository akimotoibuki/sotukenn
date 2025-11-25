from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ikisaki.app.models import db
from .register import register_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(register_bp)

if __name__ == '__main__':
    app.run(debug=True)