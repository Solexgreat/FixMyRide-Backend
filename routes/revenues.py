from flask import Flask
from flask import Flask, jsonify, request, abort, redirect, render_template, flash
# from flask_login import login_user, logout_user, login_required, current_user, LoginManager
# from db import DB
from ..column.app.v1.Revenues.control import RevenueControl
from ..column.app.v1.core.auth import AUTH
from ..db import DB
from . import revenue_bp
from ..column.app.v1.core.middleware import authenticate
from ..column.app.v1.users.model import UserTypeEnum



User_Type_Enum = UserTypeEnum()
db = RevenueControl()
db_instance = DB()
AUTH = AUTH()


@revenue_bp.route('/revenue', methods=['GET'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.USER])
def get_revenue() -> str:
    """Return all the Revenue property
    """
    try:
        user = request.user
        if user.role != 'admin':
            return jsonify({'msg': "Not authorized"}), 403
        return jsonify(db.get_all_revenue()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@revenue_bp.route('/revenue', methods=['POST'], strict_slashes=False)
def create_revenue() ->str:
    """POST /revenue
       Return: Jsonify status 200
    """
    data = request.get_json()
    required_fields = ['date_time', 'total_appointment', 'total_repairs', 'total_revenue']
    err_msg = None

    # Check for missing fields
    for field in required_fields:
        if not data or data.get(field) == "":
            err_msg = f'{field} is missing'
            break
    if err_msg is None:
        try:
            date_time = data['date_time']
            total_appointment = data['total_appointment']
            total_repairs = data['total_repairs']
            total_revenue = data['total_revenue']
            revenue = db.add_revenue(date_time,
                            total_appointment,
                            total_repairs,
                            total_revenue)
            return jsonify({"message": "Revenure Created", 'revenue_id':revenue.revenue_id}), 201
        except Exception as e:
            err_msg = "can't create appointment: {}".format(e)
    return jsonify({'err_msg': err_msg}), 400

@revenue_bp.route('/delete/<int:revenue_id>', methods=['DELETE'], strict_slashes=False)
@authenticate
def delete_revenue(revenue_id):
    """
        delete service via revenue id
    """
    try:
        # db_instance.add_column('revenue', 'repair_id', 'TEXT')

        user = request.user
        if user.role != 'admin':
            return jsonify({'msg': 'Not authorized'}), 403
        del_service =db.delete_revenue(revenue_id)
        return jsonify(del_service), 200
    except Exception as e:
        return jsonify({'msg': str(e) }), 500
