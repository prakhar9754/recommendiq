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
    (int(user),)
    for user in users_df["visitorid"].dropna().unique()
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
        (int(item),)
        for item in items_df["itemid"].unique()
    ]

    cursor.executemany(query, data)

    connection.commit()

    cursor.close()
    connection.close()
    
def insert_interactions(interaction_df):

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
    '''Large-scale interaction data was loaded into MySQL using batch processing to reduce memory consumption and improve insertion efficiency.'''
    
    batch_size = 10000

    for start in range(0, len(interaction_df), batch_size):

        batch = interaction_df.iloc[start:start+batch_size]

        data = [
            (
                int(row.visitorid),
                int(row.itemid),
                int(row.interaction_strength),
                int(row.recency_days)
            )
            for row in batch.itertuples(index=False)
        ]

        cursor.executemany(query, data)

        connection.commit()

        print(
            f"Inserted {min(start + batch_size, len(interaction_df))} rows"
        )

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
