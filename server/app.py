from flask import Flask, request, jsonify, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if 'user_id' in session:
        return f'Hello, {session["username"]}! <a href="/logout">Logout</a>'
    return 'Welcome! <a href="/login">Login</a> or <a href="/signup">Signup</a>'

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return jsonify({'message': 'You are already signed in'}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'username': user.username}})

@app.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' not in session:
        return jsonify({'message': 'You are not signed in'}), 401

    session.clear()
    return jsonify({'message': 'Logout successful'})

@app.route('/protected-resource')
def protected_resource():
    if 'user_id' not in session:
        return jsonify({'message': 'You are not signed in'}), 401

    # Authorization logic for the protected resource
    # Add your authorization code here
    authorized_user = User.query.get(session['user_id'])

    if not authorized_user:
        return jsonify({'message': 'User not found'}), 401

    return jsonify({'message': 'This is a protected resource', 'user': {'id': authorized_user.id, 'username': authorized_user.username}})

if __name__ == '__main__':
    app.run(debug=True)
