# app/dash_app/__init__.py

import dash
from flask import Flask
from .layouts import create_layout
from .callbacks import register_callbacks


def create_g1_dash(server: Flask) -> dash.Dash:
    """Cria e configura a aplicação Dash."""
    dash_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname="/g1-news/",
        external_stylesheets=["../static/styles.css"],
    )

    # Configurar layout da aplicação Dash
    dash_app.layout = create_layout()

    # Registrar callbacks
    register_callbacks(dash_app)

    return dash_app
