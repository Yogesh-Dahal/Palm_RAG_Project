import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

url = os.getenv("DATABASE_URL")

engine = create_engine(url)
session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Create all tables
def init_db():
    # First, ensure the schema exists
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS datas"))
        conn.commit()
    
    # Then create all tables
    Base.metadata.create_all(bind=engine)
    print("Database and tables initialized successfully")
