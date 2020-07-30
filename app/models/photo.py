from db import db

class PhotoModel(db.Model):
	__allowed_ext__ = ["JPG", "JPEG", "PNG"]

	__tablename__ = "photos"
	id = db.Column(db.Integer, primary_key = True)
	filepath = db.Column(db.String, nullable = False)
	caption = db.Column(db.String, nullable = True)
	date_created = db.Column(db.Date, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


	def __init__(self, filepath, caption, date_created):
			self.filepath = filepath
			self.caption = caption
			self.date_created = date_created

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	def json(self):
		return {
				"id" : self.id,
				"filepath" : self.filepath,
				"caption" : self.caption,
				"date_created" : str(self.date_created)
				}

	@classmethod
	def validate(cls, ext):
		if ext in cls.__allowed_ext__:
			return True
		else:
			return False		

	@classmethod
	def find_by_id(cls, id):
		photo = cls.query.filter_by(id = id).first()
		return photo
		
	@classmethod
	def find_by_path(cls, path):
		photo = cls.query.filter_by(path = path)
		return photo

		