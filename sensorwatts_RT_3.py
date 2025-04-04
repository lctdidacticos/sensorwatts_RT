#Referencia Wi-Fi para corregir la version BLE

import asyncio
import streamlit as st
from streamlit_javascript import st_javascript
import pandas as pd
import plotly.express as px
import aiohttp
import datetime
import subprocess
from PIL import Image

st.set_page_config(page_title="Dashboard Tiempo Real", layout="wide") 

# Input para capturar la IP
IP_SW = st.text_input("URL_SensorWatts")

# Esperar hasta que se ingrese una IP válida
if IP_SW:
    EVENTS_URL = f"{IP_SW}/events"
else:
    st.warning("Por favor, ingrese la URL para continuar.")
    st.stop()  # Detiene la ejecución del script hasta que se ingrese una IP

columns_dict = {
    "voltaje": "Voltaje",
    "frecuencia": "Frecuencia",
    "corriente": "Corriente",
    "factorpot": "Factor de Potencia",
    "rlc": "RLC",
    "potencia": "Potencia",
    "qreact": "Potencia Reactiva",
    "sapart": "Potencia Aparente",
    "eactiva": "Energia Activa",
    "ereact": "Energia Reactiva",
    "Tiempo": "Tiempo"
}

dataframe = pd.DataFrame(columns=columns_dict.values())

# Variable de control para alternar entre "Tiempo Real" y "Estadística"
if "modo_estadistica" not in st.session_state:
    st.session_state.modo_estadistica = False

def toggle_modo():
    st.session_state.modo_estadistica = not st.session_state.modo_estadistica

async def listen_to_events():
    global dataframe
    while True:
        if st.session_state.modo_estadistica:
            break  # Detiene la actualización si está en modo Estadística
        try:
            timeout = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(EVENTS_URL) as response:
                    if response.status == 200:
                        async for line in response.content:
                            try:
                                raw_data = line.decode("utf-8").strip()
                                if raw_data.startswith("data: "):
                                    json_data = raw_data[6:]
                                    new_data = pd.DataFrame([eval(json_data)])
                                    
                                    if 'Tiempo' in new_data.columns:
                                        new_data['Tiempo'] = new_data['Tiempo'].apply(
                                            lambda x: str(datetime.timedelta(seconds=int(x)))
                                        )
                                                                                                            
                                    new_data.rename(columns=columns_dict, inplace=True)
                                    new_data.drop(columns=[col for col in ['MAC'] if col in new_data.columns], inplace=True, errors='ignore')
                                    dataframe = pd.concat([dataframe, new_data], ignore_index=True).tail(100)
                                    
                            except Exception as e:
                                st.error(f"Error procesando datos: {e}")
                    else:
                        st.error(f"Error conectando al servidor: {response.status}")
        except asyncio.TimeoutError:
            st.warning("Se perdió la conexión. Reintentando...")
        except Exception as e:
            st.error(f"Error inesperado: {e}")
        await asyncio.sleep(1)

image_path = "SW_ICON.png"
image = Image.open(image_path)

col1, col2 = st.columns([0.25, 0.75])
with col1:
    st.image(image, use_container_width=True)
with col2:
    st.title("Dashboard en Tiempo Real")

# Botón para cambiar entre modos
app_url = "https://mainpy-8hhzdhejmj8f752qpnlhzq.streamlit.app"  # Reemplaza con la URL real de tu App
if st.button("Estadística"):
    st_javascript(f"window.open('{app_url}', '_blank')")


# Lógica de actualización si está en modo "Tiempo Real"
if not st.session_state.modo_estadistica:
    m1, m2 = st.columns(2)
    c1, c2 = st.columns(2)
    parametro = st.sidebar.selectbox("Selecciona el parámetro a graficar", list(columns_dict.values())[:-1])

    tabla_placeholder = c1.empty()
    grafico_placeholder = c2.empty()
    potencia_placeholder = m1.empty()
    energia_placeholder = m2.empty()
    
    async def main():
        asyncio.create_task(listen_to_events())
        iteration = 0  # Contador para claves únicas
        while not st.session_state.modo_estadistica:
            if not dataframe.empty:
                tabla_placeholder.dataframe(dataframe)
                
                fig = px.line(dataframe, x='Tiempo', y=parametro, title=f"{parametro} en Tiempo Real")
                grafico_placeholder.plotly_chart(fig, use_container_width=True, key=f"plot_{iteration}")
                iteration += 1
                potencia_valor = dataframe["Potencia"].iloc[-1] if "Potencia" in dataframe.columns and not dataframe.empty else 0
                energia_valor = dataframe["Energia Activa"].iloc[-1] if "Energia Activa" in dataframe.columns and not dataframe.empty else 0
                
                
                potencia_placeholder.metric(label="Potencia (W)", value=f"{potencia_valor}")
                energia_placeholder.metric(label="Energia Activa (Wh)", value=f"{energia_valor}")
                
            await asyncio.sleep(1)




# Verificamos si la tarea ya está corriendo en session_state
if "task_running" not in st.session_state:
    st.session_state.task_running = False

async def start_async_tasks():
    if not st.session_state.task_running:
        st.session_state.task_running = True
        await main()

# Iniciamos la tarea de forma segura sin bloquear Streamlit
async def run_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_async_tasks())

# Llamamos la función en Streamlit sin usar experimental_singleton
if not st.session_state.task_running:
    import asyncio

async def start_async_tasks():
    await main()  # Ejecuta la función `main()` de forma segura

async def run_async():
    loop = asyncio.get_event_loop()
    if loop.is_running():  # Si el loop ya está corriendo, ejecutamos la tarea dentro de él
        await start_async_tasks()
    else:
        loop.run_until_complete(start_async_tasks())

# En Streamlit, ejecutamos la tarea de forma segura
asyncio.run(run_async())


