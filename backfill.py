# NOTE: This script's logic is perfect, but the ExchangeRate-API requires a paid "Pro" plan 
# to access the /history/ endpoint. Used mock_data.py instead to build the local database.

import requests
import pandas as pd
import time
from datetime import datetime, timedelta

print("Starting the Time Machine... fetching 30 days of data.")

api_key = "fc5b3f6e71da7741ee352d65"
base_currency = "USD"
target_currency = "CDF"

# 1. The Empty Bucket to hold all our clean rows
all_historical_rates = []

# 2. The Loop (Runs 30 times)
for i in range(30):
    
    # Calculate the exact date for this specific loop
    target_date = datetime.now() - timedelta(days=i)
    
    # Extract the Year, Month, and Day to inject into the URL
    year = target_date.strftime('%Y')
    month = target_date.strftime('%m')
    day = target_date.strftime('%d')
    
    # The clean date format for our database (e.g., "2026-03-10")
    formatted_date = target_date.strftime('%Y-%m-%d')
    
    print(f"Fetching data for {formatted_date}...")
    
    # 3. EXTRACT: The Dynamic URL
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/history/{base_currency}/{year}/{month}/{day}"
    
    response = requests.get(url)
    data = response.json()
    
    # Check if the API actually gave us the data (Safety check!)
    if data.get("result") == "success":
        
        # 4. TRANSFORM: Clean the data exactly like you did before
        clean_row = {
            "date": formatted_date,
            "base_currency": base_currency,
            "target_currency": target_currency,
            "exchange_rate": data["conversion_rates"][target_currency]
        }
        
        # 5. Toss the clean row into the bucket
        all_historical_rates.append(clean_row)
        
    else:
        # If the API blocks us, print the error so we aren't blind
        error_type = data.get("error-type", "Unknown Error")
        print(f"  -> API Error for {formatted_date}: {error_type}")
        
    # Senior Engineer Trick: Pause for 0.5 seconds so we don't accidentally attack the API server and get banned
    time.sleep(0.5)

# 6. Outside the loop: Turn the full bucket into a Pandas DataFrame
df = pd.DataFrame(all_historical_rates)

print("\n--- Time Travel Complete! ---")
print(df.head(10)) # Print the first 10 rows to verify
print(f"\nTotal rows successfully collected: {len(df)}")

# Save a backup locally
df.to_csv("historical_clean_rates.csv", index=False)
print("Saved local backup to historical_clean_rates.csv")