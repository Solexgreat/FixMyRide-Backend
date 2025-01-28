from sqlalchemy import create_engine
from flask import Flask, jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, OperationalError,  DBAPIError
from .model import User
from typing import List
from datetime import datetime
from .....db import DB
import logging

logger = logging.getLogger(__name__)

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('app.log')

# Set the logging level for the handler
file_handler.setLevel(logging.DEBUG)  # Adjust the level as needed

# Create a formatter to format the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Add the formatter to the handler
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)


class UserControl(DB):
    """User control class that inherits from DB"""

    def get_users(self) -> dict:
        """Return a list of users as dictionaries"""
        users = self._session.query(User).all()
        return [u.to_dict() for u in users]

    def add_user(self, **kwargs) -> dict:
        """Add a user to the session and commit"""
        try:
            user = User(**kwargs)
            self._session.add(user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        return user.to_dict()

    def find_user(self, field: str, value: str) -> User:
        """Find a user by provided criteria (e.g., email or user_name) and return the user"""

        try:
            query = self._session.query(User)

            user = query.filter(getattr(User, field) == value).first()

            if user is None:
                return None

        except DBAPIError as e:  # Replace with the actual database error type
            logger.exception("Database error:", exc_info=e)
            raise DBAPIError(f"Database error occurred: {e}")
        # raise InvalidRequestError("An error occurred while finding the user")

        return user

    def get_user_id(self, **kwargs) -> int:
        """Get the user_id of a user based on given criteria"""
        try:
            user = self.find_user(**kwargs)
            user_id = user.user_id
        except Exception as e:
            return e
        return user_id

    def get_user_by_id(self, user_id: int) -> dict:

        """
            Retrieve a user by their ID and return their details.
            Args:
                user_id (int): The ID of the user to retrieve.

            Returns:
                dict: A dictionary containing user details (name, username, email).

            Raises:
                NoResultFound: If no user with the given ID exists.
                Exception: For any other unexpected errors.
        """
        try:
            # Fetch user by ID
            user = self._session.query(User).filter_by(user_id=user_id).first()
            if not user:
                raise NoResultFound(f"User with ID {user_id} not found.")

            # Construct response
            user_data = {
                'username': user.user_name,
                'email': user.email
            }
            return user_data

        except NoResultFound as e:
            # Raise specific error if user not found
            raise e
        except Exception as e:
            # Log or handle generic errors
            raise Exception(f"An unexpected error occurred: {str(e)}")

    def update_user(self, **kwargs: dict) -> None:
        """Update a user's attributes"""

        user_name = kwargs.get('user_name')
        email = kwargs.get('email')

        try:
             #Verify if user exist by user_name or email
            if user_name:
                user = self.find_user('user_name', user_name)
            if not user_name:
                user = self.find_user('email', email)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"{key} is not a valid attribute of User")
            self._session.commit()
        except NoResultFound:
            return NoResultFound
        return user

    def find_user_by_session_id(self, session_id: str):
        """
            Get user via session_id
        """
        try:
            user = self._session.query(User).filter_by(session_id=session_id).first()
            return user
        except Exception as e:
            raise e