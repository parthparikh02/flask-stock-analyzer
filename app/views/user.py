from flask import request, jsonify
from app.models.user import User
from app.extensions import db
from flask_login import login_user, logout_user, login_required, current_user
from app.utils.common import send_json_response
from app.utils.constants import HttpStatusCode


def register():
    """
    Register a new user
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "user@example.com"
            password:
              type: string
              example: "mypassword"
            name:
              type: string
              example: "John Doe"
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: true
            message:
              type: string
              example: "User registered successfully"
      400:
        description: Bad request - Missing required fields or user already exists
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: false
            message:
              type: string
              example: "Email and password are required"
    """
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
    """
    Log in a user
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "user@example.com"
            password:
              type: string
              example: "mypassword"
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: true
            message:
              type: string
              example: "Login successful"
      400:
        description: Missing email or password
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: false
            message:
              type: string
              example: "Email and password are required"
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: false
            message:
              type: string
              example: "Invalid credentials"
    """
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
    return send_json_response(response_status=True, message_key="Login successful",
                              http_status=HttpStatusCode.OK.value)


@login_required
def logout():
    """
    Log out the current user
    ---
    tags:
      - User
    responses:
      200:
        description: Logout successful
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: true
            message:
              type: string
              example: "Logout successful"
    """
    logout_user()
    return send_json_response(response_status=True, message_key="Logout successful",
                              http_status=HttpStatusCode.OK.value)


@login_required
def user_info():
    """
    Get the current user's info
    ---
    tags:
      - User
    responses:
      200:
        description: Returns the current user's details
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: true
            message:
              type: string
              example: "Details Fetched Successfully"
            data:
              type: object
              properties:
                email:
                  type: string
                  example: "user@example.com"
                name:
                  type: string
                  example: "John Doe"
    """
    data = {
        "email": current_user.email,
        "name": current_user.name
    }
    return send_json_response(response_status=True, message_key="Details Fetched Successfully",
                              http_status=HttpStatusCode.OK.value,
                              data=data)
