from pytrends.request import TrendReq
import pandas as pd
import psycopg2

# Configurar o Pandas para aceitar o comportamento futuro
pd.set_option('future.no_silent_downcasting', True)

# Configurações de conexão com o banco de dados
db_params = {
    'host': 'my_postgres',
    'database': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'port': 5432
}

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
        date TIMESTAMP,
        candidate VARCHAR(255)
    )
    '''
    cursor.execute(create_table_query)

    # Apaga todos os dados
    cursor.execute("DELETE FROM trends_data")

    # Insere os dados
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO trends_data (term, interest, date, candidate) VALUES (%s, %s, %s, %s)",
            (row['term'], row['interest'], row['date'], row['candidate'])
        )

    conn.commit()
    cursor.close()
    conn.close()

def collect_data_from_google():
    """Coleta dados do Google Trends e armazena no banco de dados."""
    pytrends = connect_to_trends()
    # Lista de candidatos com variantes
    candidates = {
        'Ricardo Nunes': ['Ricardo Nunes', 'Ricardo N.', 'Nunes'],
        'Guilherme Boulos': ['Guilherme Boulos', 'Guilherme B.', 'Boulos'],
        'Pablo Marçal': ['Pablo Marçal', 'Pablo M.', 'Marçal'],
        'Tabata Amaral': ['Tabata Amaral', 'Tabata A.', 'Amaral'],
        'Datena': ['Datena', 'José Luiz Datena', 'José Datena']
    }

    # Conectar ao banco de dados
    conn = psycopg2.connect(
        host="my_postgres",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    # Cria um DataFrame vazio para armazenar todos os dados
    all_data = pd.DataFrame()

    for candidate, variations in candidates.items():
        print(f"Coletando dados para: {candidate}")
        df = get_interest_over_time(pytrends, variations)

        # Adiciona coluna de variantes e a data atual
        df['candidate'] = candidate

        # Adiciona os dados ao DataFrame geral
        all_data = pd.concat([all_data, df], ignore_index=True)

    conn.close()

    if not all_data.empty:
        store_data(all_data, db_params)