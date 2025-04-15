# Importando Bibliotecas Necessárias;
import streamlit as st
import pandas as pd
import numpy as np
from arquivo_logica import MEI_Calculadora


# Titulo e subtitulo do projeto
st.title("Calculadora MEI – Declaração de Imposto de Renda")
st.info("Preencha os dados abaixo para saber se você, MEI, precisa declarar o IR.")

# Esntradas do Usúario (Faturamento, Despesas e Atividade)
col1, col2, col3 = st.columns(3)
with col1:
    faturamento = st.number_input("Faturamento Anual (R$)", min_value=0.0, step=100.0, value=0.0)
with col2:
    despesas = st.number_input("Despesas Anuais (R$)", min_value=0.0, step=100.0, value=0.0)
with col3:
    tipo_atividade = st.selectbox(
        "Tipo de Atividade",
        options=[1, 2, 3],
        index=0,
        format_func=lambda x: {
            1: "Comércio, indústria e transporte de cargas (8%)",
            2: "Transporte de passageiros (16%)",
            3: "Prestação de serviços (32%)"
        }[x]
    )

