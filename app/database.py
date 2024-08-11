# app/database.py

import psycopg2
import pandas as pd

DATABASE = {
    "host": "db",  # Nome do serviço Docker
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "port": 5432,
}


def connect_to_database():
    """Estabelece uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(**DATABASE)
        return conn
    except Exception as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None


def fetch_data_from_db():
    """Get data from the database."""
    conn = connect_to_database()
    if conn:
        df = pd.read_sql(
            "SELECT term, interest, date FROM trends_data WHERE date >= NOW() - INTERVAL '7 day'",
            conn,
        )
        conn.close()
        return df
    print("Não foi possível conectar ao banco de dados.")
    return pd.DataFrame()
