import streamlit as st
from arquivo_logica import MEI_Calculadora



##############################
# Inicialização de session_state - Serve para garantir que o aplicativo sempre tenha as variaveis definidas, mesmo antes de interagir. Para não dar erro
##############################


if "is_calculated" not in st.session_state:
    st.session_state["is_calculated"]        = False
    st.session_state["mei_calculator"]       = None
    st.session_state["parcela_isenta_val"]   = 0.0
    st.session_state["parcela_tributavel_val"]= 0.0
    st.session_state["resultado_final"]      = (False, "")


##############################
# Inicialização do estado de sessão - Essas funções são para formatar os valores no padrão brasileiro.
##############################
def converter_valor(valor_str):
    """
    Converte, por exemplo, "9.000,00" para 9000.00 (float).
    """
    valor_normalizado = valor_str.replace(".", "").replace(",", ".")
    try:
        return float(valor_normalizado)
    except ValueError:
        return None

def formatar_para_brasileiro(num: float) -> str:
    """
    Recebe 7200.0 e retorna 'R$ 7.200,00'.
    """
    valor_em_ingles = f"{num:,.2f}"                   # ex.: "7,200.00"
    valor_em_brasil = valor_em_ingles.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {valor_em_brasil}"

##############################
# Layout Principal - Aqui é a configuração visual, começando com o titulo, texto informativo, e o menu interativo separado em colunas.
##############################
st.title("Calculadora MEI – Declaração de Imposto de Renda (IRPF)")
st.info("""Você é MEI e quer descobrir se precisa declarar o IRPF 🧮? \n  
Esta ferramenta foi criada **para Microempreendedores Individuais**  que **ainda não têm serviço 
contábil contratado**, tornando fácil verificar seus rendimentos do MEI.  No final, gere um **PDF** com 
instruções detalhadas para a sua declaração, caso seja necessário! """)

col1, col2, col3 = st.columns(3)
with col1:
    faturamento_txt = st.text_input(
        "Faturamento Anual (ex.: 9.000,00)", "0,00",
        help="Total faturado no ano (R$)."
    )
with col2:
    despesas_txt = st.text_input(
        "Despesas Anuais (ex.: 5.000,00)", "0,00",
        help="Informe despesas comprovadas e em nome da empresa, como contas de água, luz, telefone, compras de mercadorias, manutenção, salários e aluguel."
    )
with col3:
    tipo_atividade = st.selectbox(
        "Tipo de Atividade",
        [1, 2, 3],
        format_func=lambda x: {
            1: "Comércio/Indústria/Transporte de Carga (8%)",
            2: "Transporte de passageiros (16%)",
            3: "Prestação de Serviços (32%)"
        }[x]
    )


##############################
# 1) BOTÃO CALCULAR- Aqui começa a parte do calculo da aplicação.
##############################
if st.button("Calcular", key="btn_calc"):
    # 1.a) Converter inputs 
    faturamento_val = converter_valor(faturamento_txt)
    despesas_val    = converter_valor(despesas_txt)
    if faturamento_val is None:
        st.error("Formato de faturamento inválido. Use ex.: 9.000,00")
        st.stop()
    if despesas_val is None:
        st.error("Formato de despesas inválido. Use ex.: 5.000,00")
        st.stop()

    # 1.b) Instanciar classe e validar cada etapa
    mei_calc    = MEI_Calculadora(faturamento_val, despesas_val, tipo_atividade)
    valido_fat  = mei_calc.obter_faturamento()
    if not valido_fat[0]:
        st.error(f"Faturamento inválido: {valido_fat[1]}")
        st.stop()
    valido_desp = mei_calc.obter_despesas()
    if not valido_desp[0]:
        st.error(f"Despesas inválidas: {valido_desp[1]}")
        st.stop()
    valido_ati  = mei_calc.obter_atividade()
    if not valido_ati[0]:
        st.error(f"Tipo de atividade inválido: {valido_ati[1]}")
        st.stop()

    # 1.c) Cálculos leves
    parcela_isenta   = mei_calc.parcela_isenta()
    parcela_tributavel = mei_calc.parcela_tributavel()
    resultado_validacao = mei_calc.validacao_final()  # # (bool, mensagem)

    # 1.d) Guardar no session_state
    st.session_state["mei_calculator"]        = mei_calc
    st.session_state["parcela_isenta_val"]    = parcela_isenta
    st.session_state["parcela_tributavel_val"]= parcela_tributavel
    st.session_state["resultado_final"]       = resultado_validacao
    st.session_state["is_calculated"]         = True

##############################
# 2) EXIBIÇÃO DE RESULTADOS  
##############################
if st.session_state["is_calculated"]:
    # Formatar para BR
    isentar_br = formatar_para_brasileiro(st.session_state["parcela_isenta_val"])
    tributario_br = formatar_para_brasileiro(st.session_state["parcela_tributavel_val"])
    resultado_final    = st.session_state["resultado_final"]


    # Cards via Markdown+CSS
    st.markdown(f"""
    <style>
      .card-container {{ display:flex; gap:16px; justify-content:center; margin-top:24px; }}
      .card {{ flex:1; max-width:360px; background:#f0f2f6; border-radius:12px;
               padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.04); text-align:center; }}
      .isenta h2 {{ color:#0f5688; }} .tributavel h2 {{ color:#c53030; }}
      .status-card {{ background:#e8f2fc; border-radius:12px;
                      padding:16px; margin:24px auto; max-width:760px; text-align:center; }}
    </style>
    <div class="card-container">
      <div class="card isenta">
        <h4>Parcela Isenta</h4><h2>{isentar_br}</h2>
      </div>
      <div class="card tributavel">
        <h4>Parcela Tributável</h4><h2>{tributario_br}</h2>
      </div>
    </div>
    <div class="status-card"><strong>{resultado_final[1]}</strong></div>
    """, unsafe_allow_html=True)

# condição que indica se já pode gerar o PDF
pdf_disponivel = (
    st.session_state["is_calculated"] and
    st.session_state["resultado_final"][0]
)

st.download_button(
    label="📄 Baixar PDF de Instruções para Declaração",
    data=(
        st.session_state["mei_calculator"]
            .gerar_pdf_com_dados_e_imagens()
        if pdf_disponivel else b""
    ),
    file_name="Instrucoes_Declaracao_MEI.pdf",
    mime="application/pdf",
    key="btn_download",
    disabled=not pdf_disponivel
)


##############################
# 4) INFO COMPLEMENTAR
##############################
st.markdown("""
<style>
  .info-card {
    background:#f0f2f6;
    border-radius:12px;
    padding:16px;
    margin:32px auto;
    max-width:760px;
    line-height:1.5;
    font-size:15px;
  }
</style>
<div class="info-card">
  <p>🔍 Esta calculadora considera apenas os rendimentos obtidos como MEI.  
     Caso você tenha outras fontes de renda, é recomendável buscar orientação contábil.</p>

  <p>Mesmo com rendimento tributável reduzido, algumas situações ainda podem obrigar a declaração do Imposto de Renda:</p>
  <ul>
    <li>Recebimento de rendimentos isentos superiores a R$ 200.000,00</li>
    <li>Ter residido no Brasil em parte do ano de 2024</li>
    <li>Operações na bolsa de valores acima de R$ 40.000,00</li>
    <li>Receita bruta da atividade rural acima de R$ 153.199,50</li>
    <li>Posse de bens com valor total superior a R$ 800.000,00</li>
    <li>Venda de imóvel com isenção de imposto</li>
  </ul>
  <p>⚠️ Se alguma dessas situações se aplicar a você, é importante falar com um contador antes de finalizar sua declaração.</p>
  <p><strong>Contato:</strong> ALCONTÁBIL@gmail.com</p>
</div>
""", unsafe_allow_html=True) 