'''
スケジュール処理
'''
from datetime import datetime
from flask import request, jsonify
from flask_login import login_required, current_user

from apps.app import db
from apps.ikisaki.models import Schedule
from apps.ikisaki.blueprint import ikisaki

@ikisaki.route("/schedule/create", methods=["POST"])
@login_required
def schedule_create():
	# JSONで受け取る: {"ymd":"20260203", "schedule":"会議"}
	data = request.get_json(silent=True) or {}

	ymd_str = (data.get("ymd") or "").strip()
	text = (data.get("schedule") or "").strip()

	# --- バリデーション ---
	if not ymd_str:
		return jsonify(ok=False, error="ymd is required"), 400

	try:
		ymd_date = datetime.strptime(ymd_str, "%Y%m%d").date()
	except ValueError:
		return jsonify(ok=False, error="ymd format must be YYYYMMDD"), 400

	# --- 空文字は削除扱い ---
	if text == "":
		Schedule.query.filter_by(user_id=current_user.user_id, ymd=ymd_date).delete()
		db.session.commit()
		return jsonify(ok=True, ymd=ymd_str, schedule="")

	# --- 追加 or 更新 ---
	s = Schedule(user_id=current_user.user_id, ymd=ymd_date, schedule=text, )
	db.session.merge(s)
	db.session.commit()

	return jsonify(ok=True, ymd=ymd_str, schedule=text)

