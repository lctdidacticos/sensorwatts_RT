'''Muestra la relacion de Fase Volt & Corriente
de acuerdo al Factor de Potencia de la carga
'''
#INICIO
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu


def fase(datos, ciclos=2):#Muestra n ciclos
    #st.markdown('# Relación de Fase')
    st.sidebar.markdown("## Relaciones de Fase (°)Grados")
    
    df = pd.DataFrame(datos)
    # Asumiendo que los datos ya están limpios y listos para ser procesados.
             
    frecuencia_promedio = df['Frecuencia'].mean()
    tiempo_total = ciclos / frecuencia_promedio
    tiempo = np.linspace(0, tiempo_total, 1000)
    voltaje_max = df['Voltaje'].mean() * 1.41
    onda_voltaje = voltaje_max * np.sin(2 * np.pi * frecuencia_promedio * tiempo)
    
    # Cálculo de la fase y la corriente basándose en el factor de potencia
            
    inductivo = df[df['RLC'] == 'Ind']['Factor de Potencia'].mean()
    corrienteL = df[df['RLC'] == 'Ind']['Corriente'].mean()
    potenciaL = df[df['RLC'] == 'Ind']['Potencia'].mean()
    reactivaL = df[df['RLC'] == 'Ind']['Potencia Reactiva'].mean()
    aparenteL = df[df['RLC'] == 'Ind']['Potencia Aparente'].mean()
    
    resistivo = df[df['RLC'] == 'Res']['Factor de Potencia'].mean()
    df_corrienteR = df[(df['RLC'] == 'Res') & (df['Corriente']!=0)]
    corrienteR = df_corrienteR["Corriente"].mean()
    
    capacitivo = df[df['RLC'] == 'Cap']['Factor de Potencia'].mean()
    corrienteC = df[df['RLC'] == 'Cap']['Corriente'].mean()
    potenciaC = df[df['RLC'] == 'Cap']['Potencia'].mean()
    reactivaC = df[df['RLC'] == 'Cap']['Potencia Reactiva'].mean()
    aparenteC = df[df['RLC'] == 'Cap']['Potencia Aparente'].mean()
    
    
        
    # 2. MENU RLC HORIZONTAL usando la libreria streamlit_option_menu
    
    selected = option_menu('Relacion de fase', ["Resistivo", "Inductivo", "Capacitivo"], 
    icons=['r-circle', 'L', 'c-circle'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
     
    if selected == "Resistivo":
        fase = np.arccos(resistivo)
        corriente_max = corrienteR *1.41
        corriente = corrienteR     
          
    elif selected == "Inductivo":
        fase = -(np.arccos(inductivo))
        corriente_max = corrienteL *1.41
        P = np.round(potenciaL, 2)
        Q = np.round(reactivaL, 2)
        S = np.round(aparenteL, 2)
        fp = np.round(inductivo, 2)
        leyenda = "upper left"
        corriente = corrienteL
    else:
        selected
        fase = np.arccos(capacitivo)
        corriente_max = corrienteC *1.41
        P = np.round(potenciaC, 2)
        Q = np.round(-(reactivaC), 2)
        S = np.round(aparenteC, 2)
        fp = np.round(capacitivo, 2)
        leyenda = "upper right"
        corriente = corrienteC

    fase_grados = np.degrees(fase)
    
    #Probar el valor de fase_grados
    #st.write(fase_grados)
        
    if  (np.isnan(fase_grados) or (corriente <= 0.1) ):  # Si fase_grados es NaN  
                            
        st.markdown ('## NO disponible')   
           
    else:    
        fase_grados = np.round(fase_grados, 2)
    
        st.markdown(f'## Fact. de Potencia {selected} Φ = {fase_grados}°')
    
        onda_corriente = corriente_max * np.sin(2 * np.pi * frecuencia_promedio * tiempo + fase)
    
    
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(tiempo, onda_voltaje, 'r-')
        ax2.plot(tiempo, onda_corriente, 'b-')
        ax1.set_xlabel('Tiempo (s)')
        ax1.set_ylabel('Voltaje (V)', color='r')
        ax1.tick_params(axis='y', labelcolor='r')
        ax2.set_ylabel('Corriente (A)', color='b')
        ax2.tick_params(axis='y', labelcolor='b')
        ax1.grid(True)
        st.pyplot(fig)
    
#Muestra Triangulo de Potencia

# Configurando el gráfico

        if fase_grados == 0:#Factor de Potencia Resistivo
           st.markdown ('## Voltaje y Corriente en Fase') 
        else:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot([0, P], [0, 0], 'g', label=f'P = {P} W')
            ax.plot([P, P], [0, Q], 'b', label=f'Q = {Q} VAR')
            ax.plot([0, P], [0, Q], 'r', label=f'S = {S} VA\nfp = {fp}')
       # ax.text(P / 2, 5, f'P = {P}W', horizontalalignment='center')
        #ax.text(P + 10, Q / 2, f'Q = {Q}VAR', verticalalignment='center')
        #ax.text(P / 2, Q / 2, f'S = {S}VA\nfp = {fp}', horizontalalignment='center')
        
        # Ajustar los límites del gráfico
            ax.set_xlim(left=min(0, P) - abs(P) * 0.1, right=P + abs(P))
            ax.set_ylim(bottom=min(0, Q) - abs(Q) * 0.2, top=Q + abs(1.5*Q))

# Mejorando la presentación
            ax.set_aspect('equal', 'box')
            ax.legend(loc=leyenda)
                           
            ax.grid(True)
            plt.xlabel('Watts')
            plt.ylabel('VAR')
            plt.title('Triángulo de Potencias')

        # Mostrar en Streamlit
            st.pyplot(fig)

    
        























'''import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fase(datos, ciclos =6):
    st.markdown('# Relacion de Fase: (°)Grados')
    st.sidebar.markdown("## (°)Grados")#la situa en el sidebar 
    
# Función para calcular y graficar ondas sinusoidales
#def calcular_ondas_sinusoidales(df, ciclos=10):
        
    df = pd.DataFrame(datos)
    #df= df.loc[:,['Voltaje','Frecuencia','Corriente', 'Factor de Potencia', 'RLC']]
    #df.dropna(inplace=True)#Limpia el df eliminando TODAS la FILAS con valores NaN
    #df = df.reset_index(drop=True)
             
    frecuencia_promedio = df['Frecuencia'].mean()
    tiempo_total = ciclos / frecuencia_promedio
    tiempo = np.linspace(0, tiempo_total, 1000)
    voltaje_max = df['Voltaje'].max()*1.41
    corriente_max = df['Corriente'].max()*1.41
    onda_voltaje = voltaje_max * np.sin(2 * np.pi * frecuencia_promedio * tiempo)
    #Falta agregar la FASE a la onda de corriente en funcion del Factor de Potencia
    onda_corriente = corriente_max * np.sin(2 * np.pi * frecuencia_promedio * tiempo + 30)#Falta agregar la FASE
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(tiempo, onda_voltaje, 'r-')
    ax2.plot(tiempo, onda_corriente, 'b-')
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Voltaje (V)', color='r')
    ax2.set_ylabel('Corriente (A)', color='b')
    st.pyplot(fig)
    
     
    inductivo = df[df['Factor de Potencia'].where(cond=df['RLC']=='Ind')].mean()
    st.write(f'Fact.Induct{inductivo}')'''
    
    
    
   