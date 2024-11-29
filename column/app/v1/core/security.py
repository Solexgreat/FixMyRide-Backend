from ..users.control import UserControl
from flask import Flask, jsonify
from ..users.model import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
import bcrypt
from datetime import datetime, timedelta
# from ..... import run
# from itsdangerous import URLSafeTimedSerializer

# Initialize serializer with a secret key

DB = UserControl()

def _hash_password(password: str) -> bytes:
    """returned bytes is a salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def _generate_uuid():
    """Generate and return
       string uuid
    """
    return str(uuid.uuid4())


class SECURITY:
    """Auth class to interact with the authentication database.
    """
    def __init__(self) -> None:
        self._db = DB

    def create_session(self,):
        """Create a session via uuid
           update the user session and
           retyrb the session id
        """
        try:
            session_id = _generate_uuid()
            return session_id
        except NoResultFound:
            return NoResultFound

    def destroy_session(self, user_id: int) -> None:
        """Updates user's session_id to None
        """
        if not user_id:
            return None
        try:
            user = self._db.find_user(user_id)
            session_id = None
            self._db.update_user(user.user_id, session_id=session_id)
        except NoResultFound:
            return None

    def get_reset_password_token(self, **kwargs: dict) -> str:
        """Generate new token with uuid4
        """
        try:
            reset_token = _generate_uuid()
            expiration_time = datetime.now() + timedelta(hours=1)
            self._db.update_user(**kwargs, reset_token=reset_token, token_expiration=expiration_time)
            return reset_token
        except Exception as e:
            raise Exception(f'{e}')

    def validate_reset_token(self, email: str, reset_token: str) -> bool:
        """Validate the reset token and check for expiration."""
        try:
            user = self._db.find_user('email', email)
        except NoResultFound:
            return False

        if user.reset_token != reset_token:
            return False

        # Check if the token is expired
        if datetime.now() > user.token_expiration:
            return False

        return True

    def validate_session(self, email: str, session_id: str) -> bool:
        """Validate the reset token and check for expiration."""
        try:
            user = self._db.find_user("email", email)
        except NoResultFound:
            return False

        if user.session_id != session_id:
            return False

        # Check if the token is expired
        if datetime.now() > user.session_expiration:
            return False

        return True

