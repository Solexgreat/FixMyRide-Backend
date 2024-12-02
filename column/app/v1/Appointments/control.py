from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import and_
from .model import Appointment
from typing import List
from datetime import datetime, timedelta
from .....db import DB
from ..Revenues.model import Revenue
from ..Services.model import Service
from ..users.control import UserControl

user_db = UserControl()





class AppointmentControl(DB):
    """Appointment control class that inherits from DB"""

    def get_all_appointments(self, user_id: int, role: str) -> dict:
        """Return a list of all appointments as dictionaries"""

        try:

            if role == 'admin':
                appointments = self._session.query(Appointment).all()
            elif role == 'mechanic':
                appointments = self._session.query(Appointment).filter_by(mechanic_id=user_id).all()
            else:
                appointments = self._session.query(Appointment).filter_by(mechanic_id=user_id).all()

            return [a.to_dict() for a in appointments]
        except Exception as e:
            raise(f'{e}')

    def get_appointments(self, appointment_id: int, user_id: int, role: str) -> dict:
        """Return a list of all appointments as dictionaries"""
        #Get appointment and verify if it exist
        appointment = self._session.query(Appointment).filter_by(appointment_id=appointment_id).first()
        if not appointment:
            raise NoResultFound(f'Appointment with {appointment_id} does not exist')
        try:
            if role == 'admin':
                return appointment.to_dict()

            #Get the mechanic_id and check if it exist
            mechanic_id = appointment.mechanic_id
            if not mechanic_id:
                raise NoResultFound(f'Service or Mechanic no longer available')

            #Check if the user(mechanic or customer) is authorize to get appointment
            customer_id = appointment.customer_id
            if user_id != mechanic_id or user_id != customer_id:
                raise InvalidRequestError(f'Unauthorized request')

            return appointment.to_dict()
        except Exception as e:
            raise (f'{e}')

    def add_appointment(self, date: str, time: str, customer_id: int, service_id: int, status: str) -> Appointment:
        """Add an appointment and update revenue"""

        try:
            # Combine date and time into a datetime object
            date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
            # Create a new appointment
            appointment = Appointment(date_time=date_time, customer_id=customer_id,
                                      service_id=service_id, status=status)
            self._session.add(appointment)
            self._session.commit()

            # print("Created Appointment ID:", appointment.appointment_id)
            return appointment

        except Exception as e:
            self._session.rollback()
            raise Exception(f'{e}')

    def update_appointment(self, appointment_id: str, **kwargs: dict):
        """
            update appointment
        """
        #Fetech the appointment and check if it exist
        appointment = self._session.query(Appointment).get(appointment_id)
        if not appointment:
            raise NoResultFound (f'Appointment not found')

        #Update the appointment field with kwargs value
        for key, value in kwargs.items():
            setattr(appointment, key, value)

        #Update the updated_date field
        appointment.updated_date = datetime.now()

        self._session.commit()


        return appointment

    def get_appointment_between_dates(self, start_date_str: datetime, end_date_str: datetime):
        """
            Get appointments between a period of time
        """
        try:
            start_date = datetime.strptime(start_date_str, "%a, %d %b %Y")
            end_date = datetime.strptime(end_date_str, "%a, %d %b %Y") + timedelta(days=1)
            appointments = self._session.query(Appointment).filter(
                Appointment.date_time.between(start_date, end_date)
            ).all()
            appointments_dict = [appointment.to_dict() for appointment in appointments]
            return appointments_dict
        except Exception as e:
            raise Exception(f'{str(e)}')

    def get_completed_appointment_between_dates(self, start_date_str: str, end_date_str: str):
        """
            Get appointments with 'status' complete between a period of time
        """
        try:
            start_date = datetime.strptime(start_date_str, "%a, %d %b %Y")
            end_date = datetime.strptime(end_date_str, "%a, %d %b %Y") + timedelta(days=1)
            appointments = self._session.query(Appointment).filter(
                and_(
                    Appointment.status == 'completed',
                    Appointment.updated_date.between(start_date, end_date)
                )
                ).all()
            appointments_dict = [appointment.to_dict() for appointment in appointments]
            return appointments_dict
        except Exception as e:
            raise Exception(f'{str(e)}')

    def delete_appointment(self, appointment_id: int,)-> str:
        """Delete service by service_id"""
        appointment = self._session.query(Appointment).filter_by(appointment_id=appointment_id).first()
        if not appointment:
            raise NoResultFound(f'Appointment not found')

        try:
            self._session.delete(appointment)
            self._session.commit()
            return {"message": "Appointment deleted successfully"}
        except Exception as e:
            self._session.rollback()
            raise Exception(f'An error occured:{e} ')

    def generate_time_slots(self, start: int, end: int):

        slots = []
        current_time = start
        while current_time < end:
            hours = current_time // 60
            minutes = current_time % 60
            slots.append(f"{hours:02}:{minutes:02}")
            current_time += 30  # Increment by 30 minutes
        return slots

    def available_time(self, date_str: str):

        all_slots = self.generate_time_slots(540, 1020)

        try:
            date = datetime.strptime(date_str, "%a, %d %b %Y")
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())

            booked_appointments =(
                self._session.query(Appointment.date_time)
                .filter(
                    Appointment.date_time >= start_of_day,
                    Appointment.date_time <= end_of_day,
                )
                )

            booked_slots = {
                appointment.date_time.strptime("%H:%M") for appointment in booked_appointments
            }

            available_slots = [slot for slot in all_slots if slot not in booked_slots]

            return available_slots
        except Exception as e:
            return str(e)

    def available_mechanic(self, date_str: str, time: str):
        """
            Finds mechanics who are available at a specific date and time,
            ignoring mechanics with appointments within an hour before the requested time,
            except for appointments at 09:00 or 09:30.

            Args:
                date: The date (datetime.date) for the booking.
                time: The time (HH:MM) for the booking.

            Returns:
                A list of available mechanic IDs.
        """
        try:

            #combine the date and timeto datetime object
            date = datetime.strptime(date_str, "%a, %d %b %Y")
            booking_datetime = datetime.combine(date, datetime.strptime(time, "%H:%M").time())

             # Check for appointments one hour before the requested time
            one_hour_before = booking_datetime - timedelta(hours=1)

            #Query all distinct mechanics id
            all_mechanics = self._session.query(Appointment.mechanic_id).distinct().all()
            all_mechanics = [mechanic[0] for mechanic in all_mechanics]
            if not all_mechanics:
                raise NoResultFound('No mechanics found')

            #Query booked mechanics for the given time
           # Query booked mechanics at the requested time
            booked_mechanics = (
                self._session.query(Appointment.mechanic_id)
                .filter(
                    (Appointment.date_time == booking_datetime)  # Appointment exactly at requested time
                    | (Appointment.date_time == one_hour_before)  # Appointment an hour before
                )
                .filter(
                    ~(
                        (Appointment.date_time.time() == datetime.strptime("09:00", "%H:%M").time())
                        | (Appointment.date_time.time() == datetime.strptime("09:30", "%H:%M").time())
                    )  # Exclude 09:00 and 09:30 exceptions
                )
                .all()
            )

            booked_mechanics = [mechanics[0] for mechanics in booked_mechanics]

            #filter booked mechanics
            available_mechanics = [m for m in all_mechanics if m not in booked_mechanics]
            if not available_mechanics:
                raise NoResultFound("No available mechanics at this time")

            mechanic_names = []
            for mechanic_id in available_mechanics:
                try:
                    user_data = user_db.get_user_by_id(mechanic_id)  # Assuming this returns a dictionary
                    mechanic_names.append(user_data['name'])
                except NoResultFound:
                    # Skip if mechanic ID is not found
                    continue
                except Exception as e:
                    raise Exception(f"Error retrieving mechanic details: {str(e)}")

            return mechanic_names

            return available_mechanics
        except Exception as e:
            return str(e)
