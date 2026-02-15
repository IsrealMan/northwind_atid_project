import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Example:
# SERVER=localhost
# DB=northwind
# USER=sa
# PASSWORD=YourStrongPassword!
server = os.getenv("DB_SERVER", "localhost")
database = os.getenv("DB_NAME", "northwind")
user = os.getenv("DB_USER", "sa")
password = os.getenv("DB_PASSWORD", "YourStrongPassword!")

# ODBC Driver 18 is common; change if needed
conn_str = (
    f"mssql+pyodbc://{user}:{password}@{server}/{database}"
    f"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

engine = create_engine(conn_str, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
