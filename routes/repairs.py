from flask import Flask
from flask import Flask, jsonify, request, abort, redirect, render_template, flash
# from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from ..column.app.v1.Repairs.control import RepairControl
from Backend.column.app.v1.core.auth import AUTH
from . import repair_bp
from ..db import DB
from ..column.app.v1.core.middleware import authenticate


db_instance = DB()
db = RepairControl()
AUTH = AUTH()



@repair_bp.route('/repairs', methods=['GET'], strict_slashes=False)
@authenticate
def get_repairs() -> str:
    """Return json of all repairs
    """

    try:
        user = request.user
        if user.role != 'admin' or user.role != 'mechanic':
            return jsonify({'msg': 'Not authorized'}), 403

        return jsonify(db.get_all_repairs()), 201
    except Exception as e:
        return jsonify({'error': str(e)})

@repair_bp.route('/create-repair', methods=['POST'], strict_slashes = False)
@authenticate
def create_repairs() -> str:
    """POST /repairs
       Return: Jsonify(message) status 200
    """

    # db_instance.drop_column('revenue', 'date')
    data = request.get_json()
    user_id = request.user.user_id
    err_msg = None
    if not data:
        err_msg = 'wrong format'

    if not err_msg and data['customer_id']  == "":
        err_msg = 'customer_id is messing'
    if not err_msg and data['service_id']  == "":
        err_msg = 'service_id is messing'
    if err_msg is None:
        try:
            date_time = None
            customer_id = data['customer_id']
            service_id = data['service_id']
            mechanic_id = user_id
            repair = db.add_repair(date_time,
                            customer_id,
                            service_id,
                            mechanic_id)
            return jsonify({"message": "Repair Created successfully", 'repair_id': repair.repair_id}), 200
        except Exception as e:
            err_msg = "can't create appointment:"
            return jsonify({'msg': err_msg, 'error': str(e)}), 500

@repair_bp.route('/delete/<int:repair_id>', methods=['DELETE'], strict_slashes=False)
@authenticate
def delete_revenue(repair_id):
    """
        delete service via revenue id
    """
    try:
        user = request.user
        if user.role != 'admin':
            return jsonify({'msg': 'Not authorized'}), 403

        del_service = db.delete_repair(repair_id)
        return jsonify(del_service), 200
    except Exception as e:
        return jsonify({'msg': str(e) }), 500