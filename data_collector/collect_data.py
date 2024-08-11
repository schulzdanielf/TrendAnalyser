# collect_data.py

from pytrends.request import TrendReq
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import time

def connect_to_trends():
    """Estabelece conexão com o Google Trends."""
    return TrendReq(hl='pt-BR', tz=360)

def connect_to_db():
    """Conecta ao banco de dados PostgreSQL."""
    return psycopg2.connect(
        host="my_postgres",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )

def create_table():
    """Cria a tabela trends_data se ela não existir."""
    # Conectar ao banco de dados
    conn = psycopg2.connect(
        host="my_postgres",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    
    # Criar um cursor
    cur = conn.cursor()
    
    # Comando SQL para criar a tabela
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS trends_data (
        id SERIAL PRIMARY KEY,
        term VARCHAR(255),
        interest INTEGER,
        location VARCHAR(255)
    );
    '''
    
    # Executar o comando
    cur.execute(create_table_query)
    
    # Confirmar a transação
    conn.commit()
    
    # Fechar a conexão
    cur.close()
    conn.close()
    print("Tabela criada com sucesso.")

# Executar a função para criar a tabela
create_table()

def get_interest_by_city(pytrends, keywords, region='BR-SP'):
    """Obtém dados de interesse por cidade para uma lista de palavras-chave."""
    pytrends.build_payload(keywords, cat=0, timeframe='today 3-m', geo=region, gprop='')
    interest_by_region_df = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True, inc_geo_code=False)
    
    if 'São Paulo' in interest_by_region_df.index:
        sao_paulo_data = interest_by_region_df.loc['São Paulo']
        return sao_paulo_data.sort_values(ascending=False)
    else:
        print("Dados para a cidade de São Paulo não encontrados.")
        return pd.Series()

def insert_data_to_db(conn, data, keywords):
    """Insere os dados de interesse no banco de dados."""
    with conn.cursor() as cursor:
        sql = "INSERT INTO trends_data (term, interest, location) VALUES %s"
        values = [(keyword, interest, 'São Paulo') for keyword, interest in zip(keywords, data)]
        execute_values(cursor, sql, values)
    conn.commit()

def main():
    pytrends = connect_to_trends()
    conn = connect_to_db()

    try:
        # Definir a lista de palavras-chave de interesse
        keywords = ["tecnologia", "inovação", "startups", "inteligência artificial", "computação"]

        # Obter dados de interesse por cidade
        sao_paulo_interest = get_interest_by_city(pytrends, keywords)
        print("Interesse por termos de tecnologia na cidade de São Paulo:")
        print(sao_paulo_interest)

        # Inserir dados no banco de dados
        if not sao_paulo_interest.empty:
            insert_data_to_db(conn, sao_paulo_interest, keywords)

    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        main()
        time.sleep(600)
    
