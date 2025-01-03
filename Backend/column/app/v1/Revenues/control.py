from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from .model import Revenue
from typing import List
from datetime import datetime, timedelta
from .....db import DB


class RevenueControl(DB):
    """Revenue control class that inherits from DB"""
    def get_all_revenue(self) -> list:
        """Retrieve all revenue records from the database."""

        try:
            revenues = self._session.query(Revenue).all()
            revenues_dict =  [revenue.to_dict() for revenue in revenues]

             #Calculate the total repair revenue
            total_repair_revenue = sum(revenue.get('repair_price', 0) for revenue in revenues_dict)

            # Append total repair revenue to the result
            return {"revenues": revenues_dict, "total_repair_revenue": total_repair_revenue}

        except Exception as e:
            # Include the traceback for easier debugging
            raise Exception(f"Error in get_revenue_between_dates: {str(e)}")

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

    def get_revenue_between_dates(self, start_date_str: datetime, end_date_str: datetime):
        """
            Get appointments between a period of time
        """
        try:
            start_date = datetime.strptime(start_date_str, "%a, %d %b %Y")
            end_date = datetime.strptime(end_date_str, "%a, %d %b %Y") + timedelta(days=1)
            revenues= self._session.query(Revenue).filter(
                Revenue.date_time.between(start_date, end_date)
            ).all()
            revenues_dict = [revenue.to_dict() for revenue in revenues]

            #Calculate the total repair revenue
            total_repair_revenue = sum(revenue.get('repair_price', 0) for revenue in revenues_dict)

            # Append total repair revenue to the result
            return {"revenues": revenues_dict, "total_repair_revenue": total_repair_revenue}
        except Exception as e:
            raise Exception(f'{str(e)}')
