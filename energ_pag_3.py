#Pagina #3 de la App multipaginas que muestra el registro 
# de Energias en el Tiempo

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib import ticker



#@st.cache(suppress_st_warning=True)
def energ(datos):
    
    st.markdown("## Energia Activa, Energia Reactiva")#marca o identifica la pagina en cuestion
    st.sidebar.markdown("## Wh/VARh")#la situa en el sidebar

    df_sw = pd.DataFrame(datos)
    df_sw= df_sw.loc[:,['Energia Activa','Energia Reactiva','Tiempo']]
    df_sw.dropna(inplace=True)#Limpia el df eliminando TODAS la FILAS con valores NaN
    df_sw = df_sw.reset_index(drop=True)#Reset el index para indexar segun 
#numero fila 0,1,2,3...n y poder emplear el metodo df.iloc[n]

#Crea un checkbox, para mostrar S/N las mediciones
    #if st.checkbox('Muestra mediciones'):#crea un checkbox, que muestra SI/NO la tabla de datos 
        #st.subheader('Mediciones')
        #st.write(df_sw)

#Crea el grafico de Volt & Corriente, respecto al Tiempo
#df_sw_volt_amp = df_sw_volt.loc[:,['Voltaje','Corriente','Tiempo']]
    energ_act = df_sw['Energia Activa']
    energ_react = df_sw['Energia Reactiva']
    tiempo = df_sw['Tiempo']
    cant = len(tiempo) #Igual a la cantidad de mediciones de Tiempo

#Adiciona un slider para control de la escala de Tiempo

    slider = st.sidebar.slider(
    'Seleccione Intervalo de mediciones',
    0, cant-1,(0, 5))#valor inicial, final (inicial default, final default)

    inicio,fin = slider #indexa los valores de la tupla slider en dos variables

    tiempo = pd.to_datetime(tiempo, format='%H:%M:%S').dt.strftime('%H:%M:%S')

    filtro = df_sw.iloc[fin:fin+20, [0,1,2]]#Toma valor final del slider 
#para filtrar mediciones, muestra las columna 0,1,2 del df_sw

#Para mostrar el grafico completo 100%
    if st.checkbox('Muestra grafico 100%'):#crea un checkbox
        ticker.LinearLocator(numticks = 4)
        st.subheader('Grafico 100% Todas las mediciones')
        filtro = df_sw.iloc[:, [0,1,2]]#todas las filas y solo las columnas 0,1,2,3

    else:
        st.subheader('Intervalo de 20 mediciones')

    fig,ax1 = plt.subplots()
    ax1.plot(filtro['Tiempo'], filtro['Energia Activa'], color= 'g',label='Wh')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Wh',color='g')
    ax1.tick_params(axis='y', labelcolor='g')
    plt.xticks(rotation=45)
    #ELIMINA SOLAPAMIENTO EJE X 
    locator = mdates.AutoDateLocator(minticks=10, maxticks=20)  # Ajusta estos valores según sea necesario
    plt.gca().xaxis.set_major_locator(locator)
    
    plt.tight_layout()
# Crear un segundo y tercer eje (derecho)
    ax2 = ax1.twinx()
    #ax3 = ax1.twinx()
# Grafica la Potencia Reactiva en el segundo eje (derecho)
    ax2.plot(filtro['Tiempo'], filtro['Energia Reactiva'], color= 'b',label='VARh')
    ax2.set_ylabel('VARh', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    #ax3.plot(filtro['Tiempo'], filtro['Potencia Aparente'], color= 'r',label='VA')
    #ax3.set_ylabel('VA', color='g')
    #ax3.tick_params()#axis='y', labelcolor='g')

# Agrega leyendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    #lines_3, labels_3 = ax3.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.title("Energias, Wh, VARh")

    st.write(filtro)#Muestra en el rango seleccionado, las variables de interes
    st.write(slider)
    st.pyplot(fig)