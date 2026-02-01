'''
インデックス
'''
import calendar
from datetime import date
from flask import current_app, render_template, request
from flask_login import login_required, current_user

#from apps.app import db
from apps.ikisaki.models import Schedule
from apps.ikisaki.forms import SpotSearchForm
from apps.ikisaki.utils import is_admin
from apps.ikisaki.blueprint import ikisaki

@ikisaki.route("/")
@login_required
def index():

	ssform = SpotSearchForm()

	base_ym = request.args.get("ym", type=int)	# 6桁の年月（例: 202602）

	today = date.today()
	year = today.year
	month = today.month
	if base_ym:
		year = base_ym // 100	# 上4桁は年
		month = base_ym % 100	# 下2桁は月

	# 月の値が不正だった場合は今日の年月
	if month < 1 or month > 12:
		year = today.year
		month = today.month

	cal = calendar.Calendar(current_app.config["FIRST_WEEKDAY"])  # カレンダーの始まりの曜日

	# 指定月からVIEW_DATEか月分
	months = []
	y, m = year, month
	for _ in range(current_app.config["VIEW_DATE"]):
		weeks = cal.monthdayscalendar(y, m)
		months.append({
			"year": y,
			"month": m,
			"weeks": weeks,
		})

		if m == 12:
			y += 1
			m = 1
		else:
			m += 1

	# YYYYMM を月単位で加減算するヘルパ
	def add_months_ym(ym: int, delta: int) -> int:
		y = ym // 100
		m = ym % 100
		idx = y * 12 + (m - 1) + delta
		ny = idx // 12
		nm = idx % 12 + 1
		return ny * 100 + nm

	current_ym = year * 100 + month
	prev_ym = add_months_ym(current_ym, current_app.config["VIEW_DATE"] * -1)
	next_ym = add_months_ym(current_ym, current_app.config["VIEW_DATE"])

	### スケジュールを挿入

	# 表示している期間を求める
	start_date = date(months[0]["year"], months[0]["month"], 1)

	last = months[-1]
	end_date = date(last["year"], last["month"], calendar.monthrange(last["year"], last["month"])[1])

	# その期間のスケジュールをまとめて取得
	schedules = (
		Schedule.query
		.filter(Schedule.user_id == current_user.user_id)
		.filter(Schedule.ymd >= start_date)
		.filter(Schedule.ymd <= end_date)
		.all()
	)

	# 日付 → 予定文字列 のハッシュにする
	schedule_map = {}
	for s in schedules:
		schedule_map[s.ymd] = s.schedule

	return render_template(
		"ikisaki/index.html",
		ssform=ssform,
		base_yearmonth=current_ym,   # 表示基準（YYYYMM）
		months=months,               # VIEW_DATEか月分
		weekday_labels=current_app.config["WEEKDAY_LABELS"],
		prev_yearmonth=prev_ym,
		next_yearmonth=next_ym,
		schedule_map=schedule_map,
		date=date,
		is_admin=is_admin(current_user.user_id),
	)
