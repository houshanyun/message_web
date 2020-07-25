from werkzeug.security import generate_password_hash, check_password_hash
from myapp import db
from datetime import datetime
from flask_login import UserMixin

class Nickname(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    article = db.relationship('Article', backref='nick', lazy='dynamic')
    admin = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    txt = db.Column(db.Text(140))
    nowtime = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    nick_id = db.Column(db.Integer, db.ForeignKey('nickname.id'))

