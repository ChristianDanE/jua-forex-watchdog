import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Jua Analytics", page_icon="📈", layout="wide")

st.title("🇨🇩 Jua Market Intelligence")
st.write("Live USD/CDF Exchange Rate Monitoring")

# Connection
engine = create_engine('postgresql://admin:password123@127.0.0.1:5455/forex_data')

# Pull data
df = pd.read_sql("SELECT * FROM exchange_volatility ORDER BY date DESC", engine)

if not df.empty:
    # 1. Top Level Metrics
    latest_rate = df['daily_rate'].iloc[0]
    prev_rate = df['daily_rate'].iloc[1] if len(df) > 1 else latest_rate
    delta = round(latest_rate - prev_rate, 2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Current Rate (USD/CDF)", value=f"{latest_rate:,}", delta=f"{delta} CDF")
    with col2:
        # Calculate moving average volatility
        vol = abs((latest_rate - df['seven_day_moving_avg'].iloc[0]) / df['seven_day_moving_avg'].iloc[0])
        st.metric(label="7-Day Volatility", value=f"{vol:.2%}", delta="Market Swing", delta_color="off")

    # 2. The Chart
    st.subheader("Market Trend")
    # We sort ascending for the chart so time moves left to right
    st.line_chart(data=df.sort_values('date'), x='date', y='daily_rate')

    # 3. Data Table
    with st.expander("View Raw Data Vault"):
        st.dataframe(df)
else:
    st.warning("The Vault is currently empty. Check your Airflow tasks.")
