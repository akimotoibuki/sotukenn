from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/spot')
def spot():
    return render_template('spot.html')

@home_bp.route('/spotdetail')
def spotdetail():
    return render_template('spotdetail.html')

@home_bp.route('/spotpost')
def spotpost():
    return render_template('spotpost.html')

@home_bp.route('/favorite')
def favorite():
    return render_template('favorite.html')