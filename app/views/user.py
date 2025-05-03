from flask import request, jsonify
from app.models.user import User
from app.extensions import db

from flask_login import login_user, logout_user, login_required, current_user

from app.utils.common import send_json_response
from app.utils.constants import HttpStatusCode


def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password:
        return send_json_response(response_status=False, message_key="Email and password are required",
                                  http_status=HttpStatusCode.BAD_REQUEST.value)

    if User.query.filter_by(email=email).first():
        return send_json_response(response_status=False, message_key="User already exists",
                                  http_status=HttpStatusCode.BAD_REQUEST.value)

    user = User(email=email, name=name)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return send_json_response(response_status=True, message_key="User registered successfully",
                              http_status=HttpStatusCode.CREATED.value)


def login():
    if request.method == "GET":
        return send_json_response(response_status=False, message_key="Login required",
                                  http_status=HttpStatusCode.UNAUTHORIZED.value)

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return send_json_response(response_status=False, message_key="Email and password are required",
                                  http_status=HttpStatusCode.BAD_REQUEST.value)

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return send_json_response(response_status=False, message_key="Invalid credentials",
                                  http_status=HttpStatusCode.UNAUTHORIZED.value)

    login_user(user, remember=True)

    return send_json_response(response_status=True, message_key="Login successful", http_status=HttpStatusCode.OK.value)


@login_required
def logout():
    logout_user()
    return send_json_response(response_status=True, message_key="Logout successful",
                              http_status=HttpStatusCode.OK.value)


@login_required
def user_info():
    data = {
        "email": current_user.email,
        "name": current_user.name
    }
    return send_json_response(response_status=True, message_key="Details Fetched Successfully",
                              http_status=HttpStatusCode.OK.value,
                              data=data)
