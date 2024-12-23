from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship
from .....db import Base
from ..Services.model import Service
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

class UserTypeEnum:
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    session_id = Column(String(225), nullable=True)
    reset_token = Column(String(225), nullable=True)
    token_expiration = Column(DateTime(), nullable=True)
    session_expiration= Column(DateTime(), nullable=True)
    is_active = Column(Boolean(), default=True)
    user_type = Column(
        Enum(UserTypeEnum.ADMIN, UserTypeEnum.USER, UserTypeEnum.GUEST, name="user_type_enum"),
        nullable=False
    )


    def to_dict(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_name': self.user_name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
        }