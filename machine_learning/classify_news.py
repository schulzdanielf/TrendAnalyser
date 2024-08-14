import psycopg2
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Função para conectar ao banco de dados
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


# Função para buscar dados do banco
def fetch_data_from_db():
    """Obtém dados do banco de dados."""
    conn = connect_to_database()
    if conn:
        df = pd.read_sql(
            "SELECT term, candidate, interest, date FROM trends_data WHERE date >= NOW() - INTERVAL '10 day'",
            conn,
        )
        conn.close()
        return df
    print("Não foi possível conectar ao banco de dados.")
    return pd.DataFrame()


# Função para análise de sentimentos
def analyze_sentiments(df):
    """Realiza a análise de sentimentos nos dados coletados."""
    analyzer = SentimentIntensityAnalyzer()
    df["sentiment"] = df["term"].apply(
        lambda x: analyzer.polarity_scores(x)["compound"]
    )
    return df


# Função para modelagem de tópicos
def topic_modeling(df, n_topics=5):
    """Realiza a modelagem de tópicos nos termos coletados."""
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
    dtm = vectorizer.fit_transform(df["term"])
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(dtm)

    topics = {}
    for index, topic in enumerate(lda.components_):
        topics[f"Topic {index}"] = [
            vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]
        ]

    return topics


# Função principal de processamento
def main():
    df = fetch_data_from_db()
    if not df.empty:
        df_with_sentiments = analyze_sentiments(df)
        print("Análise de Sentimentos Realizada:")
        print(df_with_sentiments.head())

        topics = topic_modeling(df)
        print("Modelagem de Tópicos Realizada:")
        for topic, words in topics.items():
            print(f"{topic}: {', '.join(words)}")
    else:
        print("Nenhum dado foi recuperado do banco de dados.")


if __name__ == "__main__":
    main()
