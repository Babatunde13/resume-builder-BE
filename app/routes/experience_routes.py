'''Module that handles view of everything that has to do with work experience of the  user'''
from app import app
from app.models import WorkExperience
import flask
from app.routes import token_required

@app.route('/experience')
@token_required
def get_experience(current_user):
    return flask.jsonify(
        WorkExperience().get_user_experiences(current_user['_id'])
    )

@app.route('/experience', methods=['POST'])
@token_required
def create_experience(current_user):
    payload = flask.request.get_json()
    if 'course' not in payload or 'school' not in payload or\
             'start_date' not in payload:
        return flask.jsonify({
            'error': 'Bad request',
            'message': 'Invalid data'
        }), 400
    data = {
        'course': payload['course'], 'school': payload['school'],
        'start_date': payload['start_date'],
        'user_id': current_user['_id']
    }
    if 'end_date' in payload:
        data['end_date'] = payload['end_date']
    if 'description' in payload:
        data['desc'] = payload['description']
    data['user_id'] = current_user['_id']
    w=WorkExperience().create_work(**data)
    return flask.jsonify(w), 200

@app.route('/experience/<id>', methods=['DELETE'])
@token_required
def delete_experience(current_user, id):
    WorkExperience().delete_work(id)
    return '', 204

@app.route('/experience/<id>', methods=['PUT'])
@token_required
def edit_experience(current_user, id):
    if 'title' not in payload or 'company' not in payload:
        return flask.jsonify({
            'error': 'Bad request'
        }), 400
    return flask.jsonify(WorkExperience().edit_work(id, payload))