from flask import Flask
from flask import Flask, jsonify, request, abort, redirect, render_template, flash
# from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from ..column.app.v1.Appointments.control import AppointmentControl
from ..column.app.v1.core.auth import AUTH
from . import appointment_bp
from ..db import DB
from ..column.app.v1.core.middleware import authenticate
from ..column.app.v1.users.model import UserTypeEnum


User_Type_Enum = UserTypeEnum()
db_instance = DB()
db = AppointmentControl()
auth = AUTH()


@appointment_bp.route('/create', methods=['POST'], strict_slashes = False)
def Create_appointment() -> str:
    """POST /appoitments
       Return:
       json obj with status 201
    """
    data = request.get_json()

    try:
    # db_instance.drop_column('appointments', 'model')
    # db_instance.add_column('appointments', 'date', 'TEXT')
        date = data.get('date')
        time = data.get('time')
        service_id = data.get('service_id')
        status = data.get('status')
        appointment = db.add_appointment(date, time,
                            service_id, status)
        return jsonify({"message": "sucessfully created", 'appointment_id': f'{appointment.appointment_id}'}), 201
    except Exception as e:
        return jsonify({'msg': 'Internal error', 'error': str(e)}), 500

@appointment_bp.route('/', methods=['GET'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.USER])
def appointment_history() -> str:
    """Render the appointment history page"""
    try:
        user_id = request.user.user_id
        role = request.user.role

        appointments = db.get_all_appointments(user_id, role)
        return jsonify({'Appointments' : appointments}), 201
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@appointment_bp.route('/history_between', methods=['GET'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def appointment_history_between() -> str:
    """Render the appointment history page"""
    try:
        data = request.args.get()
        initial_date = data.get('initial_date')
        current_date = data.get('current_date')
        user_Id = request.user_id

        appointments = db.get_appointment_history_between(user_Id, initial_date, current_date)
        return appointments
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@appointment_bp.route('/completed_between', methods=['GET'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def appointment_completed_between() -> str:
    """Render the completed appointment history page"""
    try:
        data = request.args.get()
        initial_date = data.get('initial_date')
        current_date = data.get('current_date')
        role = request.user.role

        #Check if user is an admin
        if role != 'admin':
            return jsonify({'msg': 'unauthorised user'}), 403

        appointments = db.get_completed_appointment_between_dates(initial_date, current_date)
        return jsonify(appointments), 201
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@appointment_bp.route('/appointment/<int:appointment_id>', methods=['GET'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def get_appointment(appointment_id) -> str:
    """Return json of an appointments
    """
    user = request.user
    role = user.role
    user_id = user.user_id
    try:
        appointment = db.get_appointments(appointment_id, user_id, role)
        return jsonify(appointment)
    except Exception as e:
        return jsonify({'error': f'{e}'}), 500

@appointment_bp.route('/update_appointment/<int:appointment_id>', methods=['PUT'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def update_appointment(appointment_id) -> str:
    """Return json of all appointments
    """

    data = request.get_json()
    try:
        # db_instance.add_column('appointment', 'mechanic_id', 'INETGER')
        if not data:
            return jsonify({'msg': 'request is empty'}), 400
        appointment = db.update_appointment(appointment_id, **data)
        return jsonify({'msg': 'Appointment updated successfuly', 'appointment_id': f'{appointment.appointment_id}'})
    except Exception as e:
        return jsonify({'msg': 'Internal error', 'error': str(e)}), 500


@appointment_bp.route('/delete/<int:appointment_id>', methods=['DELETE'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def delete_sercice(appointment_id):
    """
        delete service via service_id
    """
    try:
        user_id = request.user.user_id
        del_service = db.delete_appointment(appointment_id)
        if del_service:
            return jsonify(del_service), 201
    except Exception as e:
        return jsonify({'msg': str(e) }), 500

@appointment_bp.route('/available_slots', methods=['GET'], strict_slashes=False)
# @authenticate
def available_slots():
    """
        GEt available slots
    """

    data= request.args.get('date')
    try:
        available_slots = db.available_time(data)
        if available_slots :
            return jsonify(available_slots), 201

    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@appointment_bp.route('/available_mechanics', methods=['GET'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def available_mechanics():
    """
        GEt available mechanics
    """

    data= request.args
    date = data.get('date')
    time = data.get('time')
    try:
        available_mechanics = db.available_mechanice(date, time)
        if available_slots :
            return jsonify(available_mechanics), 201

    except Exception as e:
        return jsonify({'msg': str(e)}), 500