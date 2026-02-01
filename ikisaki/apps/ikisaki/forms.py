from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserForm(FlaskForm):
	user_id = StringField(
		"ユーザー名",
		validators=[
			DataRequired(message="ユーザー名は必須です"),
			Length(max=30, message="30文字以内で入力してください"),
		],
	)

	password = PasswordField(
		"パスワード",
		validators=[
			DataRequired(message="パスワードは必須です"),
		],
	)
	submit = SubmitField("新規登録")


class UserUpdateForm(FlaskForm):
	user_id = StringField(
		"ユーザー名",
		render_kw={"readonly": True},  # 表示だけ
	)

	password = PasswordField(
		"新しいパスワード",
		validators=[Optional()],
	)

	submit = SubmitField("更新")

class LoginForm(FlaskForm):
	user_id = StringField(
		"ユーザー名",
		validators=[
			DataRequired("ユーザー名は必須です。"),
		],
	)

	password = PasswordField(
		"パスワード",
		validators = [
			DataRequired("パスワードは必須です。"),
		],
	)

	submit = SubmitField("ログイン")

class ScheduleForm(FlaskForm):
	ymd = StringField(
		"年月日",
		validators=[
			DataRequired("年月日は必須です。"),
		],
	)

	schedule = StringField(
		"スケジュール",
		validators=[
			DataRequired("スケジュールは必須です。"),
		],
	)

	submit = SubmitField("登録")

class SpotForm(FlaskForm):
	name = StringField(
		"スポット名",
		validators=[
			DataRequired("スポット名は必須です。"),
		],
	)

	introduction = TextAreaField(
		"紹介文",
		validators=[
			DataRequired("紹介文は必須です。"),
		],
	)

	url = StringField(
		"URL",
	)

	submit = SubmitField("登録")

class SpotSearchForm(FlaskForm):
	name = StringField(
		"スポット名",
	)

	submit = SubmitField("検索")
