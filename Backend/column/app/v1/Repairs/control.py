from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from .model import Repair
from ..Services.model import Service
from ..Revenues.model import Revenue
from typing import List
from datetime import datetime
from .....db import DB


class RepairControl(DB):
    """Repair control class that inherits from DB"""

    def get_all_repairs(self) -> dict:
        """Return a list of all repairs as dictionaries"""
        repairs = self._session.query(Repair).all()
        return [r.to_dict() for r in repairs]

    def add_repair(self, date_time: datetime, customer_id: int,
                   service_id: int, mechanic_id: int) -> Repair:
        """Add a new repair to the database and return the repair object"""
        if date_time is None:
            date_time = datetime.now().date()
        try:
            repair = Repair(date_time=datetime.now(),
                            customer_id=customer_id,
                            service_id=service_id,
                            mechanic_id=mechanic_id)
            self._session.add(repair)
            self._session.commit()

            revenue = self._session.query(Revenue).filter_by(repair_id=repair.repair_id).first()
            if not revenue:
                revenue= Revenue(repair_id=repair.repair_id)
                self._session.add(revenue)
                self._session.commit()

            service = self._session.query(Service).filter_by(service_id=service_id).first()
            if service:
                revenue.total_revenue += service.price
                revenue.total_appointments += 1
                revenue.total_repairs += 1


                self._session.commit()
            else:
                raise ValueError(f'Service not available')
            return repair

        except Exception as e:
            self._session.rollback()
            raise Exception(f'{e}')

    def delete_repair(self, repair_id: int):
        """
            Delete repair and also update revenue
        """
        repair = self._session.query(Repair).filter_by(repair_id=repair_id).first()

        if not repair:
            raise NoResultFound(f'Repair not found')

        try:
            #update revenue database
            revenue= self._session.query(Revenue).filter_by(repair_id=repair_id).first()
            if revenue:
                self._session.delete(revenue)

            self._session.delete(repair)
            self._session.commit()
            return {"msg": "deleted successfully"}
        except Exception as e:
            self._session.rollback()
            raise Exception(f'An error occured: {e}')