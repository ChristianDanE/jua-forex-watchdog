# 🇨🇩 Jua Forex Watchdog: Market Intelligence Pipeline

An end-to-end Data Engineering framework designed to monitor USD/CDF exchange rate volatility. This system demonstrates a production-ready ETL architecture featuring automated alerting and a live visualization layer.

## 🚀 The Mission
Market volatility in the DRC (Kinshasa) impacts business operations daily. This project provides a robust, automated solution for tracking risk metrics and alerting stakeholders via encrypted SMTP when market swings exceed a 2% threshold.

## 🛠️ The Tech Stack
- **Orchestration:** Apache Airflow (Docker-based)
- **Database:** PostgreSQL (Time-series data storage)
- **Visualization:** Streamlit (Real-time, mobile-responsive dashboard)
- **Language:** Python (Pandas, SQLAlchemy, SMTP)
- **Infrastructure:** AWS EC2 (Ubuntu 24.04)

## 📊 Pipeline Architecture & Data Strategy
1. **Ingestion (Synthetic Strategy):** To demonstrate high-volatility alerting without incurring high-frequency API costs, the ingestion layer currently utilizes a **Synthetic Data Generator**. This mimics the 7-day volatility patterns of the Congolese Franc.
2. **Transformation:** Pandas performs windowed calculations (Moving Averages and Daily Volatility %).
3. **Storage:** Structured data is pushed to a secure PostgreSQL vault.
4. **Alerting:** Logic-based triggers identify high-volatility events and push high-priority email notifications.
5. **Dashboarding:** A live Streamlit app visualizes market trends for stakeholders.

## 📱 Live Demo
View the real-time analytics dashboard here: [http://3.145.21.193:8501](http://3.145.21.193:8501)

## 🏗️ How to Run
1. Clone the repo: `git clone https://github.com/ChristianDanE/jua-forex-watchdog.git`
2. Create a `.env` file with your `DB_PASSWORD` and `GMAIL_PASSWORD`.
3. Run `docker-compose up -d` to launch the database and Airflow.
