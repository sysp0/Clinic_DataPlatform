from sqlalchemy import text
import sys
from src.db import init_warehouse_db, warehouse_engine

def migrate():
    """Create all warehouse tables."""
    print("Running migrations...")
    init_warehouse_db()
    print("Done!")

def check_connections():
    """Test database connections."""
    print("Checking Warehouse DB connection...")
    try:
        with warehouse_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Warehouse DB: OK")
    except Exception as e:
        print(f"Warehouse DB: FAILED - {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py [migrate|check]")
        return
    
    command = sys.argv[1]
    
    if command == "migrate":
        migrate()
    elif command == "check":
        check_connections()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()