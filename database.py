from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Define the Database Location
# 'sqlite:///...' tells SQLAlchemy to create a local file named url_shortener.db
DATABASE_URL = "sqlite:///./data/url_shortener.db"

# 2. Initialize the Engine
# 'check_same_thread=False' is a specific requirement for SQLite to work smoothly with FastAPI's async nature
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Establish Session and Base Configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 4. Define the URL Mapping Table Schema
class URLMapping(Base):
    __tablename__ = "url_mappings"

    # Auto-incrementing ID is the core driver for our Base62 encoder!
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    long_url = Column(String, nullable=False)
    
    # We index the short_code because lookups happen constantly when users click links
    short_code = Column(String, unique=True, index=True, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)


# 5. Helper Function to Get a Database Session
def get_db():
    """
    Creates a temporary database session for a single request,
    and safely closes it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Database Initializer ---
def init_db():
    """Creates the database file and tables if they don't exist."""
    print("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database setup complete.")

if __name__ == "__main__":
    # If you run this script directly, it will just create the empty database table for you
    init_db()