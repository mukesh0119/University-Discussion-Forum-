# application/user_api/routes.py
from . import user_api_blueprint
from .. import db, login_manager
from ..models import User
from flask import make_response, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from passlib.hash import sha256_crypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None

@user_api_blueprint.route('/api/<int:user_id>/username', methods=['GET'])
def get_username(user_id):

    user = User.query.get_or_404(user_id)
    if user:
        user_response = user.to_json()
        user_name = user_response['first_name'] + ' ' + user_response['last_name']
        response = jsonify(user_name)
    else:
        response = jsonify({'message': 'Cannot find user/username'}), 404
    return response


@login_required
@user_api_blueprint.route('/api/user', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        return make_response(jsonify({'result': current_user.to_json()}))

    return make_response(jsonify({'message': 'Not logged in'})), 401


@user_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())

    response = jsonify(data)
    return response

@user_api_blueprint.route('/api/user/create', methods=['POST'])
def post_register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    uni_number = request.form['uni_number']
    user_role = request.form['user_role']
    image_url = request.form['image_url']

    password = sha256_crypt.hash((str(request.form['password'])))

    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.uni_number = uni_number
    user.phone_number = phone_number
    user.user_role = user_role
    user.image_url = image_url
    user.authenticated = True

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User added', 'result': user.to_json()})

    return response

@user_api_blueprint.route('/api/user/update', methods=['POST'])
def post_update():

    id = request.form['user_id']
    user = User.query.filter_by(id=id).first()

    image_url = request.form['image_url']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']

    if len(request.form) > 5:
        if request.form['user_role'] != '':
            user_role = request.form['user_role']
            user.user_role = user_role

    if image_url != 'defaultpp.png':
        user.image_url = image_url

    if first_name != '':
        user.first_name = first_name

    if last_name != '':
        user.last_name = last_name

    if phone_number != '':
        user.phone_number = phone_number

    db.session.commit()

    response = jsonify({'message': 'User updated', 'result': user.to_json()})

    return response

@user_api_blueprint.route('/api/user/login', methods=['POST'])
def post_login():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        if sha256_crypt.verify(str(request.form['password']), user.password):
            user.encode_api_key()
            db.session.commit()
            login_user(user)

            return make_response(jsonify({'message': 'Logged in', 'api_key': user.api_key}))

    return make_response(jsonify({'message': 'Not logged in'}), 401)

@user_api_blueprint.route('/api/user/logout', methods=['POST'])
def post_logout():
    if current_user.is_authenticated:
        current_user.api_key = None
        db.session.commit()
        logout_user()
        return make_response(jsonify({'message': 'You are logged out'}))
    return make_response(jsonify({'message': 'You are not logged in'}))

@user_api_blueprint.route('/api/user/<email>/exists', methods=['GET'])
def get_email(email):
    item = User.query.filter_by(email=email).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'message': 'Cannot find email'}), 404
    return response

@user_api_blueprint.route('/api/user/uni_number/<uni_number>/exists', methods=['GET'])
def get_urn(uni_number):
    item = User.query.filter_by(uni_number=uni_number).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'message': 'Cannot find uni_number'}), 404
    return response

@user_api_blueprint.route('/api/user/phone_number/<phone_number>/exists', methods=['GET'])
def get_phone(phone_number):
    item = User.query.filter_by(phone_number=phone_number).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'message': 'Cannot find phone_number'}), 404
    return response

@user_api_blueprint.route('/api/user/<id>', methods=['GET'])
def get_otheruser(id):
    response = []

    user = User.query.filter_by(id=id).first()
    if user is None:
        response = jsonify({'message': 'Cannot find user'}), 404
        return response

    response = jsonify(user.to_json())

    return response