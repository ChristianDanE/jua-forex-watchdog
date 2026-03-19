# import matplotlib as plt 
import pandas as pd
import requests
import json
api_key = "fc5b3f6e71da7741ee352d65"
url = f"https://v6.exchangerate-api.com/v6/fc5b3f6e71da7741ee352d65/latest/USD"
#this transalate the raw internaet data into a dictinarry
response = requests.get(url)
data = response.json()
#grabing the dictionary for all rate
all_rate = data['conversion_rates']
cdf_rate = all_rate['CDF']
print(f"Actuellement 1 USD vaut {cdf_rate} CDF")
# Create a new file named "raw_rates.json" and open it in "w" (write) mode
with open("raw_rates.json", "w") as file:
    # Dump the dictionary data into the file
    json.dump(data, file)
print("Data successfully saved to raw_rates.json!")

