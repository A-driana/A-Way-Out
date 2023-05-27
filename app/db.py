from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings


Database_url = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
engine = create_engine(Database_url, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()
