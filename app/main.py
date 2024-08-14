# app/main.py

from flask import Flask, render_template
from .database import connect_to_database
from .dash_app.google_trends import create_google_dash
from .dash_app.g1_news import create_g1_dash

# Inicializar o servidor Flask
server = Flask(__name__)


@server.route("/")
def index():
    """Rota da página inicial."""
    conn = connect_to_database()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return render_template("index.html", db_time=result[0])
    return "Não foi possível conectar ao banco de dados"


# Inicializar a aplicação Dash na rota /google-trends/
google_dash = create_google_dash(server)

# Inicializar uma segunda aplicação Dash na rota /g1-news/
g1_dash = create_g1_dash(server)

if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=5000)
