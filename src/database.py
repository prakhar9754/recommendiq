import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def get_engine():

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "recommendation_engine")
    )

    return create_engine(connection_url)