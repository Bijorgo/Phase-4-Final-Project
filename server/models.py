from server.config import db

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username}

class Song(db.Model):
    __tablename__="songs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    album = db.Column(db.String)
    duration = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "artist": self.artist, "album": self.album, "duration": self.duration}