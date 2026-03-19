import pandas as pd
from sqlalchemy import create_engine

# 1. Open the tunnel to port 5455
db_url = 'postgresql://admin:password123@127.0.0.1:5455/forex_data'
engine = create_engine(db_url)

# 2. Write your SQL Query (Let's just grab the first 5 rows)
sql_query = "SELECT * FROM exchange_rates LIMIT 5;"

result = pd.read_sql(sql_query, engine)

print("---- data from the postges vault---")
print(result)