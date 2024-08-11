# app/dash_app/layouts.py

from dash import dcc, html
import plotly.express as px
from ..database import fetch_data_from_db


def create_layout():
    """Define o layout da aplicação Dash."""
    data = fetch_data_from_db()
    fig = px.bar(data, x="term", y="interest", title="Interesse por Termo")

    layout = html.Div(
        children=[
            html.H1(children="Tendências de Pesquisa em São Paulo"),
            dcc.Graph(id="example-graph", figure=fig),
        ]
    )
    return layout
