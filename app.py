from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session 
import os
import bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)
CORS(app)
Session(app)

class User(db.Model):
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
    user = User(name=data.name, username=data.username, password=hash)
    db.add(user)
    db.commit()
    return jsonify({"Success": "Registered user"}), 200

@app.route('/api/login/', methods=['POST'])
def login():
    data = request.json()
    if not all(i in data for i in ['username', 'password']):
        return jsonify({'error': 'Missing required fields'}), 200
    user = db.query(User).fitler(username=data.username)
    if not user:
        return jsonify({'error': 'No such user found'}), 404
    if bcrypt.checkpw(user.password):
        session['username'] = user.username
        return jsonify({'success': 'logged in'}), 200
    else:
        return jsonify({'fail': 'Incorrect password'}), 403
