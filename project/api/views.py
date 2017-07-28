from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import User
from project.api.models import Group
from project.api.models import GroupDetails
from project.api.models import VotingSession
from project import db


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
group_blueprint = Blueprint('group', __name__, template_folder='./templates')
votingsession_blueprint = Blueprint('votingsession', __name__, template_folder='./templates')

@users_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
    })

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
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
                'message': '{email} was added!',
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.',
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400

@group_blueprint.route('/group', methods=['POST'])
def create_group():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400
    group_name = post_data.get('groupname')
    location = post_data.get('location')
    radius = post_data.get('radius')
    price = post_data.get('price')
    openat = post_data.get('openat')
    categories = post_data.get('categories')
    try:
        newgroup = Group(group_name=group_name)
        db.session.add(newgroup)
        db.session.flush()

        groupinfo = GroupDetails(group_id=newgroup.group_id, latitude=location.get('latitude'), longitude=location.get('longitude'), radius=radius, price=price, open_at=openat, categories=categories)
        db.session.add(groupinfo)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': '{group_name} was created!'.format(group_name=group_name),
            'url': newgroup.group_id,
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400

@group_blueprint.route('/group/<group_id>', methods=['GET'])
def join_group(group_id):
    if not group_id:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400
    try:
        group = Group.query.filter_by(group_id=group_id).first()
        if group:
            group.member_count += 1
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': '{group_id} was found!'.format(group_id=group_id),
                'groupname': group.group_name,
                'userid': group.member_count,
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
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400

@votingsession_blueprint.route('/group/<group_id>/votingsession', methods=['POST'])
def start_voting(group_id):
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400
    try:
        voting_session = VotingSession(
                group_id=group_id,
                voting_status="InProgress",
            )
        db.session.add(voting_session)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': '{group_name}'s voting session' was created!'.format(group_name=group_name),
            'voting_session_id': voting_session.voting_session_id,
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400

@votingsession_blueprint.route('/group/<group_id>/votingsession/<voting_session_id>', methods=['PUT'])
def end_voting(group_id, voting_session_id):
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400
    try:
        votingsession = VotingSession.query.filter_by(voting_session_id=voting_session_id).first()
        if votingsession:
            votingsession.voting_status = "Done"
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': '{voting_session_id} marked as Done!'.format(voting_session_id=voting_session_id),
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. The votingsession doesn\'t exist.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400
