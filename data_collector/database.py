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
