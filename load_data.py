import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

print("DB_USER:", DB_USER)
print("DB_HOST:", DB_HOST)
print("DB_PORT:", DB_PORT)
print("DB_NAME:", DB_NAME)

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("One or more database environment variables are missing.")

password = quote_plus(DB_PASSWORD)

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print(f"Connecting to {DB_HOST}:{DB_PORT}/{DB_NAME}")

# Test connection
with engine.connect() as conn:
    conn.execute(text("SELECT 1"))
    print("Database connection successful!")

# Read CSVs
products_df = pd.read_csv("Data/processed/products.csv")
warehouses_df = pd.read_csv("Data/processed/warehouses.csv")
inventory_df = pd.read_csv("Data/processed/inventory.csv")
demand_df = pd.read_csv("Data/processed/demand.csv")
operations_df = pd.read_csv("Data/processed/operations.csv")

# Clear existing data but keep schema + constraints, commented during data load into kubernetes postgreSQL as the database is fresh 
#with engine.begin() as conn:
    #conn.execute(text("TRUNCATE TABLE operations, demand, inventory, warehouses, products CASCADE"))

# Reload data in parent -> child order
#products_df.to_sql("products", engine, if_exists="append", index=False)
#warehouses_df.to_sql("warehouses", engine, if_exists="append", index=False)
#inventory_df.to_sql("inventory", engine, if_exists="append", index=False)
#demand_df.to_sql("demand", engine, if_exists="append", index=False)
#operations_df.to_sql("operations", engine, if_exists="append", index=False)

# Reload data in parent -> child order #for kubernetes
products_df.to_sql("products", engine, if_exists="replace", index=False)
warehouses_df.to_sql("warehouses", engine, if_exists="replace", index=False)
inventory_df.to_sql("inventory", engine, if_exists="replace", index=False)
demand_df.to_sql("demand", engine, if_exists="replace", index=False)
operations_df.to_sql("operations", engine, if_exists="replace", index=False)


print("Data loaded successfully!")