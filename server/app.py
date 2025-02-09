from Flask import Flask, request, jsonify
from config import app, db, IntegrityError
from models import User, Mixtape, Song, MixtapeItem

# POST /register: Register a new user.

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
    

    


