from pytrends.request import TrendReq
import pandas as pd
import time
from google_collector import collect_data_from_google
from g1_collector import collect_news_from_g1

# Configurar o Pandas para aceitar o comportamento futuro
pd.set_option("future.no_silent_downcasting", True)


if __name__ == "__main__":
    while True:
        collect_data_from_google()
        collect_news_from_g1(1)
        time.sleep(3600)  # Aguarda 1 hora
