'''
ユーザー処理
'''
from flask import current_app, render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError

from apps.app import db
from apps.ikisaki.models import Spot, User
from apps.ikisaki.forms import UserForm, UserUpdateForm, LoginForm, SpotSearchForm
from apps.ikisaki.utils import is_admin
from apps.ikisaki.blueprint import ikisaki
from flask_login import login_required, current_user, login_user, logout_user

@ikisaki.route("/user_create", methods=["GET","POST"])
def user_create():
	form = UserForm()
	if form.validate_on_submit():
		user = User(
			user_id = form.user_id.data,
			password = form.password.data,
		)
		
		db.session.add(user)

		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
			flash("そのユーザーIDは既に使われています")
			return render_template("ikisaki/user_create.html", form=form)

		login_user(user)
		
		next_ = request.args.get("next")
		if next_ is None or not next_.startswith("/"):
			next_ = url_for("ikisaki.index")
		return redirect(next_)

	return render_template("ikisaki/user_create.html", form=form)

@ikisaki.route("/user/update", methods=["GET", "POST"])
@login_required
def user_update():
	ssform = SpotSearchForm()
	form = UserUpdateForm()

	# ログイン中ユーザーを取得（必ず1回だけ）
	user = User.query.filter_by(user_id=current_user.user_id).first()
	if user is None:
		flash("ユーザーが存在しません")
		return redirect(url_for("ikisaki.login"))

	# POST: 更新
	if form.validate_on_submit():
		# パスワードは未入力なら更新しない（安全）
		new_pw = (form.password.data or "").strip()
		if new_pw:
			user.password = new_pw
			db.session.commit()
			flash("ユーザー情報を更新しました")
		else:
			flash("パスワードが未入力のため更新しませんでした")

		return redirect(url_for("ikisaki.user_update"))

	return render_template(
		"ikisaki/user_update.html",
		ssform=ssform,
		form=form,
		user=user,
	)


@ikisaki.route("/user/delete/<user_id>", methods=["GET", "POST"])
@login_required
def user_delete(user_id):

	# 管理者以外はトップへ
	if not is_admin(current_user.user_id):
		return redirect(url_for("ikisaki.index"))

	# 自分自身は削除させない(念のため)
	if user_id == current_user.user_id:
		flash("ログインユーザー自身は削除できません")
		return redirect(url_for("ikisaki.user_list"))

	user = User.query.filter_by(user_id=user_id).first()

	if user is None:
		flash("対象のユーザーが存在しません")
		return redirect(url_for("ikisaki.user_list"))

	# 管理者ID（先頭を使う）
	admin_ids = current_app.config.get("ADMIN_USER_ID", [])
	admin_user_id = admin_ids[0]

	# 削除されるユーザーの spot を管理者に付け替える
	Spot.query.filter_by(user_id=user_id).update(
		{"user_id": admin_user_id}
	)

	# ユーザー削除
	db.session.delete(user)
	db.session.commit()

	flash(f"{user_id} を削除しました（スポットは {admin_user_id} に引き継ぎました）")

	# ユーザー管理画面にリダイレクト
	return redirect(url_for("ikisaki.user_list"))


@ikisaki.route("/user/list", methods=["GET"])
@login_required
def user_list():
	ssform = SpotSearchForm()

	# 管理者以外はトップへ
	if not is_admin(current_user.user_id):
		return redirect(url_for("ikisaki.index"))

	# ユーザー一覧
	users = User.query.order_by().all()

	return render_template(
		"ikisaki/user_list.html",
		ssform=ssform,
		users=users,
	)

@ikisaki.route("/login", methods=["GET","POST"])
def login():
	ssform = SpotSearchForm()
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(user_id=form.user_id.data).first()

		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for("ikisaki.index"))
		
		flash("ユーザー名かパスワードが不正です")

	return render_template("ikisaki/login.html", ssform=ssform, form=form)

@ikisaki.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("ikisaki.login"))

