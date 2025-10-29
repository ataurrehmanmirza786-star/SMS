from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
