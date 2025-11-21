from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    from app.routes.spot_routes import spot_bp
    app.register_blueprint(spot_bp)

    return app
