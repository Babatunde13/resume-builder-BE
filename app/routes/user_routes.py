'''Module that handles view of everything that has to do with CRUD of the user'''
from app import app
from app.models import *
import flask
from app.routes import token_required
from app.routes.image_saver import save_pic

@app.route('/user')
@token_required
def get_user(current_user):
    user = User().get_user(current_user['_id'])
    user['skills'] = Skill().get_user_skills(current_user['_id'])
    user['education'] = Education().get_user_educations(current_user['_id'])
    user['languages'] = Language().get_user_skills(current_user['_id'])
    user['experiences'] = WorkExperience().get_user_experiences(current_user['_id'])
    user['achievements'] = Achievement().get_user_achievements(current_user['_id'])
    user['certificates'] = Certificate().get_user_certificates(current_user['_id'])
    return flask.jsonify(user)

@app.route('/user', methods=['PUT'])
@token_required
def update_user(current_user):
    data = dict(flask.request.form)
    avatar_name = save_pic(flask.request.files['avatar'])
    if type(avatar_name) == dict and 'error' in avatar_name:
        return {
            'error': 'Bad request',
            'message': avatar_name['message']
        }, 400
    data['image_path'] = flask.request.host_url+'static/'+avatar_name
    return {
        **data
        }, 201

@app.route('/users')
def users():
    return User().get_users()

def confirm_account():
    pass