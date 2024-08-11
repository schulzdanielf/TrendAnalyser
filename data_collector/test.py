import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetch_g1_news(query, num_articles=5):
    """Obtém notícias do site G1 com base em uma consulta."""

    url = f'https://g1.globo.com/busca/?q={query}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erro ao acessar o site: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    # salvar o html
    # with open('g1.html', 'w') as file:
    #    file.write(response.text)   

    # Encontre os blocos de notícia
    for item in soup.find_all('li', class_='widget widget--card widget--info'):
        title_tag = item.find('div', class_='widget--info__title')
        link_tag = item.find('a', href=True)
        date_tag = item.find('div', class_='widget--info__meta')
        description_tag = item.find('p', class_='widget--info__description')
        
        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = fetch_final_link(link_tag['href'])
            date = date_tag.get_text(strip=True) if date_tag else 'Desconhecida'
            description = description_tag.get_text(strip=True) if description_tag else 'Sem descrição'
            
            # Extrai o texto completo da notícia
            full_text = fetch_news_text(link)
            
            # Adiciona os dados ao resultado
            articles.append({
                'title': title,
                'link': link,
                'date': date,
                'description': description,
                'full_text': full_text
            })

            # Parar se já tiver o número desejado de artigos
            if len(articles) >= num_articles:
                break
    
    return articles

def fetch_final_link(link):
    """Obtém o link final de uma notícia."""
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Erro ao acessar o link da notícia: {response.status_code}")
    
    link_final = response.text.split('window.location.replace("')[1].split('");')[0]

    print(f"Link final: {link_final}")

    return link_final


def fetch_news_text(news_link):
    """Obtém o texto completo de uma notícia a partir do link."""
    print(f"Obtendo texto da notícia: {news_link}")
    # A URL pode precisar ser ajustada se o link for relativo
    if not news_link.startswith('http'):
        news_link = f'https:{news_link}'
    
    response = requests.get(news_link)
    
    if response.status_code != 200:
        print(f"Erro ao acessar o link da notícia: {response.status_code}")
        return 'Texto não disponível'
    # salvar o html
    with open('g1.html', 'w') as file:
        file.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ajuste o seletor de acordo com a estrutura da página de notícia
    text_container = soup.find('p', class_=' content-text__container ')  # Exemplo de seletor
    if text_container:
        paragraphs = text_container.find_all('p')
        full_text = '\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
        return full_text
    else:
        return 'Texto não disponível'


def store_news(articles, db_params):
    """Armazena os dados das notícias no banco de dados PostgreSQL."""
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Cria a tabela se não existir
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS g1_news (
        id SERIAL PRIMARY KEY,
        title TEXT,
        link TEXT,
        date TEXT
    )
    '''
    cursor.execute(create_table_query)

    # Apaga todos os dados
    cursor.execute("DELETE FROM g1_news")

    # Insere os dados
    for article in articles:
        cursor.execute(
            "INSERT INTO g1_news (title, link, date) VALUES (%s, %s, %s)",
            (article['title'], article['link'], article['date'])
        )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Substitua pelos seus parâmetros de conexão
    db_params = {
        'host': 'my_postgres',
        'database': 'mydatabase',
        'user': 'myuser',
        'password': 'mypassword',
        'port': 5432
    }
    
    # Busca notícias relacionadas a "Tabata Amaral"
    query = 'Tabata'
    news_articles = fetch_g1_news(query, num_articles=1)
    
    print(f"Encontradas {len(news_articles)} notícias sobre {query}")

    # imprimir 3 noticías
    for article in news_articles[:3]:
        print("Título",article['title'])
        print()
        print("Link",article['link'])
        print()
        print("Data",article['date'])
        print()
        print("Descrição",article['description'])
        print()
        print("Texto",article['full_text'])        
        print()


