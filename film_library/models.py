from views import db
from flask_login import UserMixin


class CustomUser(db.Model, UserMixin):
    __tablename__ = 'customusers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    films = db.relationship('Film', backref='customusers')


    def __repr__(self):
        return f"CustomUser(id={self.id}, username={self.username})"


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release = db.Column(db.Date)
    description = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(255), default='default.png')
    user_id = db.Column(db.Integer, db.ForeignKey('customusers.id'), nullable=False)
    director_id = db.Column(db.String(), db.ForeignKey('directors.id', ondelete='SET DEFAULT'), nullable=False, server_default='unknown')

    def __repr__(self):
        return f"Film(id={self.id}, name={self.name})"


class Director(db.Model):
    __tablename__ = 'directors'

    id = db.Column(db.String(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    films = db.relationship('Film', backref='directors')

    def __repr__(self):
        return f"Director(id={self.id}, first_name={self.first_name})"
