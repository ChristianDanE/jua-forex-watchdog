FROM python:3.11-slim

# Install system dependencies for Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install the "Big Three" your script needs
RUN pip install pandas sqlalchemy psycopg2-binary

WORKDIR /app
COPY . .

CMD ["python", "-u", "analytics.py"]