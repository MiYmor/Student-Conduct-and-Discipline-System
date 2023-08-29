# api/api_routes.py
from flask import Blueprint, jsonify, request, redirect, url_for, flash, session
from models import  Student

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import  login_user
from flask_cors import CORS 

import os

# Access API keys from environment variables
WEBSITE1_API_KEY = os.getenv('WEBSITE1_API_KEY')
WEBSITE2_API_KEY = os.getenv('WEBSITE2_API_KEY')
WEBSITE3_API_KEY = os.getenv('WEBSITE3_API_KEY')
WEBSITE4_API_KEY = os.getenv('WEBSITE4_API_KEY')
WEBSITE5_API_KEY = os.getenv('WEBSITE5_API_KEY')

API_KEYS = {
    'website1': WEBSITE1_API_KEY,
    'website2': WEBSITE2_API_KEY,
    'website3': WEBSITE3_API_KEY,
    'website4': WEBSITE4_API_KEY,
    'website5': WEBSITE5_API_KEY,
    # Add more websites and keys as needed
}

student_api = Blueprint('student_api', __name__)
CORS(student_api)  # Apply CORS to the student_api blueprint

# Api/v1/student/api_routes.py

@student_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        student = Student.query.filter_by(email=email).first()
        if student and check_password_hash(student.password, password):
            # Successfully authenticated
            access_token = create_access_token(identity=student.id)
            session['access_token'] = access_token
            session['user_role'] = 'student'
            return redirect(url_for('student_home'))
        else:
            flash('Invalid email or password', 'danger')
    return redirect(url_for('student_login'))



#===================================================
# TESTING AREA
@student_api.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    print("CURRENT USER ID: ", current_user_id)
    # Debug print statement
    student = Student.query.get(current_user_id)
    if student:
        return jsonify(student.to_dict())
    else:
        flash('User not found', 'danger')
        return redirect(url_for('student_api.login'))
    
    
@student_api.route('/all/student', methods=['GET'])
def allstudent():
    api_key = request.headers.get('X-Api-Key')  # Get the API key from the request header

    if api_key in API_KEYS.values():
        return jsonify(message="You got API data")
    else:
        return jsonify(message="Invalid key you cant have an access")
