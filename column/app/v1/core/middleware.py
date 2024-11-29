from functools import wraps
from flask import request, jsonify
from ..users.control import UserControl
from ..core.security import SECURITY

DB = UserControl()
security = SECURITY()

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session_id = request.cookies.get("session_id")
            if session_id:
                user = DB.find_user_by_session_id(session_id)  # Check if session_id exists in the database

                if user and security.validate_session(user.email, user.session_id):
                    request.user = user  # Add the user to the request context
                    return f(*args, **kwargs)
                else:
                    return jsonify({"message": "Invalid session"}), 403
            else:
                return jsonify({"message": "Token required"}), 403
        except Exception as e:
            raise Exception(f'{e}')

    return decorated_function