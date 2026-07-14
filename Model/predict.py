import streamlit as st

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.inference import CreditRiskModel
from app.preprocess import build_features
from app.de_para import ESTADO_CIVIL, ESCOLARIDADE, TIPO_RENDA

st.set_page_config(
    page_title="Sistema Inteligente de Limite de Crédito",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Sistema Inteligente de Limite de Crédito")
st.caption("Previsão da Probabilidade de Default (PD)")

@st.cache_resource
def load_model():
    return CreditRiskModel()

modelo = load_model()

# =========================
# Dados do Cliente
# =========================

st.header("📝 Dados do Cliente")

# -----------------------------------------------------
# Dados Pessoais
# -----------------------------------------------------
st.subheader("👤 Dados Pessoais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    sexo = st.selectbox(
        "Sexo",
        ["Masculino", "Feminino"]
    )

with col2:
    idade = st.number_input(
        "Idade",
        min_value=18,
        max_value=100,
        value=35
    )

with col3:
    estado_civil = st.selectbox(
        "Estado Civil",
        sorted(list(ESTADO_CIVIL.keys())),
    )

with col4:
    escolaridade = st.selectbox(
        "Escolaridade",
        sorted(list(ESCOLARIDADE.keys()))
    )

st.divider()

# -----------------------------------------------------
# Situação Familiar
# -----------------------------------------------------
st.subheader("👨‍👩‍👧 Situação Familiar")

col1, col2 = st.columns(2)

with col1:
    filhos = st.number_input(
        "Número de Filhos",
        min_value=0,
        value=0,
    )

with col2:
    membros_familia = st.number_input(
        "Quantidade de Membros da Família",
        min_value=1,
        value=1,
    )

st.divider()

# -----------------------------------------------------
# Situação Profissional
# -----------------------------------------------------
st.subheader("💼 Situação Profissional")

col1, col2 = st.columns(2)

with col1:
    tipo_renda = st.selectbox(
        "Tipo de Renda",
        sorted(list(TIPO_RENDA.keys())),
    )

with col2:
    anos_emprego = st.number_input(
        "Tempo de Emprego (anos)",
        min_value=0,
        max_value=50,
        value=8,
    )

st.divider()

# -----------------------------------------------------
# Informações Financeiras
# -----------------------------------------------------
st.subheader("💰 Informações Financeiras")

col1, col2, col3 = st.columns(3)

with col1:
    renda = st.number_input(
        "Renda Anual (R$)",
        min_value=0.0,
        value=120000.0,
        step=1000.0,
    )

with col2:
    valor_credito = st.number_input(
        "Valor do Empréstimo (R$)",
        min_value=0.0,
        value=120000.0,
        step=1000.0,
    )

with col3:
    valor_parcela = st.number_input(
        "Valor Total das Parcelas (R$)",
        min_value=0.0,
        value=120000.0,
        step=1000.0,
    )

st.divider()

# -----------------------------------------------------
# Patrimônio
# -----------------------------------------------------
st.subheader("🏠 Patrimônio")

col1, col2 = st.columns(2)

with col1:
    carro = st.selectbox(
        "Possui carro?",
        ["Não", "Sim"],
    )

with col2:
    imovel = st.selectbox(
        "Possui imóvel?",
        ["Não", "Sim"],
    )

# =========================
# Predição
# =========================

if st.button("🔍 Calcular risco", use_container_width=True):
    features = build_features(
        renda=renda,
        valor_credito=valor_credito,
        valor_bem=0,
        valor_parcela=valor_parcela,
        idade=idade,
        anos_emprego=anos_emprego,
        filhos=filhos,
        membros_familia=1,
        sexo=sexo,
        possui_carro=carro == "Sim",
        possui_imovel=imovel == "Sim",
        tipo_renda=tipo_renda,
        estado_civil=estado_civil,
        escolaridade=escolaridade,
    )

    resultado = modelo.predict(features)

    st.divider()
    st.subheader("Resultado da Análise")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Renda Anual",
        f"R$ {renda:,.2f}",
    )

    c2.metric(
        "⚠️ Probabilidade de Default",
        f"{resultado['pd']:.2%}",
    )

    c3.metric(
        "📈 Faixa de Risco",
        resultado["faixa"],
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "🏦 Decisão",
        resultado["decisao"],
    )

    c5.metric(
        "💳 Limite Recomendado",
        f"R$ {resultado['limite']:,.2f}",
    )

    c6.metric(
        "📅 Prazo",
        f"{resultado['prazo']} meses",
    )