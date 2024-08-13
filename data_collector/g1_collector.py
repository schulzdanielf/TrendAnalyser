"""This module is responsible for scraping the G1 website."""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import database
from psycopg2 import errors
import time


# Configurar o Pandas para aceitar o comportamento futuro
pd.set_option("future.no_silent_downcasting", True)


def not_contains_query(query, title, description):
    """Verifica se a consulta não está no título ou descrição."""
    for word in query.lower().split(" "):
        if word in title.lower() or word in description.lower():
            return False
    print("Não contém a consulta: ", query, title, description)
    return True


def database_contains_link(link):
    """Verifica se o link da notícia já está no banco de dados."""
    conn = database.connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT link FROM g1_news WHERE link = %s", (link,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None


def fetch_g1_news(query, num_articles=5):
    """Obtém notícias do site G1 com base em uma consulta."""

    base_url = f'https://g1.globo.com/busca/?q={query.replace(" ", "+")}&order=recent&species=notícias'
    articles = []
    page = 1

    while len(articles) < num_articles:
        url = f"{base_url}&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erro ao acessar o site: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Encontre os blocos de notícia
        for item in soup.find_all("li", class_="widget widget--card widget--info"):
            title_tag = item.find("div", class_="widget--info__title")
            link_tag = item.find("a", href=True)
            date_tag = item.find("div", class_="widget--info__meta")
            description_tag = item.find("p", class_="widget--info__description")

            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = fetch_final_link(link_tag["href"])
                date = date_tag.get_text(strip=True) if date_tag else "Desconhecida"
                description = (
                    description_tag.get_text(strip=True)
                    if description_tag
                    else "Sem descrição"
                )

                # Se a consulta não estiver no título ou descrição, pule
                if not_contains_query(query, title, description):
                    print("Pulando: ", title)
                    continue

                # Se a notícia já foi coletada, pule
                if database_contains_link(link):
                    print("Notícia já coletada: ", title)
                    continue

                # Extrai o texto completo da notícia
                full_text = fetch_news_text(link)

                # Adiciona os dados ao resultado
                articles.append(
                    {
                        "title": title,
                        "link": link,
                        "date": date,
                        "description": description,
                        "full_text": full_text,
                    }
                )

                # Parar se já tiver o número desejado de artigos
                if len(articles) >= num_articles:
                    break

        # Avança para a próxima página
        page += 1

    articles_df = pd.DataFrame(articles)
    articles_df = ajusta_data(articles_df)

    articles_df["candidate"] = query

    return articles_df


def fetch_final_link(link):
    """Obtém o link final de uma notícia."""
    if not link.startswith("http"):
        link = f"https:{link}"
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Erro ao acessar o link da notícia: {response.status_code}")

    link_final = response.text.split('window.location.replace("')[1].split('");')[0]

    return link_final


def fetch_news_text(news_link):
    """Obtém o texto completo de uma notícia a partir do link."""
    if not news_link.startswith("http"):
        news_link = f"https:{news_link}"

    response = requests.get(news_link)

    if response.status_code != 200:
        print(f"Erro ao acessar o link da notícia: {response.status_code}")
        return "Texto não disponível"
    # salvar o html
    with open("g1.html", "w") as file:
        file.write(response.text)

    soup = BeautifulSoup(response.text, "html.parser")

    # Ajuste o seletor de acordo com a estrutura da página de notícia
    text_container = soup.find(
        "p", class_="content-text__container"
    )  # Exemplo de seletor
    full_text = ""
    if text_container:
        # For loop para pegar todos os p e a tag de texto
        for text in text_container:
            # concatenate the text
            full_text += text.get_text()
        return full_text
    else:
        return ""


def ajusta_data(df):
    """Ajusta o formato da data."""
    for i in range(len(df)):
        # try and except to handle if occurs an error and set the date to unknown
        last_date = datetime.now()
        try:
            if df["date"][i][:2] == "há":
                df["date"][i] = datetime.now() - timedelta(days=int(df["date"][i][3]))
                last_date = df["date"][i]
            else:
                # convert this format 05/08/2024 14h54 to datetime
                df["date"][i] = datetime.strptime(df["date"][i], "%d/%m/%Y %Hh%M")
                last_date = df["date"][i]
        except Exception:
            df["date"][i] = last_date
    return df


def store_news(articles):
    """Armazena os dados das notícias no banco de dados PostgreSQL."""
    conn = database.connect_to_database()
    cursor = conn.cursor()

    for index, row in articles.iterrows():
        title = row["title"]
        link = row["link"]
        date = row["date"]
        description = row["description"]
        full_text = row["full_text"]
        candidate = row["candidate"]

        try:
            cursor.execute(
                "INSERT INTO g1_news (title, link, date, description, text, candidate) VALUES (%s, %s, %s, %s, %s, %s)",
                (title, link, date, description, full_text, candidate),
            )
        except Exception as e:
            print("Erro ao inserir dados:", e)

    conn.commit()
    cursor.close()
    conn.close()


def collect_news_from_g1():
    """Coleta notícias do G1 e armazena no banco de dados."""
    candidatos = [
        "Tabata Amaral",
        "Guilherme Boulos",
        "Ricardo Nunes",
        "Pablo Marçal",
        "Luiz Datena",
    ]
    for candidato in candidatos:
        print(f"Coletando notícias para: {candidato}")
        articles = fetch_g1_news(candidato, num_articles=20)
        store_news(articles)
        # sleep for 10 seconds
        time.sleep(5)
