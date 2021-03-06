'''Module that handles view of everything that has to do with education of the  user'''
from app import app
from app.models import Education
import flask
from app.routes import token_required

@app.route('/education')
@token_required
def get_educations(current_user):
    return flask.jsonify(
        Education().get_user_educations(current_user['_id'])
    )

@app.route('/education/<id>')
@token_required
def get_education(current_user, id):
    return flask.jsonify(
        Education().get_education(id)
    )

@app.route('/education', methods=['POST'])
@token_required
def create_education(current_user):
    payload = flask.request.get_json()
    if 'title' not in payload or 'company' not in payload or\
             'start_date' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid data'
        }), 400
    data = {
        'title': payload['title'], 'company': payload['company'],
        'start_date': payload['start_date'],
        'user_id': current_user['_id']
    }
    if 'end_date' in payload:
        data['end_date'] = payload['end_date']
    if 'description' in payload:
        data['desc'] = payload['description']
    data['user_id'] = current_user['_id']
    if Education().db.find_one(data):
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Language already exist for the user'
        }), 400
    e=Education().create_education(**data)
    return e, 201

@app.route('/education/<id>', methods=['DELETE'])
@token_required
def delete_education(current_user, id):
    if not Education().db.find_one({'_id': id}):
        return {
            'error': 'Bad request',
            'message': 'No education with that id'
        }, 404
    Education().delete_education(id)
    return '', 204

@app.route('/education/<id>', methods=['PUT'])
@token_required
def edit_education(current_user, id):
    payload = flask.request.get_json()
    if 'course' not in payload or 'school' not in payload:
        return flask.jsonify({
            'error': 'Bad request'
        }), 400
    e=Education().edit_education(id, payload)
    return e, 201