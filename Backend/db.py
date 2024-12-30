import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()
Base = declarative_base()


class DB:
    """DB class
    """

    def __init__(self, drop_tables=False) -> None:
        """Initialize a new DB instance"""
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise RuntimeError("DATABASE_URL environment variable is not set.")
        try:
            self._engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800,
                echo=True
            )
            if drop_tables:
                Base.metadata.drop_all(self._engine)
            Base.metadata.create_all(self._engine)
            self.Session = scoped_session(sessionmaker(bind=self._engine))
        except Exception as e:
            raise RuntimeError(f"Failed to connect to the database: {e}")

    def init_app(self, app):
        """Bind database to Flask app"""
        app.teardown_appcontext(self.teardown)
        app.engine = self._engine
        app.session = self.Session

    @property
    def _session(self):
        """Thread-safe session object"""
        return self.Session()

    @property
    def engine(self):
        """Expose the engine for external use."""
        return self._engine

    def teardown(self, exception=None):
        """Remove the session at the end of the request"""
        self.Session.remove()

    def add_column(self, table_name, column_name, column_type):
        """Adds a column to an existing table."""
        with self._engine.connect() as connection:
            connection.execute(
                text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
            )

    def drop_column(self, table_name, column_name):
        """Removes a column from an existing table."""
        with self._engine.connect() as connection:
            connection.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {column_name};"))
