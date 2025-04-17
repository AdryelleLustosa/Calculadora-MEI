import streamlit as st
import pandas as pd
import numpy as np
from arquivo_logica import MEI_Calculadora
from fpdf import FPDF


import streamlit as st
from arquivo_logica import MEI_Calculadora

##############################
# Função para converter string do formato brasileiro para float
##############################
def converter_valor(valor_str):
    """
    Converte, por exemplo, "9.000,00" para 9000.00 (float).
    """
    valor_limpo = valor_str.replace(".", "").replace(",", ".")
    try:
        return float(valor_limpo)
    except ValueError:
        return None

##############################
# Função para exibir float no formato brasileiro
##############################
def formatar_para_brasileiro(num: float) -> str:
    """
    Recebe, por exemplo, 7200.0 e retorna 'R$ 7.200,00'.
    """
    # Primeiro obtemos o formato em US (ex.: "7,200.00")
    str_us = f"{num:,.2f}"
    # Troca ',' por 'X', '.' por ',', e 'X' por '.'
    str_br = str_us.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {str_br}"

##############################
# Layout Principal
##############################
st.title("Calculadora MEI – Declaração de Imposto de Renda")
st.info("Preencha os dados abaixo para saber se você, MEI, precisa declarar o IRPF.")


# Inputs em 3 colunas
col1, col2, col3 = st.columns(3)

with col1:
    faturamento_texto = st.text_input(
    "Faturamento Anual (ex.: 9.000,00)", 
    value="0,00",
    help= "Todos os valores recebidos pela empresa em 2024")
                                                                          
with col2:
    despesas_texto = st.text_input(
        "Despesas Anuais (ex.: 5.000,00)",
        value="0,00",
        help="Exemplos: Pró-labore, DAS, Mercadorias, Aluguel, Água, Luz e Tel. Só serão dedutíveis despesas comprovadas (nota fiscal e/ou recibo) que constem no CNPJ da empresa."
    )
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

# Botão para processar os dados
if st.button("Calcular"):
    # Converte os valores inseridos para float
    faturamento = converter_valor(faturamento_texto)
    despesas = converter_valor(despesas_texto)
    
    if faturamento is None:
        st.error("Formato de faturamento inválido. Use ex.: 9.000,00")
        st.stop()
    if despesas is None:
        st.error("Formato de despesas inválido. Use ex.: 5.000,00")
        st.stop()
    
    # Cria o objeto da lógica MEI_Calculadora
    calc = MEI_Calculadora(faturamento, despesas, tipo_atividade)
    
    # Validações
    res_fat = calc.obter_faturamento()
    if res_fat is None or not res_fat[0]:
        st.error(f"Faturamento inválido: {res_fat[1] if res_fat else 'Erro na conversão.'}")
        st.stop()
    
    res_desc = calc.obter_despesas()
    if res_desc is None or not res_desc[0]:
        st.error(f"Despesas inválidas: {res_desc[1] if res_desc else 'Erro na conversão.'}")
        st.stop()
    
    res_ativ = calc.obter_atividade()
    if res_ativ is None or not res_ativ[0]:
        st.error(f"Tipo de atividade inválido: {res_ativ[1] if res_ativ else 'Erro na conversão.'}")
        st.stop()
    
    # Se todas as validações estiverem OK, efetua os cálculos
    valor_isento = calc.parcela_isenta()           # Retorna o valor da parcela isenta
    valor_tributavel = calc.parcela_tributavel()     # Retorna o valor da parcela tributável
    res_final = calc.validação_final()             # Retorna (bool, mensagem final)
    
    # Formata os valores para o padrão brasileiro
    valor_isento_br = formatar_para_brasileiro(valor_isento)
    valor_tributavel_br = formatar_para_brasileiro(valor_tributavel)
    
       # Exibe os resultados em "cards" lado a lado com espaçamento
    st.markdown(f"""
<style>
  /* Container geral dos cards – gap e margem reduzidos ao mínimo */
  .card-container {{
    display: flex;
    gap: 6px;            /* antes 10px */
    margin: 6px 0;       /* antes 10px 0 */
    justify-content: center;
  }}

  /* Card base – padding super enxuto */
  .card {{
    flex: 1;
    max-width: 360px;
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 8px;        /* antes 7px, pode até testar 6px */
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }}
  .card h4 {{
    margin-bottom: 8px;  /* antes maior */
    font-size: 1.0rem;
  }}
  .card h2 {{
    margin: 0;
    font-size: 1.8rem;   /* um pouco menor */
  }}

  /* Status card – margem e padding mínimas */
  .status-card {{
    background-color: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 12px;
    padding: 8px;        /* antes 7px */
    margin: 8px auto;    /* antes 32px/16px */
    max-width: 740px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    text-align: center;
  }}
  .status-card h3 {{
    margin: 0;
    font-size: 1.2rem;   /* um pouco menor */
    line-height: 1.3;
  }}

  /* Info card – margem e padding mínimas */
  .info-card {{
    background-color: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    padding: 12px;       /* antes 7px */
    margin: 12px auto;   /* antes 48px/24px */
    max-width: 740px;
    font-size: 0.9rem;
    line-height: 1.4;
  }}
  .info-card ul {{
    padding-left: 16px;
    margin: 6px 0;
  }}
  .info-card li {{
    margin-bottom: 4px;
  }}
</style>

<div class="card-container">
  <div class="card isenta">
    <h4>Parcela Isenta</h4>
    <h2>{valor_isento_br}</h2>
  </div>
  <div class="card tributavel">
    <h4>Parcela Tributável</h4>
    <h2>{valor_tributavel_br}</h2>
  </div>
</div>

<div class="status-card">
  <h3>{res_final[1]}</h3>
</div>

<div class="info-card">
  <p>Esta calculadora considera apenas ganhos da atividade MEI. Para outras fontes de renda ou situações especiais, consulte um contador.</p>
  <p>Mesmo com baixo rendimento tributável, os seguintes fatores podem obrigar à declaração do IRPF:</p>
  <ul>
    <li>Rendimentos isentos acima de R$ 200.000,00</li>
    <li>Residência fiscal parcial no Brasil em 2024</li>
    <li>Operações na bolsa acima de R$ 40.000,00</li>
    <li>Receita rural bruta > R$ 153.199,50</li>
    <li>Bens cujo valor total ultrapasse R$ 800.000,00</li>
    <li>Venda de imóvel com isenção de IR</li>
  </ul>
  <p>Se “sim” em qualquer item acima, consulte um contador antes de finalizar sua declaração.</p>
</div>
""", unsafe_allow_html=True)
    
# import streamlit as st
# from fpdf import FPDF

# def limpar_texto(texto: str) -> str:
#     """
#     Remove ou substitui caracteres Unicode problemáticos para a codificação latin-1.
#     Exemplo: substitui en dash (–) e em dash (—) por traço (-) e substitui aspas inteligentes por aspas simples ou duplas.
#     """
#     # Substitui en dash (U+2013) e em dash (U+2014) por um traço simples
#     texto = texto.replace("\u2013", "-").replace("\u2014", "-")
#     # Substitui aspas “smart” por aspas duplas
#     texto = texto.replace("“", '"').replace("”", '"')
#     # Substitui aspas simples inteligentes por aspas simples
#     texto = texto.replace("’", "'")
#     return texto

# def gerar_pdf(conteudo: str) -> bytes:
#     """
#     Gera um PDF a partir do conteúdo fornecido e retorna os bytes do PDF,
#     limpando previamente os caracteres problemáticos.
#     """
#     # Limpa o texto para remover caracteres que não podem ser codificados
#     conteudo_limpo = limpar_texto(conteudo)
    
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, txt=conteudo_limpo)
    
#     # Converte o PDF para bytes utilizando latin-1 com errors="replace"
#     pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="replace")
#     return pdf_bytes

# # Interface do Streamlit para gerar e baixar o PDF
# st.title("Gerar PDF com Streamlit")
# st.write("Clique no botão abaixo para gerar e baixar o PDF.")

# # Conteúdo de exemplo para o PDF (pode incluir en dash, aspas inteligentes, etc.)
# conteudo_pdf = (
#     "Calculadora MEI – Declaração de Imposto de Renda\n\n"
#     "Este documento apresenta os resultados da Calculadora MEI – análise de faturamento, despesas, "
#     "e outros fatores. \n\n"
#     "Obs: Se o valor das despesas ultrapassar o faturamento, a validação mostrará erro – "
#     "confira os dados com atenção. – Use sempre o formato correto."
# )

# # Gera os bytes do PDF com o conteúdo limpo
# pdf_bytes = gerar_pdf(conteudo_pdf)

# # Botão de download do PDF
# st.download_button(
#     label="Baixar PDF",
#     data=pdf_bytes,
#     file_name="calculadora_mei.pdf",
#     mime="application/pdf"
# )
