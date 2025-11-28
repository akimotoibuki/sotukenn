from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from .models import User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user = User.query.filter_by(user_id=user_id).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            flash('ログイン成功！')
            return redirect(url_for('home.home'))  # ホーム画面に遷移
        else:
            flash('ユーザーIDまたはパスワードが間違っています')
            return redirect(url_for('login.login'))

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました')
    return redirect(url_for('login.login'))