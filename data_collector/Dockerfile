# Use uma imagem Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /usr/src/app

# Copie os arquivos de dependência e instale-os
COPY . . 
RUN pip install --no-cache-dir -r requirements.txt

# Execute o script de coleta de dados
CMD ["python", "-m", "collect_data"]
