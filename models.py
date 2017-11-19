from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class Memo(db.EmbeddedDocument):
    tag = db.StringField(max_length=20)
    body = db.StringField(max_length=150)

class Post(db.Document):
    title = db.StringField(max_length=100, required=True)
    content = db.StringField(max_length=200, required=True)
    memo = db.EmbeddedDocumentField(Memo)
    created_at = db.DateTimeField(default=datetime.datetime.now)

