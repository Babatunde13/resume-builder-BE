'''Module that handles view of everything that has to do with skill of the  user'''
from app import app
import flask
from app.routes import token_required
from app.models import Skill

@app.route('/skills')
@token_required
def get_skills(current_user):
    return flask.jsonify(
        Skill().get_user_skills(current_user['_id'])
    )

@app.route('/skills/<id>')
@token_required
def get_skill(current_user, id):
    return flask.jsonify(
        Skill().get_skill(id)
    )

@app.route('/skills', methods=['POST'])
@token_required
def create_skill(current_user):
    payload = flask.request.get_json()
    if 'name' not in payload or 'level' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid email or password'
        }), 400
    payload = {
        'name': payload['name'], 'level': payload['level'],
        'user_id': current_user['_id']
    }
    if Skill().db.find_one({'user_id': current_user['_id'], 'name': payload['name']}):
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Skill already exist for the user'
        }), 400
    s=Skill().create_skill(**payload)
    return s, 201

@app.route('/skills/<id>', methods=['DELETE'])
@token_required
def delete_skill(current_user, id):
    if not Skill().db.find_one({'_id': id}):
        return {
            'error': 'Bad request',
            'message': 'No skill with that id'
        }, 404
    Skill().delete_skill(id)
    return '', 204

@app.route('/skills/<id>', methods=['PUT'])
@token_required
def edit_skill(current_user, id):
    payload = flask.request.get_json()
    if 'name' not in payload or 'level' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'name or level not defined'
        }), 400
    h = Skill().db.find_one({
        'user_id': current_user['_id'], 'name': payload['name']
        }) if 'name' in payload else None
    if h:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'that skill already exist for the user'
        }), 400
    s=Skill().edit_skill(id, payload)
    return s, 201