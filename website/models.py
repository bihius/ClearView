from extensions import db

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    photos = db.relationship('Photo', backref='album', lazy=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
