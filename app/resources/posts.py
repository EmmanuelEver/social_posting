from flask_restful import Resource, reqparse
from models.post import PostModel
from models.user import UserModel
from flask_jwt_extended import (
								get_jwt_identity, 
								jwt_required, 
								jwt_refresh_token_required,
								get_raw_jwt
								)
from datetime import datetime

class Post(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("title", type=str, required=True, help="You must put a title for the post")
	parser.add_argument("caption", type=str, required=False)
	parser.add_argument("filepath", type=str, required=False)

	@jwt_required
	def post(self):
		_id = get_jwt_identity()
		user = UserModel.find_by_id(_id)
		data = Post.parser.parse_args()
		data["date_created"] = datetime.date(datetime.now())
		try:
			post = PostModel(**data)
			post.save_to_db()
			user.add_post(post)
			return {"msg" : "Post added"}, 200
		except:
			return {"msg" : "error adding new post"}, 500

	@jwt_required
	def get(self, post_id):
		post = PostModel.find_by_id(post_id)
		return {"posts" : post.json()},200

	@jwt_required
	def delete(self, post_id):
		post = PostModel.find_by_id(post_id)
		post.delete_to_db()
		return {"msg" : "Post deleted"}, 200


class PostList(Resource):

	@jwt_required
	def get(self):
		_id = get_jwt_identity()
		user = UserModel.find_by_id(_id)
		posts = user.get_post()
		return {"posts" : posts},200