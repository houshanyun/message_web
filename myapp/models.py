from werkzeug.security import generate_password_hash, check_password_hash
from myapp import db
from datetime import datetime
from flask_login import UserMixin

class Nickname(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    article = db.relationship('Article', backref='nick', lazy='dynamic')
    n_comment = db.relationship('Comment', backref='n_com', lazy='dynamic')
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
    a_comment = db.relationship('Comment', backref='a_com', lazy='dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    com_txt = db.Column(db.Text(100))
    com_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    com_nick_id = db.Column(db.Integer, db.ForeignKey('nickname.id'))
    com_article_id = db.Column(db.Integer, db.ForeignKey('article.id'))



