from functools import wraps

from bson import ObjectId
from flask import Flask, jsonify, request, session, make_response
from flask_pymongo import PyMongo
from datetime import timedelta, datetime
import secrets, jwt

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dashboard_incendios_forestales'
app.config['SECRET_KEY'] = secrets.token_urlsafe(64)
mongo = PyMongo(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
            session['user_id'] = payload['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 403

    return decorated


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    users = mongo.db.users
    user = users.find_one({'username': data.get('username')})
    if user['username'] == data.get('username') and user['password'] == data.get('password'):
        session['logged_in'] = True
        token = jwt.encode({
            'user_id': str(user['_id']),
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Authentication Failure!"'})


@app.route('/admin_only', Methods=['GET'])
@token_required
def admin_only():
    users = mongo.db.users
    user = users.find_one({'_id': ObjectId(session['user_id'])})
    if user and user['role'] == 'admin':
        return jsonify({'message': 'Hello admin'}), 200
    else:
        return jsonify({'message': 'You are not an admin'}), 401


if __name__ == '__main__':
    app.run(port=5001)
