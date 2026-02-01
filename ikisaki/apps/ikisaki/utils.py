import uuid
from pathlib import Path
from flask import current_app

"""
アップロードされた画像を static/uploads に保存し、
DBに保存するURL（/static/uploads/xxx.jpg）を返す。
未選択なら None。
"""
def save_upload_to_static(file_storage) -> str | None:
	if not file_storage or file_storage.filename == "":
		return None

	ext = Path(file_storage.filename).suffix
	image_uuid_file_name = str(uuid.uuid4()) + ext

	image_path = Path(
		current_app.config["UPLOAD_FOLDER"], image_uuid_file_name
	)
	file_storage.save(image_path)
	return image_uuid_file_name

'''
user_idが管理者の場合はtrue、それ以外はfalse
'''
def is_admin(user_id):
	return (user_id in current_app.config["ADMIN_USER_ID"])

def apply(obj, data: dict):
	for name, value in data.items():
		setattr(obj, name, value)
