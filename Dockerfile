# Use uma imagem base leve com Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie apenas o requirements para aproveitar o cache do Docker
COPY requirements.txt .

# Instale dependências
RUN pip install --no-cache-dir -r requirements.txt

# Agora copie todo o restante do seu código
COPY . .

# Só para documentar a porta padrão
EXPOSE 8080

# ENTRYPOINT que chama o app.py, que lê $PORT e inicia o Streamlit
ENTRYPOINT ["python", "app.py"]

