from pytrends.request import TrendReq
import pandas as pd
import time
from google_collector import collect_data_from_google

# Configurar o Pandas para aceitar o comportamento futuro
pd.set_option('future.no_silent_downcasting', True)


if __name__ == "__main__":
    while True:
        collect_data_from_google()
        time.sleep(3600)  # Aguarda 1 hora
