from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import Config

# Warehouse (PostgreSQL)
warehouse_engine = create_engine(url=Config.WAREHOUSE_CONN_STRING)
WarehouseSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=warehouse_engine)
WarehouseBase = declarative_base()

# Source (MSSQL)
source_engine = create_engine(url=Config.SOURCE_CONN_STRING, echo=False)
SourceSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=source_engine)
SourceBase = declarative_base()

@contextmanager
def warehouse_session():
    db = WarehouseSessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def source_session():
    db = SourceSessionLocal()
    try:
        yield db
    finally:
        db.close()
