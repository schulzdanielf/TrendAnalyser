from flask import Flask, render_template
import psycopg2

# Configurações de conexão
DATABASE = {
    'host': 'db',  # Nome do serviço Docker
    'database': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'port': 5432,
}

def connect_to_database():
    try:
        conn = psycopg2.connect(**DATABASE)
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Cria a aplicação Flask
server = Flask(__name__)

# Configuração do aplicativo Dash
# (mantenha a configuração atual do Dash)

@server.route('/')
def index():
    # Exemplo de consulta ao banco de dados
    conn = connect_to_database()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('index.html', db_time=result[0])
    return "Could not connect to the database"

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)
