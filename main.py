from libs.connect_data import get_data
from libs.config import leituras
import streamlit as st
import pandas as pd
import asyncio
import time
from datetime import datetime

# Configuração do layout
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Adicionar CSS personalizado
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-bottom: 1rem;
    }
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        min-height: 100%;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'resultados_flat' not in st.session_state:
    st.session_state.resultados_flat = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

async def processar_usina(usina, dados):
    ip = dados["ip"]
    porta = dados["port"]
    dados_clp = dados["CLPS"]
    unidade = dados["table"]
    resultados = []

    for data_key, data_value in dados_clp.items():
        leituras_resp, time_pass = await get_data(ip, porta, data_value, 'leituras', unidade)
        if leituras_resp is not None and not leituras_resp.empty:
            resultados.append((usina, data_key, leituras_resp, time_pass))
    return resultados

async def main():
    tasks = []
    for usina, dados in leituras.items():
        tasks.append(processar_usina(usina, dados))
    
    resultados = await asyncio.gather(*tasks)
    return [item for sublist in resultados for item in sublist]

def inicializar_interface(resultados_flat):
    """Cria a estrutura inicial da interface com colunas e placeholders."""
    # Criar contêiner fixo
    container = st.container()
    with container:
        cols = st.columns(len(resultados_flat))
        # Armazenar placeholders para métricas no session_state
        st.session_state.metric_placeholders = {}
        cont = 0
        
        for usina, device, leituras_resp, time_pass in resultados_flat:
            with cols[cont]:
                st.write(f"Usina: {usina}-{device}")
                st.session_state.metric_placeholders[(usina, device)] = []
                for valor in leituras_resp.index:
                    placeholder = st.empty()  # Criar placeholder para cada métrica
                    st.session_state.metric_placeholders[(usina, device)].append((valor, placeholder))
                # Placeholder para o tempo de execução
                time_placeholder = st.empty()
                st.session_state.metric_placeholders[(usina, device)].append(('time', time_placeholder))
            cont += 1
    st.session_state.initialized = True

def atualizar_valores(resultados_flat):
    """Atualiza apenas os valores nos placeholders existentes."""
    for usina, device, leituras_resp, time_pass in resultados_flat:
        if (usina, device) in st.session_state.metric_placeholders:
            for valor, placeholder in st.session_state.metric_placeholders[(usina, device)]:
                if valor == 'time':
                    placeholder.write(f"Tempo de execução: {round(time_pass, 2)}, Última atualização: {datetime.now().strftime('%H:%M:%S')}")
                else:
                    valores_validos = [float(v) for v in leituras_resp.loc[valor].values if pd.notna(v)]
                    if valores_validos:
                        placeholder.metric(label=valor, value=round(valores_validos[0], 2), border=True)

cont = 0
# Loop principal
while True:
    if (time.time() - st.session_state.last_update) >= 5:  # Atualiza a cada 5 segundos
        print(cont, ' Atualizando dados')
        cont += 1
        # Obter novos dados
        st.session_state.resultados_flat = asyncio.run(main())
        
        # Inicializar interface apenas na primeira vez
        if not st.session_state.initialized:
            inicializar_interface(st.session_state.resultados_flat)
        
        # Atualizar valores
        atualizar_valores(st.session_state.resultados_flat)
        
        st.session_state.last_update = time.time()
    
    time.sleep(1)  # Evita consumo excessivo de CPU




# import asyncio
# import time
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from libs.connect_data import get_data
# from libs.config import leituras

# # Configuração inicial
# st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# st.markdown(
#     """
#     <style>
#         .block-container { padding: 1rem 0; margin-bottom: 1rem; }
#         [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] { min-height: 100%; }
#         #MainMenu, footer, header { visibility: hidden; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Inicializar session state
# st.session_state.setdefault("last_update", time.time())
# st.session_state.setdefault("resultados_flat", [])
# st.session_state.setdefault("initialized", False)
# st.session_state.setdefault("metric_placeholders", {})

# async def processar_usina(usina, dados):
#     ip, porta, clps, unidade = dados["ip"], dados["port"], dados["CLPS"], dados["table"]
#     resultados = []
#     for data_key, data_value in clps.items():
#         resp, time_pass = await get_data(ip, porta, data_value, "leituras", unidade)
#         if resp is not None and not resp.empty:
#             resultados.append((usina, data_key, resp, time_pass))
#     return resultados

# async def coletar_dados():
#     tasks = [processar_usina(usina, dados) for usina, dados in leituras.items()]
#     return [item for sublist in await asyncio.gather(*tasks) for item in sublist]

# def inicializar_interface(resultados):
#     if not resultados:
#         st.warning("Nenhum dado disponível para exibição.")
#         return
#     with st.container():
#         cols = st.columns(len(resultados))
#         for idx, (usina, device, leituras_resp, _) in enumerate(resultados):
#             with cols[idx]:
#                 st.write(f"Usina: {usina}-{device}")
#                 placeholders = [(valor, st.empty()) for valor in leituras_resp.index]
#                 placeholders.append(("time", st.empty()))
#                 st.session_state.metric_placeholders[(usina, device)] = placeholders
#     st.session_state.initialized = True

# def atualizar_valores(resultados):
#     for usina, device, leituras_resp, time_pass in resultados:
#         if (usina, device) in st.session_state.metric_placeholders:
#             for valor, placeholder in st.session_state.metric_placeholders[(usina, device)]:
#                 if valor == "time":
#                     placeholder.write(f"Tempo: {round(time_pass, 2)}s, Atualizado: {datetime.now().strftime('%H:%M:%S')}")
#                 else:
#                     valores_validos = [float(v) for v in leituras_resp.loc[valor].values if pd.notna(v)]
#                     if valores_validos:
#                         placeholder.metric(label=valor, value=round(valores_validos[0], 2), border=True)

# # Loop principal
# while True:
#     if time.time() - st.session_state.last_update >= 5:
#         st.session_state.resultados_flat = asyncio.run(coletar_dados())
#         if not st.session_state.initialized and st.session_state.resultados_flat:
#             inicializar_interface(st.session_state.resultados_flat)
#         if st.session_state.resultados_flat:
#             atualizar_valores(st.session_state.resultados_flat)
#         st.session_state.last_update = time.time()
#     time.sleep(1)
