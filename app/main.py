from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html

# Cria a aplicação Flask
server = Flask(__name__)

# Configuração do aplicativo Dash
app_dash = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

# Layout do Dash
app_dash.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

# Rota padrão do Flask
@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)
