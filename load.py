import pandas as pd 
from sqlalchemy import create_engine
import datetime

print("starting the database load process...")

# This loads your CSV file
df = pd.read_csv("/opt/airflow/scripts/clean_rates.csv")

# --- NEW STEP: Ensure the date column is readable by Python ---
df['date'] = pd.to_datetime(df['date'])

db_url = 'postgresql://admin:password123@postgres_db:5432/forex_data'
engine = create_engine(db_url)

# Use 'append' instead of 'replace' so you keep your history!
df.to_sql("exchange_rates", engine, if_exists='append', index=False)

print(f"Success! {len(df)} rows are now locked in the Postgres vault.")
