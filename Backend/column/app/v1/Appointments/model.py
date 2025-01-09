from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .....db import Base
from datetime import datetime
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin



class Appointment(Base):
    __tablename__ = 'appointment'

    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime, nullable=False, default=datetime.now().date())
    service_id = Column(Integer, ForeignKey('service.service_id'), nullable=False)
    status = Column(String(50), default='pending')
    updated_date = Column(DateTime, nullable=False, default=datetime.now().date())

    service = relationship('Service', foreign_keys=[service_id])

    def to_dict(self):
        return {
            'appointment_id': self.appointment_id,
            'date': self.date_time,
            'status': self.status,
            'service_id': self.service_id,
            'updated_date': self.updated_date
        }