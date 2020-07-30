from db import db
from models.post import PostModel
from models.photo import PhotoModel

class UserModel(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(20), nullable = False)
	lastname = db.Column(db.String(20), nullable = False)
	username = db.Column(db.String(20), unique = True, nullable = False)
	password = db.Column(db.String(20), nullable = False)
	address = db.Column(db.String(20), nullable = True)
	number = db.Column(db.String(20), unique = True, nullable = False,)
	birth = db.Column(db.Date, nullable = False)
	age = db.Column(db.Integer, nullable = False)
	gender = db.Column(db.String(1), nullable = False)
	posts = db.relationship("PostModel", backref = "author", lazy = "dynamic")
	photos = db.relationship("PhotoModel", backref = "user", lazy = "dynamic")
	dp_path = db.Column(db.String, nullable = True)


	def __init__(self, firstname, lastname, username, password, address, number, birth, age, gender):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.password = password
		self.address = address
		self.number = number
		self.birth = birth
		self.age = age
		self.gender = gender

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_to_db(self):
		db.session.delete(self)
		db.session.commit()

	def add_post(self, post):
		self.posts.append(post)
		db.session.commit()

	def add_photo(self, photo):
		self.photos.append(photo)
		db.session.commit()

	def set_dp(self, dp_path):
		self.dp_path = dp_path
		db.session.commit()
		return {"filepath" : self.dp_path}

	def get_posts(self):
		posts = [ post.json() for post in self.posts ]
		return posts

	def get_photos(self):
		photos = [ photo.json() for photo in self.photos ]
		return photos

	def json(self):
		return {
				"username" : self.username,
				"firstname" : self.firstname,
			    "lastname" : self.lastname,
			    "address"  : self.address,
			    "age" 	   : self.age,
			    "gender"   : self.gender,
			    "dp" 	   : self.dp_path
			   }

	@classmethod
	def validity_check(cls, username, number):
		validity = dict()
		user = cls.query.filter_by(username = username).first()
		number = cls.query.filter_by(number = number).first()
		if user:
			validity["username"] = "username already existed"
		if number:
			validity["number"] = "number already existed"
			
		return validity

	@classmethod	
	def find_by_username(cls, username):
		user = cls.query.filter_by(username = username).first()
		return user

	@classmethod
	def find_by_id(cls, id):
		user = cls.query.filter_by(id = id).first()
		return user

	@classmethod
	def query_all(cls):
		users = [user.json() for user in UserModel.query.all()]
		return users

class RevokedToken(db.Model):

	__tablename__ = "revoked_tokens"

	id = db.Column(db.Integer, primary_key = True)
	jti = db.Column(db.String(200))


	def add(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def query_jti(cls, jti):
		jtis = cls.query.filter_by(jti = jti).first()
		return bool(jtis)