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
        (user,) #tuple row by row
        for user in users_df["visitorid"].unique()
    ]
    #insert all rows at once 
    cursor.executemany(
        query,
        data
    )

    connection.commit()

    cursor.close()

    connection.close()
    
def insert_items(items_df: pd.DataFrame) -> None:
    """
    Insert unique items into items table.
    """

    connection = create_connection()

    cursor = connection.cursor()

    query = """
    INSERT IGNORE INTO items(item_id)
    VALUES (%s)
    """

    data = [
        (item,)
        for item in items_df["itemid"].unique()
    ]

    cursor.executemany(query, data)

    connection.commit()

    cursor.close()
    connection.close()
    
def insert_interactions(
    interaction_df: pd.DataFrame
):
    """
    Insert engineered interactions.
    """
    connection = create_connection()
    cursor = connection.cursor()
    query = """
     INSERT INTO interactions(
        visitor_id,
        item_id,
        interaction_strength,
        recency_days
    )
    VALUES (%s, %s, %s, %s)
    """
    data = list(
        interaction_df[
            [
                "visitorid",
                "itemid",
                "interaction_strength",
                "recency_days"
            ]
        ].itertuples(
            index=False,
            name=None
        )
    )
    cursor.executemany(
        query,
        data
    )

    connection.commit()

    cursor.close()

    connection.close()
    
#Read Data Back
def fetch_interactions():
    """
    Retrieve interactions.
    """

    connection = create_connection()

    query = """
    SELECT *
    FROM interactions
    """
    
    interactions_df = pd.read_sql(
        query,
        connection
    )
    connection.close()

    return interactions_df
