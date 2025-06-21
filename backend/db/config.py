import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_SERVER, DB_NAME]):
    raise ValueError("Faltan variables de entorno para la base de datos.")

ODBC_DRIVER_NAME = "ODBC Driver 17 for SQL Server"

odbc_connection_string = (
    f"DRIVER={{{ODBC_DRIVER_NAME}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"Trusted_Connection=yes;"
)

DATABASE_URL = f"mssql+aioodbc:///?odbc_connect={quote_plus(odbc_connection_string)}"