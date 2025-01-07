from flask import Flask
import sys
import os

# Add the Backend directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from . import create_app, db_instance
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db_instance)

if __name__ == '__main__':
  app.run(debug=True)