from functools import wraps
from flask import request, jsonify
from ..users.control import UserControl
from ..core.security import SECURITY
from flask_jwt_extended import jwt_required, get_jwt_identity

user_control = UserControl()
security = SECURITY()

ACCESS_CONTROL = {
    "admin": ["GET /users", "POST /users", "DELETE /users"],
    "user": ["GET /users"],
    "guest": ["GET /public"],
}


def authenticate(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                session_id = request.cookies.get('session_id')
                print(f"Session ID: {session_id}")
                if session_id:
                    user = user_control.find_user_by_session_id(session_id)  # Check if session_id exists in the database

                    if user and security.validate_session(user.email, user.session_id):

                        # Permission check
                        if roles and user.user_type not in roles:
                            return jsonify({"message": "Access denied: insufficient permissions"}), 403

                        request.user = user  # Add the user to the request context
                        return f(*args, **kwargs)
                    else:
                        return jsonify({"message": "Invalid session"}), 403
                else:
                    return jsonify({"message": "cookie session_id not set by the browser"}), 403
            except Exception as e:
                raise Exception(f'{e}')

        return decorated_function
    return decorator