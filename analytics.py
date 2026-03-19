import pandas as pd
from sqlalchemy import create_engine
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv() # This loads the variables from .env

# 1. Database Connection
# Note: Airflow uses 'postgres_db:5432'. 
# If running manually on Ubuntu, change to '127.0.0.1:5455'
# 1. Pull the password from the secret vault
db_pass = os.getenv('DB_PASSWORD')

# 2. Build the URL using an "f-string" (the 'f' lets us put the variable inside)
db_url = f'postgresql://admin:{db_pass}@localhost:5455/forex_data'

# 3. Open the tunnel
engine = create_engine(db_url)

# 2. The Analytics Query
sql_query = """
SELECT 
    date,
    exchange_rate AS daily_rate,
    ROUND(CAST(AVG(exchange_rate) OVER (
        ORDER BY date ASC 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS NUMERIC), 2) AS seven_day_moving_avg
FROM exchange_rates
ORDER BY date DESC
LIMIT 15;
"""

print("Calculating Volatility Metrics...")
df = pd.read_sql(sql_query, engine)

# 3. Save the report to the database (The missing piece!)
try:
    df.to_sql('exchange_volatility', engine, if_exists='replace', index=False)
    print("Success! Intelligence report saved to 'exchange_volatility' table.")
except Exception as e:
    print(f"Database save failed: {e}")

# 4. Volatility Alert Logic
if not df.empty:
    latest_rate = df['daily_rate'].iloc[0]
    moving_avg = df['seven_day_moving_avg'].iloc[0]
    
    # Calculate actual percent change
    percent_change = abs((latest_rate - moving_avg) / moving_avg)
    
    print(f"\n--- Current Stats ---")
    print(f"Daily Rate: {latest_rate}")
    print(f"7-Day Avg: {moving_avg}")
    print(f"Volatility: {percent_change:.2%}")

    # Set threshold at 2% (0.02)
    threshold = 0.02 

    if percent_change > threshold:
        print(f"ALERT: High Volatility detected!")
        
        msg = EmailMessage()
        msg.set_content(f"Watchdog Alert! Market volatility for USD/CDF is at {percent_change:.2%}.\n\nLatest Rate: {latest_rate}\n7-Day Average: {moving_avg}")
        msg['Subject'] = f"VOLATILITY ALERT: {percent_change:.2%} Change Detected"
        msg['From'] = "danetshoga@gmail.com"
        msg['To'] = "danetshoga@gmail.com"

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('danetshoga@gmail.com',os.getenv('GMAIL_PASSWORD'))
                smtp.send_message(msg)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Email failed: {e}")
else:
    print("No data found to analyze.")
