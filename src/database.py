from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def get_engine():

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="Prakhar@12",
        host="localhost",
        database="recommendation_engine"
    )

    return create_engine(connection_url)