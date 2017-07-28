from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import User
from project.api.models import Group
from project.api.models import GroupDetails
from project.api.models import VotingSession
from project import db
import operator
import json

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

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

        groupinfo = GroupDetails(
            group_id=newgroup.group_id,
            latitude=location.get('latitude'),
            longitude=location.get('longitude'),
            radius=radius,
            price=price,
            open_at=openat,
            categories=categories
        )
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

@votingsession_blueprint.route('/group/<group_id>/votingsession/<voting_session_id>', methods=['GET'])
def get_voting_status(group_id, voting_session_id):
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
            response_object = {
                'status': 'success',
                'message': 'Voting Session {voting_session_id} found!'.format(voting_session_id=voting_session_id),
                'voting_status': votingsession.voting_status,
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
                'message': 'Voting Session {voting_session_id} marked as Done!'.format(voting_session_id=voting_session_id),
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

@group_blueprint.route('/group/<groupid>/user/<userid>/vote', methods=['POST'])
def add_vote(groupid, userid):
    biz_id = request.args.get('biz_id')     # we need to add biz_id on the request

    # Create a dictionary of dictionary
    # for all group votes
    # in the following style
    # { '123':
    #   { 'blue-bottle-coffee': 1 }
    #   { 'japa-curry': 1 }
    #   { 'mcdonalnds': 5 }
    # }
    # where, key = group id, value = dict of biz id and # votes

    # NOTE: Ideally we want to store businesses in the cache too
    # by the business id and flush the cache after the vote is over.

    try:
        group_votes = cache.get(groupid) # outer dict
        if group_votes is None:
            group_votes = {}
            group_votes[groupid] = {} # inner dict
            group_votes[groupid][biz_id] = 1    # add biz to dict with vote count 1
        else:
            biz_votes = group_votes.get(groupid)
            biz_vote_cnt = biz_votes.get(biz_id)   # get total # of votes for a particular biz
            if biz_vote_cnt is None:
                group_votes[groupid][biz_id] = 1
            else:
                group_votes[groupid][biz_id] = biz_vote_cnt + 1

        # update cache
        cache.set(groupid, group_votes, timeout=5 * 60)

        response_object = {
            'status': 'success'
        }
        return jsonify(response_object), 200
    except exc.IntegrityError as e:
        response_object = {
            'status': 'fail',
            'message': 'There was an error registering vote.',
        }
        return jsonify(response_object), 500

@group_blueprint.route('/group/<groupid>/vote', methods=['GET'])
def get_votes(groupid):
    # Retrieve all votes from cache and return
    # sorted by value

    try:
        group_votes = cache.get(groupid)
        if group_votes is None:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. The group doesn\'t exist.'
            }
            return jsonify(response_object), 400

         # this gives a sorted tuple
        sorted_group_votes = sorted(group_votes.items(), key=operator.itemgetter(1), reverse=True)

        response_object = {
            'status': 'success',
            'votes': json.dumps(sorted_group_votes) # hopefully parsing this wont be too bad
        }
        return jsonify(response_object), 200
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400

