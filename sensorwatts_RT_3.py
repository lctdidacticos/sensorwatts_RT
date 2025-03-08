#Referencia Wi-Fi para corregir la version BLE

import asyncio
import streamlit as st
import pandas as pd
import plotly.express as px
import aiohttp
import datetime
import subprocess
from PIL import Image

st.set_page_config(page_title="Dashboard Tiempo Real", layout="wide") 

# Input para capturar la IP
IP_SW = st.text_input("IP SensorWatts 192.168.X.Y")

# Esperar hasta que se ingrese una IP válida
if IP_SW:
    EVENTS_URL = f"http://{IP_SW}/events"
    #st.success(f"Dirección IP establecida: {EVENTS_URL}")
else:
    st.warning("Por favor, ingrese la dirección IP para continuar.")
    st.stop()  # Detiene la ejecución del script hasta que se ingrese una IP

#st.write(EVENTS_URL)
#"http://192.168.1.204/events" Direccion IP SensorWatts / Oficina
#"http://192.168.0.208/events" Direccion IP SensorWatts /Casa

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
            async with aiohttp.ClientSession(timeout=timeout,connector=aiohttp.TCPConnector(ssl=False)) as session:
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
if st.button("Estadística" if not st.session_state.modo_estadistica else "Tiempo Real"):
    toggle_modo()
    if st.session_state.modo_estadistica:
        subprocess.Popen(["streamlit", "run", "main.py"])
    else:
        st.rerun()

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

    asyncio.run(main())
