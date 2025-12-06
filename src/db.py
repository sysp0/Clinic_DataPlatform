from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import Config

# Warehouse (PostgreSQL)
warehouse_engine = create_engine(url=Config.WAREHOUSE_CONN_STRING)
WarehouseSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=warehouse_engine)
WarehouseBase: Any = declarative_base()

# Source (MSSQL)
source_engine = create_engine(url=Config.SOURCE_CONN_STRING, echo=False)
SourceSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=source_engine)
SourceBase: Any = declarative_base()

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

def init_warehouse_db():
    import src.models.warehouse  # noqa: F401
    print("Models found in metadata:", WarehouseBase.metadata.tables.keys())
    WarehouseBase.metadata.create_all(bind=warehouse_engine)
    print("Warehouse tables created successfully.")