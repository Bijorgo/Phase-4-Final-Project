from flask import Flask, request, jsonify
from server.config import app, db
from sqlalchemy.exc import IntegrityError
from server.models import User, Song

# POST /register: Register a new user. (Tested using PostMan - 200)

@app.post("/register")
def register_user():
    new_user = request.json

    if not new_user["username"] or not new_user["password"]:
        return jsonify({"error": "Username and password are required fields."}), 400
    try:
        db.session.add(User(username=new_user["username"], password=new_user["password"]))
        db.session.commit()
        return jsonify({"message:": "User created!"}), 201
    except IntegrityError:
        return jsonify({"error": "Username already exists, please try another one."})
    except Exception as exception:
        return jsonify({"error": str(exception)})

# POST /login: Log in. (Created test user in DB and tested via Postman, 200 OK)

@app.post("/login")
def user_login():
    user_entry = request.json
    username = user_entry["username"]
    password = user_entry["password"]
    if not username or not password:
        return jsonify({"error": "Username and password are required for login."})
    user=User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"error": "Inavalid username or password."}), 401
    return jsonify({"message": "You have successfully logged in!"}), 200

# GET /users/:id : Retrieve a specific user's information. (Tested via Postman, 200 OK)
@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found."})
    return jsonify(user.to_dict()), 200

# GET/songs: Get all songs (Tested via postman, 200 OK)

@app.get("/songs")
def get_songs():
    songs = Song.query.all()
    if not songs:
        return jsonify({"error": "no songs found."}), 404
    song_list = [{"id": song.id, "name": song.name, "artist": song.artist, "album": song.album} for song in songs]

    return jsonify({"songs": song_list}), 200

#POST/songs: Create a new song (tested via postman, 200 ok)

@app.post("/songs")
def create_new_song():
    new_song = request.json
    if not new_song["name"] or not new_song["artist"]:
        return jsonify({"error": "Name and artist fields are required"}), 400
    try:
        song = Song(name=new_song["name"], artist=new_song["artist"], album=new_song.get("album"), duration=new_song.get("duration"))
        db.session.add(song)
        db.session.commit()
        return jsonify(song.to_dict())
    except Exception as exception:
        return jsonify({"error": str(exception)}), 500
    
#PATCH/songs/id: Update a song (tested in Postman, 200 OK)

@app.patch("/songs/<int:song_id>")
def update_song(song_id):
    updated_song = request.json
    song = Song.query.filter_by(id=song_id).first()
    if not song:
        return jsonify({"error": "Song not found in database."}), 404
    
    if "name" in updated_song:
        song.name = updated_song["name"]
    if "artist" in updated_song:
        song.artist = updated_song["artist"]
    if "album" in updated_song:
        song.album = updated_song["album"]
    if "duration" in updated_song:
        song.duration = updated_song["duration"]

    try:
        db.session.commit()
        return jsonify(song.to_dict())
    except Exception as exception:
        return jsonify({"error": str(exception)}), 500


#DELETE/songs.id: Delete a song (Tested via Postman, 200 OK)

@app.delete("/songs/<int:song_id>")
def delete_song(song_id):
    song = Song.query.filter_by(id=song_id).first()
    if not song:
        return jsonify({"error": "Song with that ID not found."}), 404
    try:
        db.session.delete(song)
        db.session.commit()
        return jsonify({"message": "Song deleted successfully!"})
    except Exception as exception:
        return jsonify({"error": str(exception)}), 500


    

    


