import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.forms.spot_form import SpotForm

spot_bp = Blueprint("spot", __name__, url_prefix="/spot")

UPLOAD_FOLDER = "app/static/uploads"


@spot_bp.route("/post", methods=["GET", "POST"])
def post_spot():
    form = SpotForm()

    # POST時の処理（投稿ボタン押下）
    if request.method == "POST" and form.validate_on_submit():

        # 画像保存
        img_file = form.image.data
        filename = None
        if img_file:
            filename = secure_filename(img_file.filename)
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            img_file.save(img_path)

        # フォームの内容取得
        name = form.name.data
        intro = form.introduction.data
        url = form.url.data
        tag = form.tag.data
        genre = form.genre.data

        # ここでDBに保存する処理を書く
        # （例）
        # new_spot = Spot(name=name, intro=intro, url=url, tag=tag, genre=genre, image=filename)
        # db.session.add(new_spot)
        # db.session.commit()

        flash("スポットを投稿しました！", "success")
        return redirect(url_for("spot.post_spot"))

    return render_template("spot_post.html", form=form)
