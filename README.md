# TrendAnalyzer

Este projeto é uma aplicação Flask com Dash para visualização e análise de dados, que utiliza um banco de dados PostgreSQL para armazenar as informações e um serviço de coleta de dados.

## Estrutura do Projeto

- **web**: Serviço principal que executa a aplicação Flask/Dash.
- **db**: Serviço de banco de dados PostgreSQL.
- **data_collector**: Serviço responsável pela coleta de dados e inserção no banco de dados.

## Requisitos

- Docker e Docker Compose instalados na máquina.

## Como Executar

1. Clone este repositório:

    ```bash
    git clone https://github.com/schulzdanielf/TrendAnalyser.git
    cd TrendAnalyser
    ```

2. Construa e inicie os contêineres:

    ```bash
    docker-compose up --build
    ```

3. Acesse a aplicação web:

    Abra o navegador e acesse `http://localhost:8000`.

## Serviços

### Web

- Porta: 8000 (mapeada para a porta 5000 do Flask).
- Container: `flask_dash_app`
- Descrição: Executa a aplicação Flask/Dash.

### DB

- Porta: 5432
- Container: `my_postgres`
- Descrição: Banco de dados PostgreSQL.
- Variáveis de Ambiente:
  - `POSTGRES_USER`: Usuário do banco de dados (padrão: `myuser`).
  - `POSTGRES_PASSWORD`: Senha do banco de dados (padrão: `mypassword`).
  - `POSTGRES_DB`: Nome do banco de dados (padrão: `mydatabase`).

### Data Collector

- Container: `data_collector`
- Descrição: Serviço responsável pela coleta de dados e inserção no banco de dados.

## Volumes

- **db_data**: Armazena os dados persistentes do PostgreSQL.

## Parando os Serviços

Para parar os serviços, execute:

```bash
docker-compose down
```

## Limpeza

Para remover os volumes persistentes, use o comando:

```bash
docker-compose down --volumes
```

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.
