from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from .model import Service
from typing import List
from datetime import datetime
from .....db import DB


class ServiceControl(DB):
    """Service control class that inherits from DB"""

    def get_service(self) -> dict:
        """Return a list of services as dictionaries"""
        services = self._session.query(Service).all()
        return [s.to_dict() for s in services]

    def get_all_category(self)-> list:
        """
            Return:
             List of  all categories as dictionaries
        """
        try:
            services = self._session.query(Service).all()
            services_dict = [s.to_dict() for s in services]
            categories = {service['category'] for service in services_dict if 'category' in service}

            return list(categories)
        except Exception as e:
            raise Exception(f"Error retrieving categories: {str(e)}")

    def get_category_services(self, category: str)-> list:
        """
            Return:
                List of all service for the provided category
        """
        try:
            services = self._session.query(Service).filter(Service.category==category).all()
            services_dict = [s.to_dict() for s in services]

            return services_dict
        except Exception as e:
            raise Exception(f"Error retrieving categories: {str(e)}")


    def get_service_id(self, **kwargs) -> int:
        """Get the service ID based on provided criteria"""
        try:
            service = self._session.query(Service).filter_by(**kwargs).first()
            if service is None:
                raise NoResultFound(f"No service found with criteria: {kwargs}")
            service_id = service.service_id
        except TypeError:
            raise InvalidRequestError("Invalid arguments provided.")
        return service_id

    def get_popular_service(self) -> list:
        """
        Return:
                A list of popular services
        """
        try:
            popula_services_list = ['Oil change','Brake Pad Replacement', 'Battery Replacement', 'Tire Rotation']

            services = []

            for name in popula_services_list:
                service = self._session.query(Service).filter(Service.name==name).first()
                if service:
                    services.append(service.to_dict())

            return services
        except Exception as e:
            raise Exception(e)

    def add_service(self, **kwargs: dict) -> dict:
        """Add a service to the session and commit"""
        try:
            service = Service(**kwargs)
            self._session.add(service)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        return service

    def delete_service(self, service_id: str, seller_id: int)-> str:
        """Delete service by service_id"""
        service = self._session.query(Service).filter_by(service_id=service_id).first()
        if not service:
            raise NoResultFound(f'Service not found')

        try:
            if str(seller_id) != service.seller_id:
                raise InvalidRequestError(f'Unauthorize user: ')
            self._session.delete(service)
            self._session.commit()
            return {"message": "Service deleted successfully"}
        except Exception as e:
            self._session.rollback()
            raise Exception(f'An error occured:{e} ')