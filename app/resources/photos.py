from flask_restful import Resource, reqparse
from models.user import UserModel
from models.photo import PhotoModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os

class Photo(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("caption", type=str, required=False)
	parser.add_argument("filepath", type=str, required=True, help="field can't be empty")


	@jwt_required
	def post(self):
		_id = get_jwt_identity()
		user = UserModel.find_by_id(_id)
		data = Photo.parser.parse_args()
		ext = os.path.basename(data["filepath"]).split('.')[-1].upper() #get the file extension
		if user:
			if not PhotoModel.validate(ext):
				return {"msg" : "invalid filetype"}, 400
			else:
				try:
					data["date_created"] = datetime.date(datetime.now())
					photo = PhotoModel(**data)
					photo.save_to_db()
					user.add_photo(photo)
					return {"msg" : "successfully added_photo", "filepath" : photo.filepath},200
				except Exception as e:
					print(e, e.with_traceback())
		return {"msg" : "user not found"},400

	@jwt_required
	def delete(self, photo_id):
		_id = get_jwt_identity()
		user = UserModel.find_by_id(_id)
		photo = PhotoModel.find_by_id(_id)
		if user:
			if photo:
				photo.delete_from_db()
				return {"msg" : "photo successfully deleted"}, 200
			return {"msg" : "photo not found"}, 400
		return {"msg" : "user not found"}, 400


class Add_Dp(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument("caption", type=str, required=False)
	parser.add_argument("filepath", type=str, required=True, help="field can't be empty")

	@jwt_required
	def post(self):
		_id = get_jwt_identity()
		data = Add_Dp.parser.parse_args()
		user = UserModel.find_by_id(_id)
		ext = os.path.basename(data["filepath"]).split(".")[-1]
		if user:
			if not PhotoModel.validate(ext.upper()):
				return {"msg" : "invalid filetype"},400
			else:	
				data["date_created"] = datetime.date(datetime.now())
				photo = PhotoModel(**data)
				photo.save_to_db()
				user.add_photo(photo)
				new_dp_path = user.set_dp(photo.filepath)
				return {"filepath" :new_dp_path,"msg":"successfully uploaded photo"},200

		return {"msg" : "user doesn't exist"}, 400


class Set_Dp(Resource):

		@jwt_required
		def post(self, photo_id):
			_id = get_jwt_identity()
			user = UserModel.find_by_id(_id)
			if user:
				photo = PhotoModel.find_by_id(photo_id)
				new_dp_path = user.set_dp(photo.filepath)
				return {"filepath" : new_dp_path, "msg" : "DP path successfully changed"},200

			return {"msg" : "user not found"}, 400

class Photos(Resource):

	@jwt_required
	def get(self, username):
		user = UserModel.find_by_username(username)
		if user:
			photos = user.get_photos()
			return {"photos" : photos}, 200
		return {"msg" : "user doesn't exist"}, 404