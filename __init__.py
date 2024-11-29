from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .db import DB
from flask_mail import Mail

mail = Mail()


def create_app():
	app = Flask(__name__)

	# Load configuration from config class
	app.config.from_object(Config)

	# Configure your secret key for encoding JWT
	app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET']

	# Initialize JWT manager
	jwt = JWTManager(app)

	# Initialize Mail
	mail.init_app(app)


	# # Initialize the database and attach it to the app
	db = DB()
	app.db = db


	from .routes import user_bp, service_bp, appointment_bp, repair_bp, revenue_bp, auth_bp  # Import your blueprints
	# Register your blueprints (routes)
	app.register_blueprint(user_bp)
	app.register_blueprint(auth_bp)
	app.register_blueprint(service_bp)
	app.register_blueprint(revenue_bp)
	app.register_blueprint(repair_bp)
	app.register_blueprint(appointment_bp)

	return app