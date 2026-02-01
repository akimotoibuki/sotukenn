# from datetime import datetime

from apps.app import db #, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    schedules = db.relationship("Schedule", back_populates="user", cascade="all, delete-orphan")

    def get_id(self):
        return str(self.user_id)

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Schedule(db.Model):
    __tablename__ = "schedule"

    user_id = db.Column(db.String, db.ForeignKey("user.user_id"), primary_key=True, nullable=False)
    ymd = db.Column(db.Date, primary_key=True, nullable=False)
    schedule = db.Column(db.String, nullable=False)

    user = db.relationship("User", back_populates="schedules")

class Spot(db.Model):
    __tablename__ = "spot"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.Integer, nullable=False)
    introduction = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=True)
    user_id = db.Column(db.String, nullable=False)

    tags = db.relationship("SpotTag", backref="spot", cascade="all, delete-orphan")
    pictures = db.relationship("SpotPicture", backref="spot", cascade="all, delete-orphan")


class SpotTag(db.Model):
    __tablename__ = "spot_tag"

    spot_id = db.Column(db.Integer, db.ForeignKey("spot.id"), primary_key=True, nullable=False)
    tag = db.Column(db.String, primary_key=True, nullable=False)


class SpotPicture(db.Model):
    __tablename__ = "spot_picture"

    spot_id = db.Column(db.Integer, db.ForeignKey("spot.id"), primary_key=True, nullable=False)
    url = db.Column(db.String, primary_key=True, nullable=False)
