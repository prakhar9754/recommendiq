from sqlalchemy import create_engine

# Database Configuration
DB_USER = "root"
DB_PASSWORD = "Prakhar@12"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "recommendation_engine"

def get_engine():
    """
    Create and return SQLAlchemy engine.
    """
    engine = create_engine(
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return engine