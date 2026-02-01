'''
スポット処理
'''
from pathlib import Path
from flask import current_app, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from apps.app import db
from apps.ikisaki.models import Spot, SpotTag, SpotPicture
from apps.ikisaki.forms import SpotForm, SpotSearchForm
from apps.ikisaki.utils import save_upload_to_static
from apps.ikisaki.blueprint import ikisaki

@ikisaki.route("/spot/upsert", methods=["GET", "POST"])
@ikisaki.route("/spot/upsert/<int:spot_id>", methods=["GET", "POST"])
@login_required
def spot_upsert(spot_id=None):
	ssform = SpotSearchForm()
	form = SpotForm()

	# 更新対象のspot取得（spot_idがあるときだけ）
	spot = None
	if spot_id is not None:
		# 他人のspotを編集できないように user_id も条件に入れる
		spot = Spot.query.filter_by(id=spot_id, user_id=current_user.user_id).first()

		# spot_idが存在しなければトップページを表示
		if spot is None:
			flash("対象のスポットが存在しません")
			return redirect(url_for("ikisaki.index"))

		# GETなら既存値をフォームへ
		if request.method == "GET":
			form.name.data = spot.name
			form.introduction.data = spot.introduction
			form.url.data = spot.url

	# POST：保存
	if form.validate_on_submit():
		# genre_id は必ず int にして入れる（None/空だとエラーになるので）
		genre_id_str = request.form.get("genre_id")
		# JSで初期チェックしてる前提だけど、念のため
		if not genre_id_str:
			flash("ジャンルを選択してください")
			return redirect(request.url)

		# 共通：入力値
		data = {
			"name": form.name.data,
			"genre_id": int(genre_id_str),
			"introduction": form.introduction.data,
			"url": form.url.data,
		}

		# 更新時に削除する画像ファイルを控える（commit後に消す）
		delete_file_paths = []

		if spot is None:
			# --- 新規作成 ---
			spot = Spot(user_id=current_user.user_id, **data)
			db.session.add(spot)
		else:
			# --- 更新 ---
			spot.name = data["name"]
			spot.genre_id = data["genre_id"]
			spot.introduction = data["introduction"]
			spot.url = data["url"]

			# タグは入れ替え
			spot.tags.clear()

			# 更新時：チェックされた既存画像を削除（DB＋ファイル）
			delete_urls = request.form.getlist("delete_pictures")  # ["xxx.jpg", ...]
			if delete_urls:
				upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
				pics_to_delete = [p for p in spot.pictures if p.url in delete_urls]
				for p in pics_to_delete:
					# DB削除
					db.session.delete(p)
					# ファイル削除は後で
					if p.url:
						delete_file_paths.append(upload_dir / p.url)










		# タグ追加（checkbox）
		for t in request.form.getlist("tags"):
			spot.tags.append(SpotTag(tag=t))

		# 無制限画像追加（name="photos" multiple）
		for fs in request.files.getlist("photos"):
			purl = save_upload_to_static(fs)
			if purl:
				spot.pictures.append(SpotPicture(url=purl))

		db.session.commit()

		# commit成功後にファイル削除（失敗してもDBは正常）
		for p in delete_file_paths:
			try:
				p.unlink(missing_ok=True)
			except Exception:
				pass

		flash("スポットを保存しました")
		return redirect(url_for("ikisaki.index"))

	# テンプレでチェック状態を保持したい場合に渡す
	selected_genre_id = None
	selected_tags = set()
	if spot is not None:
		selected_genre_id = str(spot.genre_id) if spot.genre_id is not None else None
		selected_tags = {st.tag for st in spot.tags}

	return render_template(
		"ikisaki/spot_upsert.html",
		ssform=ssform,
		form=form,
		spot=spot,  # None=新規、あり=更新
		selected_genre_id=selected_genre_id,
		selected_tags=selected_tags,
	)

	# テンプレでチェック状態を保持したい場合に渡す
	selected_genre_id = None
	selected_tags = set()
	if spot is not None:
		selected_genre_id = str(spot.genre_id) if spot.genre_id is not None else None
		selected_tags = {st.tag for st in spot.tags}

	return render_template(
		"ikisaki/spot_upsert.html",
		ssform=ssform,
		form=form,
		spot=spot,  # Noneなら新規、あれば更新
		selected_genre_id=selected_genre_id,
		selected_tags=selected_tags,
	)

@ikisaki.route("/spot/delete/<spot_id>", methods=["POST"])
@login_required
def spot_delete(spot_id):
	# 他人のspotを編集できないように user_id も条件に入れる
	spot = Spot.query.filter_by(id=spot_id, user_id=current_user.user_id).first()

	# spot_idが存在しなければトップページを表示
	if spot is None:
		return redirect(url_for("ikisaki.index"))

	# 削除対象の画像ファイル（ファイル名）を先に控える
	upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
	file_paths = []
	for pic in getattr(spot, "pictures", []):
		if pic.url:
			file_paths.append(upload_dir / pic.url)

	# DBから削除
	db.session.delete(spot)
	db.session.commit()

	# DB削除が成功したあとにファイル削除
	for p in file_paths:
		try:
			p.unlink(missing_ok=True)
		except Exception:
			pass

	flash("スポットを削除しました")
	return redirect(url_for("ikisaki.index"))


@ikisaki.route("/spot/search", methods=["GET", "POST"])
@login_required
def spot_search():
	ssform = SpotSearchForm()

	# フォームのバリデーションが厳しくて検索で落ちることがあるので、
	# 「入力が空でも検索できる」用途なら validate_on_submit を使わずに進めるのが無難
	name_kw = (ssform.name.data or "").strip()  # 部分一致検索

	genre_ids = request.form.getlist("genre_ids")  # ["1","3",...]
	tags = request.form.getlist("tags")            # ["家族","人気",...]

	q = Spot.query.filter()

	# スポット名（部分一致）
	if name_kw:
		q = q.filter(Spot.name.contains(name_kw))

	# ジャンル（複数チェック → IN検索）
	if genre_ids:
		genre_id_list = []
		for g in genre_ids:
			genre_id_list.append(int(g))
		q = q.filter(Spot.genre_id.in_(genre_id_list))

	# タグ（チェックされたタグを「どれか1つでも含む」検索）
	if tags:
		q = q.filter(Spot.tags.any(SpotTag.tag.in_(tags)))

	spots = q.all()

	return render_template(
		"ikisaki/spot_search.html",
		ssform=ssform,
		name_kw=name_kw,
		genre_ids=genre_ids,
		tags=tags,
		spots=spots,
	)

@ikisaki.route("/spot/detail/<spot_id>", methods=["GET", "POST"])
@login_required
def spot_detail(spot_id):
	ssform = SpotSearchForm()
	form = SpotForm()

	spot = Spot.query.filter_by(id=spot_id).first()
	# spot_idが存在しなければトップページを表示
	if spot is None:
		return redirect(url_for("ikisaki.index"))
     
	spot_list = current_app.config.get("SPOT_LIST", {})
	genre_name = spot_list.get(spot.genre_id, str(spot.genre_id))

	return render_template(
		"ikisaki/spot_detail.html",
		ssform=ssform,
		form=form,
		spot=spot,
		genre_name=genre_name,
		)
