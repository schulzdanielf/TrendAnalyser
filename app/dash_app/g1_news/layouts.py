# app/dash_pages/google_trends_layout.py

from dash import dcc, html
import plotly.express as px
from app.database import fetch_data_from_g1
import pandas as pd


def create_layout():
    """Cria o layout da aplicação Dash para Google Trends."""
    # Buscar os dados das notícias
    df = fetch_data_from_g1()

    # convert date to day
    df["date"] = df["date"].dt.date

    # filter last 7 days
    df = df[df["date"] >= df["date"].max() - pd.Timedelta(days=7)]

    # Agrupar por candidato e data e somar o número de notícias
    df_grouped = (
        df.groupby(["candidate", "date"]).agg({"num_noticias": "sum"}).reset_index()
    )

    # Gráfico de Linhas
    fig_line = px.line(
        df_grouped,
        x="date",
        y="num_noticias",
        color="candidate",
        title="Número de Notícias por Candidato ao Longo do Tempo",
    )

    # Gráfico de Barras Empilhadas
    fig_bar = px.bar(
        df_grouped,
        x="date",
        y="num_noticias",
        color="candidate",
        title="Distribuição de Notícias por Candidato",
        labels={"num_noticias": "Número de Notícias"},
    )

    # Gráfico de Pizza
    # Somar o número total de notícias por candidato
    df_total_news = (
        df_grouped.groupby("candidate").agg({"num_noticias": "sum"}).reset_index()
    )
    fig_pie = px.pie(
        df_total_news,
        names="candidate",
        values="num_noticias",
        title="Participação Total de Notícias por Candidato",
    )

    # Histograma de Número de Notícias
    fig_hist = px.histogram(
        df_grouped,
        x="num_noticias",
        color="candidate",
        title="Frequência do Número de Notícias por Intervalos",
        labels={"num_noticias": "Número de Notícias"},
        nbins=20,
    )

    # Box Plot de Número de Notícias
    fig_box = px.box(
        df_grouped,
        x="candidate",
        y="num_noticias",
        title="Dispersão do Número de Notícias por Candidato",
    )

    layout = html.Div(
        className="dash-container",
        children=[
            html.H1(children="Análise do Número de Notícias dos Candidatos"),
            # Gráfico de Linhas
            dcc.Graph(
                id="line-graph",
                figure=fig_line,
            ),
            # Gráfico de Barras Empilhadas
            dcc.Graph(
                id="bar-graph",
                figure=fig_bar,
            ),
            # Gráfico de Pizza
            dcc.Graph(
                id="pie-graph",
                figure=fig_pie,
            ),
            # Histograma
            dcc.Graph(
                id="histogram",
                figure=fig_hist,
            ),
            # Box Plot
            dcc.Graph(
                id="box-plot",
                figure=fig_box,
            ),
        ],
    )

    return layout
