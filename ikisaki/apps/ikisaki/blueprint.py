from flask import Blueprint

ikisaki = Blueprint(
    "ikisaki",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/ikisaki/static",
)
