import os
import psycopg2
from sqlalchemy import create_engine
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

database_name = "medapp"
#database_path = 'postgresql://postgres_deployment_medapp_user:EhRLLkptvFgJPnNmW6ezO9CoDGlkQZOw@dpg-cgmqgbrhp8ua8vs49q30-a/postgres_deployment_medapp'
database_path = "postgresql:///{}".format(database_name)
database_path = os.environ['DATABASE_URL']

#database_path = os.getenv("DATABASE_URL")
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

# Connect to the database
SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_TRACK_MODIFICATIONS = True
#secret_key = 'super secret key'
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)