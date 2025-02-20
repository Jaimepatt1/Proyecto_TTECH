import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
git add Proyecto_DA.csv
git commit -m "Agregar Proyecto_DA.csv"
git push

df = pd.read_csv('Proyecto_DA')
# Calcular el rango intercuartílico (IQR)
Q1 = df['MONTO_TOTAL_AP'].quantile(0.25)
Q3 = df['MONTO_TOTAL_AP'].quantile(0.75)
IQR = Q3 - Q1

# Definir los límites para identificar valores atípicos
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Calcular la mediana
median_value = df['MONTO_TOTAL_AP'].median()

# Reemplazar los valores atípicos por la mediana
df['MONTO_TOTAL_AP'] = np.where((df['MONTO_TOTAL_AP'] < lower_bound) | (df['MONTO_TOTAL_AP'] > upper_bound), 
                                 median_value, df['MONTO_TOTAL_AP'])

# Crear un diccionario para mapear ESTADO_PROYECTO a las clasificaciones deseadas
classification_mapping = {
    'CODIFICADO': 'Positivo',
    'APROBADO': 'Positivo',
    'EJECUCION': 'Positivo',
    'REVISADO': 'Positivo',
    'LEGALIZADO': 'Positivo',
    'POR EVALUAR': 'Otro',
    'POR LIQUIDAR': 'Otro',
    'RETIRADO POR BENEFICIARIO': 'Negativo',
    'FINALIZADO': 'Positivo',
    'LIQUIDADO A PAZ Y SALVO': 'Otro',
    'LIQUIDADO': 'Negativo',
    'LIQUIDADO INFORME SECRETARIAL': 'Otro',
    'APROBADO MEN-CINTEL': 'Positivo',
    'RETIRADO': 'Negativo',
    'SIN RECURSOS': 'Negativo',
    'RETIRADO POR MINCIENCIAS': 'Negativo',
    'POR ELABORAR CONTRATO': 'Otro',
    'NEGADO': 'Negativo',
    'EVALUADO': 'Otro',
    'DEVUELTO': 'Negativo'
}

# Crear una nueva columna 'Classification' en el DataFrame usando el mapeo
df['Classification'] = df['ESTADO_PROYECTO'].map(classification_mapping)

# Agrupar por clasificación y sumar el MONTO_TOTAL_AP
grouped_df = df.groupby('Classification')['MONTO_TOTAL_AP'].sum().reset_index()

# Código de Streamlit para crear el dashboard interactivo

# Título del dashboard
st.title("Dashboard Interactivo de Proyectos")

# Subtítulo
st.subheader("Visualización de MONTO_TOTAL_AP por Clasificación de Proyecto")

# Sidebar para seleccionar variables
st.sidebar.title("Opciones de Visualización")
option = st.sidebar.selectbox(
    "Seleccione la visualización",
    ("Gráfico de Barras", "Gráfico Circular", "Gráfico de Caja", "Gráfico de Dispersión")
)

# Función para crear gráficos
def create_plots():
    if option == "Gráfico de Barras":
        st.subheader("Total MONTO_TOTAL_AP por Clasificación")
        plt.figure(figsize=(10, 6))
        plt.bar(grouped_df['Classification'], grouped_df['MONTO_TOTAL_AP'], color=['green', 'red', 'blue'])
        plt.xlabel('Clasificación')
        plt.ylabel('Total MONTO_TOTAL_AP')
        plt.title('Total MONTO_TOTAL_AP por Clasificación (sin valores atípicos)')
        st.pyplot(plt)

    elif option == "Gráfico Circular":
        st.subheader("Proporción de MONTO_TOTAL_AP por Clasificación")
        plt.figure(figsize=(8, 8))
        plt.pie(grouped_df['MONTO_TOTAL_AP'], labels=grouped_df['Classification'], autopct='%1.1f%%', colors=['green', 'red', 'blue'])
        plt.title('Proporción de MONTO_TOTAL_AP por Clasificación (sin valores atípicos)')
        st.pyplot(plt)

    elif option == "Gráfico de Caja":
        st.subheader("Distribución de MONTO_TOTAL_AP por Clasificación")
        plt.figure(figsize=(10, 6))
        df.boxplot(column='MONTO_TOTAL_AP', by='Classification', grid=False)
        plt.xlabel('Clasificación')
        plt.ylabel('MONTO_TOTAL_AP')
        plt.title('Distribución de MONTO_TOTAL_AP por Clasificación (sin valores atípicos)')
        plt.suptitle('')  # Esto elimina el título automático de Pandas
        st.pyplot(plt)

    elif option == "Gráfico de Dispersión":
        st.subheader("Dispersión de MONTO_TOTAL_AP por Clasificación")
        plt.figure(figsize=(10, 6))
        colors = {'Positivo': 'green', 'Negativo': 'red', 'Otro': 'blue'}
        plt.scatter(df['Classification'], df['MONTO_TOTAL_AP'], c=df['Classification'].map(colors))
        plt.xlabel('Clasificación')
        plt.ylabel('MONTO_TOTAL_AP')
        plt.title('Dispersión de MONTO_TOTAL_AP por Clasificación (sin valores atípicos)')
        st.pyplot(plt)

# Llamar a la función para crear gráficos
create_plots()
