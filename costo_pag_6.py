
#Pagina #6 de la App multipaginas que muestra el registro 
# del Costo de Energia en el Tiempo

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


def costo(datos):
    
    st.markdown("## Costo de la Energia")#marca o identifica la pagina en cuestion
    st.sidebar.markdown("## MXN Moneda Nacional")#la situa en el sidebar

    df_sw = pd.DataFrame(datos)
    df_sw= df_sw.loc[:,['Costo','Tiempo']]
    df_sw.dropna(inplace=True)#Limpia el df eliminando TODAS la FILAS con valores NaN
    df_sw = df_sw.reset_index(drop=True)#Reset el index para indexar segun 
#numero fila 0,1,2,3...n y poder emplear el metodo df.iloc[n]

#Crea un checkbox, para mostrar S/N las mediciones
    #if st.checkbox('Muestra mediciones'):#crea un checkbox, que muestra SI/NO la tabla de datos 
        #st.subheader('Mediciones')
        #st.write(df_sw)

#Crea el grafico de Volt & Corriente, respecto al Tiempo

    costo_energ = df_sw['Costo']
    tiempo = df_sw['Tiempo']
    cant = len(tiempo) #Igual a la cantidad de mediciones de Tiempo

#Adiciona un slider para control de la escala de Tiempo

    slider = st.sidebar.slider(
    'Seleccione Intervalo de mediciones',
    0, cant-1,(0, 5))#valor inicial, final,(inicial default, final default)

    inicio,fin = slider #indexa los valores de la tupla slider en dos variables

    tiempo = pd.to_datetime(tiempo, format='%H:%M:%S').dt.strftime('%H:%M:%S')

    filtro = df_sw.iloc[fin:fin+20, [0,1]]#Toma valor final del slider 
#para filtrar mediciones, muestra las columna 0,1,2 del df_sw

#Para mostrar el grafico completo 100%
    if st.checkbox('Muestra grafico 100%'):#crea un checkbox
    
        st.subheader('Grafico 100% Todas las mediciones')
        filtro = df_sw.iloc[:, [0,1]]#todas las filas y solo las columnas 0,1,4

    else:
        st.subheader('Intervalo de 20 mediciones')

    fig,ax1 = plt.subplots()
    ax1.plot(filtro['Tiempo'], filtro['Costo'], color= 'b',label='Costo MXN')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('MXN',color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    plt.xticks(rotation=45)
    #ELIMINA SOLAPAMIENTO EJE X  
    locator = mdates.AutoDateLocator(minticks=10, maxticks=20)  # Ajusta estos valores según sea necesario
    plt.gca().xaxis.set_major_locator(locator)
     
    plt.tight_layout()
    

# Agrega leyendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    ax1.legend(lines_1 , labels_1 , loc='upper left')

    plt.title("Costo de la Energia MXN")

    st.write(filtro)#Muestra en el rango seleccionado, las variables de interes
    st.write(slider)
    st.pyplot(fig)