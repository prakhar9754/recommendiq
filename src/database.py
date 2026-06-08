"""
Database Module

Purpose:
Handle MySQL database operations for
the Smart Recommendation &
Personalization Engine.
"""


import mysql.connector
import pandas as pd

def create_connection():
    """
    Create MySQL connection.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prakhar@12",
        database="recommendation_engine"
    )
    return connection

def insert_users(
    users_df: pd.DataFrame
):
    """
    Insert unique users
    """

    connection = create_connection()

    cursor = connection.cursor()

    query = """
    INSERT IGNORE INTO users(visitor_id)
    VALUES (%s)
    """

    data = [
        (user,)
        for user in users_df["visitorid"].unique()
    ]

    cursor.executemany(
        query,
        data
    )

    connection.commit()

    cursor.close()

    connection.close()