from flask import Flask
from flask import Flask, jsonify, request, abort, redirect, render_template, flash
# from flask_login import login_user, logout_user, login_required, current_user, LoginManager
# from .db import DB
from sqlalchemy.exc import InvalidRequestError
from ..column.app.v1.Services.control import ServiceControl
from Backend.column.app.v1.core.auth import AUTH
from . import service_bp
from ..db import DB
from ..column.app.v1.core.middleware import authenticate


db_instance = DB()
db = ServiceControl()
AUTH = AUTH()


@service_bp.route('/services', methods=['GET'], strict_slashes=False)
@authenticate
def get_service() -> str:
    """Return all service
    """
    try:
        # user = request.user
        # if user.role != 'admin':
        #     return jsonify({'msg': "Not authorized"}), 403

        services = db.get_service()
        return jsonify({'services': services}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@service_bp.route('/categories', methods=['GET'], strict_slashes=False)
@authenticate
def get_categories()-> list:
    """
        Return all categories
    """
    try:
        categories = db.get_all_category()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@service_bp.route('/service_name', methods=['GET'], strict_slashes=False)
@authenticate
def get_service_name()-> list:
    """
        Return all categories
    """
    try:
        servcies = db.get_category_service()
        return jsonify({'services': servcies}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@service_bp.route('/create_service', methods=['POST'], strict_slashes=False)
@authenticate
def create_service() ->str:
    """POST /revenue
       Return: Jsonify status 200
    """
    data = request.get_json()
    user = request.user
    seller_id = user.user_id

    try:
        if not data:
            return jsonify({'msg': 'Expecting data'}), 400

        # db_instance.add_column('service', 'description', 'TEXT')

        service = db.add_service(**data, seller_id=seller_id)
        return jsonify({"message": "Service is Created", 'service_id': f'{service.service_id}'}), 201
    except Exception as e:
        return jsonify({'msg': 'Internal error', 'error': str(e)}), 500

@service_bp.route('/delete/<int:service_id>', methods=['DELETE'], strict_slashes=False)
@authenticate
def delete_sercice(service_id):
    """
        delete service via service_id
    """
    try:
        user_id = request.user.user_id
        del_service = db.delete_service(service_id, user_id)
        if del_service:
            return jsonify({'msg': 'Service deleted successfully', 'service_id': service_id}), 201
    except InvalidRequestError as e:
        return jsonify({'msg': str(e)}), 403
    except Exception as e:
        return jsonify({'msg': str(e) }), 500

