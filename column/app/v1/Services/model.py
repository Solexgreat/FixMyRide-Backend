from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .....db import Base
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin




class Service(Base):
    __tablename__ = 'service'

    service_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    category = Column(String(255), nullable=False)


    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'service_id': self.service_id,
            'image': self.image_url
        }