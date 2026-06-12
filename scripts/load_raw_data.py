import pandas as pd
from sqlalchemy import text
from src.database import get_engine

# Create database connection
engine = get_engine()

print("=" * 50)
print("LOADING RETAILROCKET RAW DATA INTO MYSQL")
print("=" * 50)

# --------------------------------------------------
# Load Events Data
# --------------------------------------------------

print("\nLoading events.csv...")

events_df = pd.read_csv("data/raw/events.csv")

events_df.to_sql(
    name="events_raw",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=50000,
    method="multi"
)

print(f"Events Loaded: {len(events_df):,} rows")


# --------------------------------------------------
# Load Item Properties Part 1
# --------------------------------------------------

print("\nLoading item_properties_part1.csv...")

item_prop_1_df = pd.read_csv("data/raw/item_properties_part1.csv")

item_prop_1_df.to_sql(
    name="item_properties_raw",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=50000,
    method="multi"
)

print(f"Part 1 Loaded: {len(item_prop_1_df):,} rows")


# --------------------------------------------------
# Load Item Properties Part 2
# --------------------------------------------------

print("\nLoading item_properties_part2.csv...")

item_prop_2_df = pd.read_csv("data/raw/item_properties_part2.csv")

item_prop_2_df.to_sql(
    name="item_properties_raw",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=50000,
    method="multi"
)

print(f"Part 2 Loaded: {len(item_prop_2_df):,} rows")


# --------------------------------------------------
# Load Category Tree
# --------------------------------------------------

print("\nLoading category_tree.csv...")

category_df = pd.read_csv("data/raw/category_tree.csv")

category_df.to_sql(
    name="category_tree_raw",
    con=engine,
    if_exists="append",
    index=False
)

print(f"Category Tree Loaded: {len(category_df):,} rows")


# --------------------------------------------------
# Validation
# --------------------------------------------------

print("\nValidating Loaded Data...")

with engine.connect() as connection:

    events_count = connection.execute(
        text("SELECT COUNT(*) FROM events_raw")
    ).scalar()

    item_count = connection.execute(
        text("SELECT COUNT(*) FROM item_properties_raw")
    ).scalar()

    category_count = connection.execute(
        text("SELECT COUNT(*) FROM category_tree_raw")
    ).scalar()

print("\n" + "=" * 50)
print("DATA LOAD COMPLETED")
print("=" * 50)

print(f"events_raw            : {events_count:,}")
print(f"item_properties_raw   : {item_count:,}")
print(f"category_tree_raw     : {category_count:,}")