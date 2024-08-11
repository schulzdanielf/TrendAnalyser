# app/dash_app/layouts.py

from dash import dcc, html
import plotly.express as px
from ..database import fetch_data_from_db


def create_layout():
    """Cria o layout da aplicação Dash."""
    df = fetch_data_from_db()
    print("Tamanho DF", len(df))
    layout = html.Div(
        children=[
            html.H1(children="Tendências de Pesquisa em São Paulo"),
            dcc.Graph(
                id="example-graph",
                figure=px.line(
                    df,
                    x="date",
                    y="interest",
                    color="term",
                    title="Interesse por Termo ao Longo do Tempo",
                ),
            ),
        ]
    )

    return layout
