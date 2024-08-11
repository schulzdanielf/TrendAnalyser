from pytrends.request import TrendReq
import pandas as pd
import psycopg2
from datetime import datetime
import time

def connect_to_trends():
    """Estabelece conexão com o Google Trends."""
    return TrendReq(hl='pt-BR', tz=360)

def get_interest_over_time(pytrends, keywords, region='BR-SP'):
    """Obtém dados de interesse ao longo do tempo para uma lista de palavras-chave."""
    pytrends.build_payload(keywords, cat=0, timeframe='today 1-m', geo=region, gprop='')
    try:
        data = pytrends.interest_over_time()
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return pd.DataFrame()

    if data.empty:
        print("Nenhum dado disponível.")
        return pd.DataFrame()

    data = data.reset_index()
    df = pd.melt(data, id_vars=['date'], value_vars=keywords, var_name='term', value_name='interest')
    return df

def store_data(df, db_params):
    """Armazena os dados no banco de dados PostgreSQL."""
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Cria a tabela se não existir
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS trends_data (
        id SERIAL PRIMARY KEY,
        term VARCHAR(255),
        interest FLOAT,
        date TIMESTAMP
    )
    '''
    cursor.execute(create_table_query)

    # Apaga todos os dados
    cursor.execute("DELETE FROM trends_data")    

    # Insere os dados
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO trends_data (term, interest, date) VALUES (%s, %s, %s)",
            (row['term'], row['interest'], row['date'])
        )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Configurações de conexão com o banco de dados
    db_params = {
        'host': 'my_postgres',
        'database': 'mydatabase',
        'user': 'myuser',
        'password': 'mypassword',
        'port': 5432
    }
    while True:
        pytrends = connect_to_trends()
        keywords = ['Ricardo Nunes', 'Guilherme Boulos', 'Pablo Marçal', 'Tabata Amaral', 'Datena']
        
        df = get_interest_over_time(pytrends, keywords)
        if not df.empty:
            store_data(df, db_params)
        time.sleep(3600)  # Aguarda 1 hora