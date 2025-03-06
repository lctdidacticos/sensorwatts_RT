
#Pagina #1 de la App multipaginas que muestra el registro 
# de Voltaje y Corriente en el Tiempo

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


def volt(datos):
    
    st.markdown("## Mediciones de Voltaje & Corriente")#marca o identifica la pagina en cuestion
    st.sidebar.markdown("## Volt/Amp")#la situa en el sidebar

    df_sw = pd.DataFrame(datos)
    df_sw= df_sw.loc[:,['Voltaje','Corriente','Tiempo']]
    df_sw.dropna(inplace=True)#Limpia el df eliminando TODAS la FILAS con valores NaN
    df_sw = df_sw.reset_index(drop=True)#Reset el index para indexar segun 
#numero fila 0,1,2,3...n y poder emplear el metodo df.iloc[n]

#Crea el grafico de Volt & Corriente, respecto al Tiempo

    volt = df_sw['Voltaje']
    amp = df_sw['Corriente']
    tiempo = df_sw['Tiempo']
    cant = len(tiempo) #Igual a la cantidad de mediciones de Tiempo

#Adiciona un slider para control de la escala de Tiempo

    slider = st.sidebar.slider(
    'Seleccione Intervalo de mediciones',
    0, cant-1,(0, 0))#valor inicial, final,(inicial default, final default)

    inicio,fin = slider #indexa los valores de la tupla slider en dos variables

    tiempo = pd.to_datetime(tiempo, format='%H:%M:%S').dt.strftime('%H:%M:%S')

    filtro = df_sw.iloc[fin:fin+20, [0,1,2]]#Toma valor final del slider 
#para filtrar mediciones, muestra las columna 0,1,2 del df_sw

#Para mostrar el grafico completo 100%
    if st.checkbox('Muestra grafico 100%'):#crea un checkbox
    
        st.subheader('Grafico 100% Todas las mediciones')
        filtro = df_sw.iloc[:, [0,1,2]]#todas las filas y solo las columnas 0,1,4

    else:
        st.subheader('Intervalo de 20 mediciones')

    fig,ax1 = plt.subplots()
    ax1.plot(filtro['Tiempo'], filtro['Voltaje'], color= 'b',label='Volt_rms')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Volt_rms',color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    plt.xticks(rotation=45)
    #ELIMINA SOLAPAMIENTO EJE X  
    locator = mdates.AutoDateLocator(minticks=10, maxticks=20)  # Ajusta estos valores según sea necesario
    plt.gca().xaxis.set_major_locator(locator)
     
    plt.tight_layout()
# Crear un segundo eje (derecho)
    ax2 = ax1.twinx()

# Grafica la Corriente en el segundo eje (derecho)
    ax2.plot(filtro['Tiempo'], filtro['Corriente'], color= 'r',label='Amp_rms')
    ax2.set_ylabel('Amp_rms', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

# Agrega leyendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.title("Voltaje y Corriente valores rms")

    st.write(filtro)#Muestra en el rango seleccionado, las variables de interes
    st.write(slider)
    st.pyplot(fig)