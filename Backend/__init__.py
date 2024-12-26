from flask import Flask
import os
from flask_jwt_extended import JWTManager
# from .config import Config
from .db import DB
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv


db_instance = DB()
load_dotenv()
mail = Mail()
migrate = Migrate()



def create_app():
	app = Flask(__name__)

	CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

	print(f"Current Environment: {os.getenv('FLASK_ENV')}")


	# Dynamically load the configuration based on FLASK_ENV
	env = os.getenv('FLASK_ENV', 'production')

	if env == 'development':
		app.config.from_object('config.DevelopmentConfig')
	elif env == 'production':
		app.config.from_object('config.ProductionConfig')
	else:
		app.config.from_object('config.ProductionConfig')

	print(f"DEBUG Mode: {app.config['DEBUG']}")


	# # Configure your secret key for encoding JWT
	# app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET']

	# # Initialize JWT manager
	# jwt = JWTManager(app)

	# Initialize Mail
	mail.init_app(app)


	# Initialize the database and attach it to the app
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# Database setup
	db_instance.init_app(app)

	# Initialize Flask-Migrate with the app and the custom database instance
	migrate.init_app(app, db_instance)


	from .routes import user_bp, service_bp, appointment_bp, repair_bp, revenue_bp, auth_bp  # Import your blueprints
	# Register your blueprints (routes)
	app.register_blueprint(user_bp)
	app.register_blueprint(auth_bp)
	app.register_blueprint(service_bp)
	app.register_blueprint(revenue_bp)
	app.register_blueprint(repair_bp)
	app.register_blueprint(appointment_bp)

	return app