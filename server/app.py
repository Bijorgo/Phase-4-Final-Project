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

# GET/songs: Get all songs

@app.get("/songs")
def get_songs():
    songs = Song.query.all()
    if not songs:
        return jsonify({"error": "no songs found."}), 404
    song_list = [{"id": song.id, "title": song.title, "artist": song.artist, "genre": song.genre} for song in songs]

    return jsonify({"songs": song_list}), 200


    

    


