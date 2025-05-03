from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app.models.user import User

def token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):

        current_user_id = get_jwt_identity()

        current_user = User.query.get(current_user_id)

        if current_user is None:
            return jsonify({"msg": "User not found"}), 404

        # You can add additional checks for devices or other headers if needed
        # Example:
        # device_uid = request.headers.get('x-device-uid')
        # if device_uid and device_uid != current_user.device_uid:
        #     return jsonify({"msg": "Invalid device"}), 403

        return f(current_user, *args, **kwargs)

    return decorated
