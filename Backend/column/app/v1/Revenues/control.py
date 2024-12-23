from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from .model import Revenue
from typing import List
from datetime import datetime
from .....db import DB


class RevenueControl(DB):
    """Revenue control class that inherits from DB"""
    def get_all_revenue(self) -> list:
        """Retrieve all revenue records from the database."""
        revenues = self._session.query(Revenue).all()
        return [r.to_dict() for r in revenues]

    def add_revenue(self, date_time: datetime, total_appointment: int,
                    total_repair: int, total_revenue: int) -> Revenue:
        """Add a new revenue record to the session and commit it."""
        revenue = Revenue(date_time=date_time, total_appointment=total_appointment,
                          total_repair=total_repair, total_revenue=total_revenue)
        self._session.add(revenue)
        self._session.commit()
        return revenue

    def delete_revenue(self, revenue_id: str)-> str:
        """Delete revenue by revenue_id"""
        revenue = self._session.query(Revenue).filter_by(revenue_id=revenue_id).first()
        if not revenue:
            raise NoResultFound(f'Revenue not found')

        try:
            self._session.delete(revenue)
            self._session.commit()
            return {"message": "Revenue deleted successfully"}
        except Exception as e:
            self._session.rollback()
            raise Exception(f'An error occured: {e}')