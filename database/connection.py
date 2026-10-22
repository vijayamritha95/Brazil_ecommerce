import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config.settings import DATABASE_URL

# configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=5, pool_pre_ping=True)


def test_database_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                logger.info("Database connection successful.")
                return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        return False


def get_engine():
    return engine
