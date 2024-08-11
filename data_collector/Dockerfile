# Use uma imagem Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /usr/src/app

# Copie os arquivos de dependência e instale-os
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie o script de coleta de dados
COPY collect_data.py .

# Execute o script de coleta de dados
CMD ["python", "collect_data.py"]
