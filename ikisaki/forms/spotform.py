from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, URL
from flask_wtf.file import FileField, FileAllowed


class SpotForm(FlaskForm):
    name = StringField("スポット名", validators=[DataRequired()])
    image = FileField("写真", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    introduction = TextAreaField("紹介文", validators=[DataRequired()])
    url = StringField("URL", validators=[URL(message="正しいURLではありません")])
    tag = StringField("タグ", validators=[DataRequired()])
    genre = SelectField(
        "ジャンル",
        choices=[
            ("restaurant", "レストラン"),
            ("cafe", "カフェ"),
            ("park", "公園"),
            ("museum", "博物館"),
            ("other", "その他")
        ],
        validators=[DataRequired()]
    )
