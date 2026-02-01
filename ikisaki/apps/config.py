from pathlib import Path

basedir = Path(__file__).parent.parent

class BaseConfig:
	SECRET_KEY = "1234567890"
	WTF_CSRF_SECRET_KEY = "ABCDEFGHIJKL"
	UPLOAD_FOLDER = str(Path(basedir, "apps", "static", "uploads"))
	UPLOAD_URL = "/static/uploads/"
	SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'ikisaki.sqlite'}"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True

	ADMIN_USER_ID = ["admin"]	# 管理者権限のuser_id
	WEEKDAY_LABELS = ["日", "月", "火", "水", "木", "金", "土"]
	FIRST_WEEKDAY = 6  # 日曜始まり
	VIEW_DATE = 3	# カレンダーが1画面に表示する月数

	SPOT_LIST = {
		1: "心霊",
		2: "絶景",
		3: "水族館",
		4: "遊園地",
	 }

	TAG_LIST = [
		"家族",
		"友人",
		"デート",
		"人気",
	]
