from flask_restful import Resource, reqparse
from models.user import UserModel, RevokedToken
from flask_jwt_extended import (
								create_access_token, 
								create_refresh_token, 
								get_jwt_identity, 
								jwt_required, 
								jwt_refresh_token_required,
								get_raw_jwt
								)
from werkzeug.security import safe_str_cmp
from datetime import datetime

class UserRegister(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument("firstname", type = str, required = True, help = "firstname field cannot be empty")
	parser.add_argument("lastname",  type = str, required = True, help = "lastname field cannot be empty")
	parser.add_argument("username",  type = str, required = True, help = "username field cannot be empty")
	parser.add_argument("password",  type = str, required = True, help = "password field cannot be empty")
	parser.add_argument("address",   type = str, required = False )
	parser.add_argument("number", 	 type = str, required = True, help = "number field cannot be empty")
	parser.add_argument("birth",	 type = str, required = True, help = "birth field cannot be empty")
	parser.add_argument("age", 	     type = int, required = True, help = "Age field cannot be empty")
	parser.add_argument("gender", 	 type = str, required = True, help = "gender field cannot be empty")


	def post(self):
		data = UserRegister.parser.parse_args()
		print(data)
		validate = UserModel.validity_check(data["username"], data["number"])

		if "username" in validate or "number" in validate:
			return {"msg" : "invalid registration detail/s", "details" : validate}
		try:
			print("about to instantiate")
			user = UserModel(**data)
			print("about to change the date format")
			user.birth = datetime.strptime(data['birth'], '%Y-%m-%d').date()
			print("about to save")
			print(user)
			user.save_to_db()
			print("finish saving to db")
			return {"msg" : "User Successfully created"},200
		except Exception as e:
			print({"msg" : e.message, "traceback" : e.with_traceback()})
			return {"msg" : e.message, "traceback" : e.with_traceback()}, 500


class UserList(Resource):
	@jwt_required
	def get(self):
		users = UserModel.query_all()
		return {"users" : users},200

class Home(Resource):
	@jwt_required
	def get(self):
		_id = get_jwt_identity()
		print(_id)
		user = UserModel.find_by_id(_id)
		if user:
			return {"user" : user.json()},200
		return {"msg" : "user not found"},400


class UserLogin(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument("username", type=str, required=True, help="username cannot be empty")
	parser.add_argument("password", type=str, required=True, help="password cannot be empty")

	def post(self):
		data = UserLogin.parser.parse_args()
		user = UserModel.find_by_username(data["username"])
		if not user:
			return {"msg" : "username doesn't match any account"}, 401
		if safe_str_cmp(data["password"], user.password):
			access_token  = create_access_token(identity = user.id, fresh = True)
			refresh_token = create_refresh_token(user.id)

			return {
					"access_token" : access_token,
					"refresh_token": refresh_token,
					"username" : user.username,
					"firstname" : user.firstname
				   },201
		else:
			return {"msg" : "invalid credentials"}, 401


class TokenRefresh(Resource):

	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		if current_user:
			new_token = create_access_token(current_user, fresh = False)
			return { "access_token" : new_token},200

class UserLogout(Resource):

	@jwt_required
	def post(self):
		jti = get_raw_jwt()["jti"]
		print(jti)
		revoked_token = RevokedToken(jti = jti)
		revoked_token.add()
		return {"msg" : "Access token revoked"}, 200


class UserProfile(Resource):

	@jwt_required
	def get(self):
		_id = get_jwt_identity()
		user = UserModel.find_by_id(_id)
		if user:
			return {"user" : user.json(), "posts" : user.get_posts(), "photos" : user.get_photos()},200
		return {"msg" : "user not found"},400

class Profile(Resource):

	@jwt_required
	def get(self, username):
		user = UserModel.find_by_username(username)
		if user:
			return {"user" : user.json(), "posts" : user.get_posts(), "photos" : user.get_photos()},200
		return {"msg" : "user not found"},400
