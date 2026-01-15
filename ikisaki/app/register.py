from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from .models import db, User

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        # 既存ユーザー確認
        if User.query.filter_by(user_id=user_id).first():
            flash('そのユーザーIDは既に登録されています')
            return redirect(url_for('register.register'))

        # 新規登録
        new_user = User(user_id=user_id, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('登録が完了しました！ログインしてください')
        return redirect(url_for('login.login'))

    # ★ GET のときにユーザー一覧を取得してテンプレートに渡す
    users = User.query.all()
    return render_template('register.html', users=users)