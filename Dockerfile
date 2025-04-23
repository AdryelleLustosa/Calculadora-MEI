# Use uma imagem leve do Python
FROM python:3.10-slim

# Evita arquivos .pyc e força saída de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Copia e instala dependências
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 2) Copia todo o código da aplicação
COPY . .

EXPOSE 8501

# 3) Inicia o Streamlit
CMD ["streamlit", "run", "app_streamlit.py", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0"]
