from flask import Blueprint, render_template, request, redirect, url_for, flash
from ikisaki.app.models import User
from werkzeug.security import generate_password_hash

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if User.query.filter_by(user_id=user_id).first():
            flash("このIDはすでに使われています", "error")
            return redirect(url_for('register.register'))

        new_user = User(user_id=user_id, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash("登録が完了しました！ログインしてください", "success")
        return redirect(url_for('login'))  # ログイン画面へ
    return render_template('register.html')