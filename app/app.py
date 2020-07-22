from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.users import UserRegister, UserList, UserLogin, TokenRefresh, UserLogout, Home
from resources.posts import Post
from models.user import RevokedToken

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "aasdasdj9882unsad"

app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_SECRET_KEY"] = "aasdasdj9882unsad"
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	jti = decrypted_token["jti"]
	return RevokedToken.query_jti(jti)

@jwt.expired_token_loader
def expired_token_callback(expired_token):
	return {
		"msg" : f"Your {expired_token} token has expired",
		"status" : 401
	}

@jwt.invalid_token_loader
def invalid_token_callback(invalid_token):
	return {
		"msg" : f"Your {invalid_token} token is invalid",
		"status" : 401
	}

@jwt.revoked_token_loader
def revoked_token_callback(revoked_token):
	return {
		"msg" : f"Your {revoked_token} token is revoked",
		"status" : 401
	}

@jwt.unauthorized_loader
def unauthorized_callback(error):
	return {
		"msg" : f"{error} Unauthorized user",
		"status" : 401
	}

api.add_resource(UserRegister,"/register")
api.add_resource(UserList, "/users")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Post, "/user/post/<int:post_id>", endpoint="post_id")
api.add_resource(Post, "/user/post")
api.add_resource(Home, "/")

if "__main__" == __name__:
	from db import db
	db.init_app(app)
	app.run(debug=True)