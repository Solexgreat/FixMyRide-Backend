from flask import Flask
import sys
from Backend import create_app
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
  app.run(debug=True)