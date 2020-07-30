from db import db

class PostModel(db.Model):
	__tablename__ = "posts"

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(200), nullable = False)
	caption = db.Column(db.String(1000), nullable = True)
	filepath = db.Column(db.String(50), nullable = True)
	date_created = db.Column(db.Date, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

	def __init__(self, title, caption, filepath, date_created):
		self.title = title
		self.caption = caption
		self.filepath = filepath
		self.date_created = date_created

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_to_db(self):
		db.session.delete(self)
		db.session.commit()

	def json(self):
		return {
		"post_id" : self.id, 
		"post_title" : self.title, 
		"post_caption" : self.caption, 
		"post_filepath" : self.filepath, 
		"post_date_created" : str(self.date_created)
		}

	@classmethod
	def query_by_author(cls, author):
		posts = [post.json() for post in cls.query.filter_by(author = author).all()]
		return {"posts" : posts}

	@classmethod
	def find_by_id(cls, id):
		post = cls.query.filter_by(id = id).first()
		return post