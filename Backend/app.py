from flask import Flask
import sys
from Backend import create_app, db_instance
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db_instance)

if __name__ == '__main__':
  app.run(debug=True)