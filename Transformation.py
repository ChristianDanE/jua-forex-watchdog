import pandas as pd
import json
print("starting transfroamtion...")

with open ("raw_rates.json", "r") as file:
    raw_data =json.load(file)
    
clean_data = {
    "date": raw_data.get("time_last_update_utc", "Unknown Date"),
    "base_currency": raw_data.get("base_code", "USD"),
    "target_currency": "CDF",
    "exchange_rate": raw_data["conversion_rates"]["CDF"]
}
df = pd.DataFrame([clean_data])
print("\nhere is your clean data:")
print(df)
print("\n")
df.to_csv("clean_rates.csv", index = False)

print("Transformation succesful! saved to clean_rates.csv")
