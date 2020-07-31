from flask import Flask, make_response
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.users import UserRegister, UserList, UserLogin, TokenRefresh, UserLogout, Home, UserProfile, Profile
from resources.posts import Post, PostList
from resources.photos import Photo, Add_Dp, Set_Dp
from models.user import RevokedToken
import os

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
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
@app.route('/favicon.ico')
def favicon():
    return
           

api.add_resource(UserRegister,"/register")
api.add_resource(UserList, "/users")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Post, "/user/post/<int:post_id>", endpoint="post_id")
api.add_resource(Post, "/user/post")
api.add_resource(PostList, "/posts")
api.add_resource(Home, "/")
api.add_resource(UserProfile, "/profile")
api.add_resource(Profile, "/<string:username>")
api.add_resource(Photo, "/photo/<int:photo_id>", endpoint="photo_id")
api.add_resource(Photo, "/photo")
api.add_resource(Add_Dp, "/add_dp")
api.add_resource(Set_Dp, "/set_dp/<int:photo_id>")

if "__main__" == __name__:
	from db import db
	db.init_app(app)
	app.run(debug=True)