import asyncio
import time
import streamlit as st
import pandas as pd
from datetime import datetime
from libs.connect_data import get_data
from libs.config import leituras

# Configuração inicial
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        .block-container { padding: 1rem 0; margin-bottom: 1rem; }
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] { min-height: 100%; }
        #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inicializar session state
st.session_state.setdefault("last_update", time.time())
st.session_state.setdefault("resultados_flat", [])
st.session_state.setdefault("initialized", False)
st.session_state.setdefault("metric_placeholders", {})

async def processar_usina(usina, dados):
    ip, porta, clps, unidade = dados["ip"], dados["port"], dados["CLPS"], dados["table"]
    resultados = []
    for data_key, data_value in clps.items():
        resp, time_pass = await get_data(ip, porta, data_value, "leituras", unidade)
        if resp is not None and not resp.empty:
            resultados.append((usina, data_key, resp, time_pass))
    return resultados

async def coletar_dados():
    tasks = [processar_usina(usina, dados) for usina, dados in leituras.items()]
    return [item for sublist in await asyncio.gather(*tasks) for item in sublist]

def inicializar_interface(resultados):
    if not resultados:
        st.warning("Nenhum dado disponível para exibição.")
        return
    with st.container():
        cols = st.columns(len(resultados))
        for idx, (usina, device, leituras_resp, _) in enumerate(resultados):
            with cols[idx]:
                st.write(f"Usina: {usina}-{device}")
                placeholders = [(valor, st.empty()) for valor in leituras_resp.index]
                placeholders.append(("time", st.empty()))
                st.session_state.metric_placeholders[(usina, device)] = placeholders
    st.session_state.initialized = True

def atualizar_valores(resultados):
    for usina, device, leituras_resp, time_pass in resultados:
        if (usina, device) in st.session_state.metric_placeholders:
            for valor, placeholder in st.session_state.metric_placeholders[(usina, device)]:
                if valor == "time":
                    placeholder.write(f"Tempo: {round(time_pass, 2)}s, Atualizado: {datetime.now().strftime('%H:%M:%S')}")
                else:
                    valores_validos = [float(v) for v in leituras_resp.loc[valor].values if pd.notna(v)]
                    if valores_validos:
                        placeholder.metric(label=valor, value=round(valores_validos[0], 2), border=True)

# Loop principal
while True:
    if time.time() - st.session_state.last_update >= 5:
        st.session_state.resultados_flat = asyncio.run(coletar_dados())
        if not st.session_state.initialized and st.session_state.resultados_flat:
            inicializar_interface(st.session_state.resultados_flat)
        if st.session_state.resultados_flat:
            atualizar_valores(st.session_state.resultados_flat)
        st.session_state.last_update = time.time()
    time.sleep(1)
