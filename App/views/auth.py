from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, make_response #send_from_directory, 
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, create_access_token
from App.controllers.user import * # type: ignore
from flask import Response as FlaskResponse


from.index import * # type: ignore

from App.controllers import (
    login,
    create_user
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')



'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users() # type: ignore
    if not users:
        flash('No users found')
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")

'''
@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])

    if not token:
        flash('Bad username or password given'), 401
    else:
        flash('Login Successful')
        response = redirect(request.referrer)
        set_access_cookies(response, token) 
    return response
'''

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])

    if not token:
        flash('Bad username or password given')
        return redirect(request.referrer), 401

    response = make_response(redirect(url_for('index_views.home')))
    flash('Login Successful')
    set_access_cookies(response, token) # type: ignore
    return response

@auth_views.route('/register', methods=['POST'])
def register_action():
    data = request.form
    create_user(data['username'], data['password'])
    flash('User Registered')
    return render_template('index.html')


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = render_template('index.html')
    flash("Logged Out!")
    unset_jwt_cookies(response) # type: ignore
    return response

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    if not data:
        return jsonify(message="Please provide user details"), 400

    token = login(data['username'], data['password'])
    if not token:
        return jsonify(message='bad username or password given'), 401
    response = jsonify(access_token=token) 
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response