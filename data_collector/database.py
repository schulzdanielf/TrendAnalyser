"""This module contains the database class for the data collector."""

import psycopg2


def connect_to_database():
    """Estabelece uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host="db", database="mydatabase", user="myuser", password="mypassword"
        )
        return conn
    except Exception as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None


def create_table():
    """Cria a tabela no banco de dados."""
    conn = connect_to_database()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS g1_news (
        id SERIAL PRIMARY KEY,
        link TEXT UNIQUE,
        title TEXT,
        date TIMESTAMP,
        text TEXT,
        candidate TEXT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
