from flask import jsonify, request
from sqlalchemy.exc import InvalidRequestError
from ..column.app.v1.Services.control import ServiceControl
from ..column.app.v1.users.model import UserTypeEnum
from ..column.app.v1.core.auth import AUTH
from . import service_bp
from ..db import DB
from ..column.app.v1.core.middleware import authenticate
from ..utils.cache import cache


db_instance = DB()
service_control = ServiceControl()
AUTH = AUTH()
User_Type_Enum = UserTypeEnum()


@service_bp.route('/', methods=['GET'], strict_slashes=False)
# @authenticate(roles=[User_Type_Enum.ADMIN])
def get_service() -> str:
    """Return all service
    """
    try:
        # db_instance.add_column('service', 'image_url', 'TEXT')
        # user = request.user
        # if user.role != 'admin':
        #     return jsonify({'msg': "Not authorized"}), 403

        services = service_control.get_service()
        return jsonify({'services': services}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@service_bp.route('/pupolar_services', methods=['GET'], strict_slashes=False)
# @authenticate(roles=[User_Type_Enum.ADMIN])
@cache.cached(timeout=160, query_string=True)
@cache.cached(timeout=160)
def get_popular_service() -> str:
    """Return all service
    """
    try:
        # user = request.user
        # if user.role != 'admin':
        #     return jsonify({'msg': "Not authorized"}), 403

        services = service_control.get_popular_service()
        return jsonify(services), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@service_bp.route('/categories', methods=['GET'], strict_slashes=False)
# @authenticate(roles=[User_Type_Enum.ADMIN])
@cache.cached(timeout=160)
def get_categories()-> dict:
    """
        Return all categories
    """
    try:
        categories = service_control.get_all_category()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@service_bp.route('/category_services', methods=['GET'], strict_slashes=False)
# @authenticate(roles=[User_Type_Enum.ADMIN])
@cache.cached(timeout=160, query_string=True)
def get_category_services():
    """
        Return all categories
    """
    data = request.args.get('category')
    try:
        services = service_control.get_category_services(data)
        return jsonify(services), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@service_bp.route('/service_name', methods=['GET'], strict_slashes=False)
# @authenticate(roles=[User_Type_Enum.USER])
def get_service_name()-> list:
    """
        Return all categories
    """
    try:
        servcies = service_control.get_category_service()
        return jsonify({'services': servcies}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@service_bp.route('/create_service', methods=['POST'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def create_service() ->str:
    """POST /revenue
       Return: Jsonify status 200
    """
    data = request.get_json()
    user = request.user

    try:
        if not data:
            return jsonify({'message': 'Expecting data'}), 400

        service_list = [service_control.add_service(**services) for services in data]
        service_list = [service['service_id'] for service in service_list  ]
        return jsonify({"message": "Service is Created", 'service_id': f'{service_list}'}), 201
    except Exception as e:
        return jsonify({'message': 'Internal error', 'error': str(e)}), 500

@service_bp.route('/delete/<int:service_id>', methods=['DELETE'], strict_slashes=False)
@authenticate(roles=[User_Type_Enum.ADMIN])
def delete_sercice(service_id):
    """
        delete service via service_id
    """
    try:
        user_id = request.user.user_id
        del_service = service_control.delete_service(service_id, user_id)
        if del_service:
            return jsonify({'msg': 'Service deleted successfully', 'service_id': service_id}), 201
    except InvalidRequestError as e:
        return jsonify({'message': str(e)}), 403
    except Exception as e:
        return jsonify({'message': str(e) }), 500