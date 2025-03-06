import pandas as pd
import streamlit as st

def stadist(datos): 
    df = pd.DataFrame(datos)
    df_clean = df.dropna().copy() 
    #st.write(df_clean.head())#Contenido del df_clean
    voltaje_nominal = 120
    tolerancia = 0.10
    limite_inferior = voltaje_nominal * (1 - tolerancia)
    limite_superior = voltaje_nominal * (1 + tolerancia)
    
    df_clean = df_clean.copy()
    df_clean["Fuera de Rango"] = ~df_clean["Voltaje"].between(limite_inferior, limite_superior)
    
    tiempo_fuera_rango = df_clean["Fuera de Rango"].sum()
    
    if "Tiempo" in df_clean.columns:
        df_clean["Tiempo"] = pd.to_timedelta(df_clean["Tiempo"], errors='coerce')
        df_clean = df_clean.dropna(subset=["Tiempo"])
    
    tiempo_total_str = "00:00:00"
    if not df_clean.empty:
        tiempo_total = df_clean["Tiempo"].iloc[-1] #- df_clean["Tiempo"].iloc[0]
        tiempo_total_str = str(tiempo_total).split()[-1] if pd.notna(tiempo_total) else "00:00:00"
    
    estadisticas = df_clean.describe().T
    estadisticas = estadisticas.drop(index="Tiempo", errors='ignore')
    
    estadisticas["Tiempo Fuera de Rango"] = [tiempo_fuera_rango if col == "Voltaje" else None for col in estadisticas.index]
    
    columnas_nuevas = {
        "count": "Cantidad de datos", 
        "mean": "Valor medio", 
        "std": "Desviación Estándar", 
        "min": "Valor mínimo", 
        "max": "Valor máximo", 
        "25%": "P25", 
        "50%": "P50", 
        "75%": "P75"
    }
    estadisticas = estadisticas.rename(columns=columnas_nuevas)
    
    for col in estadisticas.columns:
        if col not in ["Cantidad de datos", "Valor máximo"]:
            estadisticas[col] = pd.to_numeric(estadisticas[col], errors='coerce').round(2)
    
    if "Costo" in estadisticas.index:
        estadisticas.loc["Costo", "Cantidad de datos"] = round(float(estadisticas.loc["Costo", "Cantidad de datos"]), 0)
        estadisticas.loc["Costo", "Valor máximo"] = round(float(estadisticas.loc["Costo", "Valor máximo"]), 4)
    
    tiempo_total_row = pd.DataFrame({col: [None] for col in estadisticas.columns})
    tiempo_total_row.index = ["Tiempo total"]
    tiempo_total_row.loc["Tiempo total", "Valor máximo"] = tiempo_total_str
    
    estadisticas = pd.concat([estadisticas, tiempo_total_row], ignore_index=False, sort=False)
    
    st.write("### Resultados")
    st.dataframe(estadisticas)


