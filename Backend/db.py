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
        self._engine = create_engine(database_url, echo=True)

        if drop_tables:
            Base.metadata.drop_all(self._engine)

        Base.metadata.create_all(self._engine)

        # Use scoped_session for thread-safe sessions
        self.Session = scoped_session(sessionmaker(bind=self._engine))

    @property
    def _session(self):
        """Thread-safe session object"""
        return self.Session()

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

    def create_enum_type(engine, enum_name, values):
        """Creates an ENUM type in the database."""
        values_clause = ", ".join(f"'{value}'" for value in values)
        with engine.connect() as connection:
            connection.execute(
                text(f"DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{enum_name}') THEN CREATE TYPE {enum_name} AS ENUM ({values_clause}); END IF; END $$;")
            )
