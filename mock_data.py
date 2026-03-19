
import pandas as pd
from sqlalchemy import create_engine
import random
from datetime import datetime, timedelta

print("Bypassing the paywall... generating 30 days of realistic market data.")

# 1. The Empty Bucket
mock_historical_rates = []

# Let's start with a realistic base rate for USD to CDF
simulated_rate = 2850.00 

# 2. Time Travel Loop (Going from 30 days ago up to today)
for i in range(30):
    # We count backwards so the data is in chronological order
    target_date = datetime.now() - timedelta(days=30-i)
    formatted_date = target_date.strftime('%Y-%m-%d')
    
    # Simulate market volatility: The rate randomly moves up or down by 1 to 15 Francs a day
    volatility = random.uniform(-15.0, 15.0)
    simulated_rate = simulated_rate + volatility
    
    clean_row = {
        "date": formatted_date,
        "base_currency": "USD",
        "target_currency": "CDF",
        "exchange_rate": round(simulated_rate, 2) # Round to 2 decimal places
    }
    
    mock_historical_rates.append(clean_row)

# 3. Turn into DataFrame
df = pd.DataFrame(mock_historical_rates)
print("\n--- Synthetic Data Generated ---")
print(df.tail()) # Show the last 5 days

# 4. Inject directly into your Docker Database!
print("\nOpening the Postgres vault...")
db_url = 'postgresql://admin:password123@127.0.0.1:5455/forex_data'
engine = create_engine(db_url)

# We use 'replace' to wipe out yesterday's single row and drop in the 30 new ones
df.to_sql('exchange_rates', engine, if_exists='replace', index=False)

print("\nSuccess! 30 days of historical data are officially locked in the database.")
