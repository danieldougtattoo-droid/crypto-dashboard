import streamlit as st
import pandas as pd

from db import insert_price, get_all_prices 
from cripto_service import get_crypto_prices
from currency_service import get_usd_to_brl
from streamlit_autorefresh import st_autorefresh

#Configuração da página

st.set_page_config(page_title="Dashboard Cripto", layout="wide")

# Auto refresh a cada 30 segundos
st_autorefresh(interval=30000, key="auto_refresh")

st.caption("Valores em usd e conversão automática para BRL")

st.divider()

# Ações principais

AUTO_UPDATE = st.toggle("Atualizar automaticamente", value=False)

if AUTO_UPDATE:
    bitcoin, ethereum = get_crypto_prices()
    insert_price(bitcoin, ethereum)

if st.button("Atualizar Preços"):
    bitcoin, ethereum = get_crypto_prices()
    insert_price(bitcoin, ethereum)
    st.success("Preços atualizados com sucesso!")

# Dados principais

dados = get_all_prices()
if not dados:
    st.info("Nenhum dado encontrado")
    st.stop()

df = pd.DataFrame(dados)

#Remove registros invalidos

df = df.dropna(subset=["bitcoin", "ethereum"])
if df.empty:
    st.info("Ainda não há dados válidos")
    st.stop()

#Conversão para BRL

usd_to_brl = get_usd_to_brl()

df["bitcoin_brl"] = df["bitcoin"] * usd_to_brl
df["ethereum_brl"] = df["ethereum"] * usd_to_brl

#Resumo

ultimo = df.iloc[-1]
col1, col2 = st.columns(2)

col1.metric(
    label = "Bitcoin (BRL)",
    value = f"R$ {ultimo['bitcoin_brl']:.2f}",
    delta = f"R$ {ultimo['bitcoin_brl'] - df['bitcoin_brl'].iloc[-2]:.2f}",
)

col2.metric(
    label = "Ethereum (BRL)",
    value = f"R$ {ultimo['ethereum_brl']:.2f}",
    delta = f"R$ {ultimo['ethereum_brl'] - df['ethereum_brl'].iloc[-2]:.2f}",
)

st.divider()

df_chart = (
    df.sort_values(by="updated_at")
    .query("bitcoin_brl > 0 and ethereum_brl > 0")
)

# Gráfico de preços

st.subheader("Evolução de Preços (BRL)")

#Ordenação por tempo
df_chart = df.sort_values(by="updated_at").dropna(subset=["bitcoin_brl", "ethereum_brl"])

#Converte data para timestamp
df_chart["updated_at"] = pd.to_datetime(df_chart["updated_at"])

col1, space, col2 = st.columns([5, 1, 5])

with col1:
    st.markdown("<h3 style='text-align: center;'>Bitcoin (BRL)</h3>", unsafe_allow_html=True)
    st.line_chart(df_chart.set_index("updated_at")["bitcoin_brl"])

with col2:
    st.markdown("<h3 style='text-align: center;'>Ethereum (BRL)</h3>", unsafe_allow_html=True)
    st.line_chart(df_chart.set_index("updated_at")["ethereum_brl"])

#Historico de preços

st.subheader("Historico de Preços")

df_view = df[[
    "bitcoin", "bitcoin_brl", "ethereum", "ethereum_brl",
    "updated_at"
]].sort_values(by="updated_at", ascending=False)

df_view.columns = [
    "Bitcoin (USD)", "Bitcoin (BRL)",
    "Ethereum (USD)", "Ethereum (BRL)",
    "Atualizado em"
]
st.dataframe(df_view)

#Gráfico de preços
