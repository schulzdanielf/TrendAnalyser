from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from app.database import fetch_data_from_db


def create_layout():
    """Cria o layout da aplicação Dash."""
    df = fetch_data_from_db()

    # Group by candidate and date and sum interest
    df_grouped = (
        df.groupby(["candidate", "date"]).agg({"interest": "sum"}).reset_index()
    )

    # Gráfico de Linhas
    fig_line = px.line(
        df_grouped,
        x="date",
        y="interest",
        color="candidate",
        title="Interesse por Candidato ao Longo do Tempo",
    )

    # Gráfico de Barras Empilhadas
    fig_bar = px.bar(
        df_grouped,
        x="date",
        y="interest",
        color="candidate",
        title="Distribuição de Interesse por Candidato",
        labels={"interest": "Interesse"},
    )

    # Gráfico de Pizza
    # Somar o interesse total por candidato
    df_total_interest = (
        df_grouped.groupby("candidate").agg({"interest": "sum"}).reset_index()
    )
    fig_pie = px.pie(
        df_total_interest,
        names="candidate",
        values="interest",
        title="Participação Total de Interesse por Candidato",
    )

    # Histograma de Interesse
    fig_hist = px.histogram(
        df_grouped,
        x="interest",
        color="candidate",
        title="Frequência de Interesse por Intervalos",
        labels={"interest": "Interesse"},
        nbins=20,
    )

    # Box Plot de Interesse
    fig_box = px.box(
        df_grouped,
        x="candidate",
        y="interest",
        title="Dispersão do Interesse por Candidato",
    )

    layout = html.Div(
        className="dash-container",
        children=[
            html.H1(children="Análise de Tendências de Pesquisa dos Candidatos"),
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
