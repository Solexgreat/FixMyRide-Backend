import os
from dotenv import load_dotenv



load_dotenv()

class Config:
	"""Base configuration class."""
	# SECRET_KEY = os.getenv('SECRET_KEY')
	JWT_SECRET = os.getenv('JWT_SECRET', 'default_secret_key')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
	MAIL_DEFAULT_SENDER = ('Fix My Ride', os.getenv('MAIL_USERNAME'))

class DevelopmentConfig(Config):
	"""Development environment configuration."""
	DEBUG = True
	SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
	"""Production environment configuration."""
	DEBUG = False
	SQLALCHEMY_ECHO = False

class TestingConfig(Config):
	"""Testing environment configuration."""
	TESTING = True
	DATABASE_URL = 'sqlite:///:memory:'