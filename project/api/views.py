from flask import Blueprint, jsonify, request,render_template
from sqlalchemy import exc

from project.api.models import User
from project import db


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
group_blueprint = Blueprint('group')

@users_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

@group_blueprint.route('/group', methods=['POST'])
def create_group():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    group_name = post_data.get('groupname')
    location = post_data.get('location')
    radius = post_data.get('radius')
    price = post_data.get('price')
    openat = post_data.get('openat')
    categories = post_data.get('categories')
    try:
        newgroup = Group(groupname=group_name, location=location, radius=radius, price=price, openat=openat, categories=categories)
        db.session.add(newgroup)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{group_name} was created!',
            'url': newgroup.id,
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

@group_blueprint.route('/group/<groupid>', methods=['GET'])
def join_group(groupid):
    if not groupid:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    try:
        group = Group.query.filter_by(id=groupid).first()
        if group:
            group.member_number += 1
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{groupid} was found!',
                'groupname': group.groupname,
                'userid': group.member_number,
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. The group doesn\'t exist.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
