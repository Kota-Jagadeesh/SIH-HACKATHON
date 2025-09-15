from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)
CORS(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(511), password=True)

@app.route('/api/register/', methods=["POST"])
def register():
    data = request.json()
    if not all(i in data for i in ['name', 'username', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    password = data.password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hash = bcrypt.hashpw(password_bytes, salt)
    user = user(name=data.name, username=data.username, password=hash)
    db.add(user)
    db.commit()
    return jsonify({"Success": "Registered user"}), 200
