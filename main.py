from src.db import source_session
from src.models.source import Province

def main():
    with source_session() as db:
        for p in db.query(Province).all():
            print(p.ProvinceCode, p.ProvinceName)


if __name__ == "__main__":
    main()
