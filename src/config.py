import environ
import os

env = environ.Env(
    DEBUG=(bool, False),
    _AIRFLOW_DB_MIGRATE=(bool, False),
    ACCEPT_EULA=(str, 'Y')
)

BASE_DIR = environ.Path(__file__) - 2

env_file_path = str(BASE_DIR.path('.env'))
if os.path.exists(env_file_path):
    env.read_env(env_file_path)
else:
    print(f".env file not found at {env_file_path}, proceeding without it.")

class Config:
    SOURCE_CONN_STRING = env.str("SOURCE_CONN_STRING")
    WAREHOUSE_CONN_STRING = env.str("WAREHOUSE_CONN_STRING")
    SUPERSET_CONN_STRING = env.str("SQLALCHEMY_DATABASE_URI")
    AIRFLOW_CONN_STRING = env.str("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")