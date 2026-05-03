# Usa uma imagem leve de Python
FROM python:3.12-slim

# Instala dependências de sistema necessárias para drivers de banco e rede
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as bibliotecas (Cassandra Driver, PyMongo, python-dotenv, etc)
RUN pip install --no-cache-dir -r requirements.txt

# O comando padrão mantém o container vivo
CMD ["tail", "-f", "/dev/null"]