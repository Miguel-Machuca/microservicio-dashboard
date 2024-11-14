import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime

# Importar st_autorefresh desde streamlit_autorefresh
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st.error("Por favor, instala 'streamlit-autorefresh' ejecutando 'pip install streamlit-autorefresh' en tu terminal.")
    st.stop()

# Configuración de la página
st.set_page_config(
    page_title='Dashboard de Productos Electrodomésticos',
    page_icon='🔌',
    layout='wide'
)

# Título del dashboard
st.title("Dashboard en Tiempo Real para Productos Electrodomésticos")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("electrodomesticos.csv", parse_dates=['fecha_venta'])
    return df

df = load_data()

# Filtros de la barra lateral
st.sidebar.header("Filtros")

categoria_filter = st.sidebar.multiselect(
    "Selecciona Categorías de Producto",
    options=df['categoria'].unique(),
    default=df['categoria'].unique()
)

region_filter = st.sidebar.multiselect(
    "Selecciona Regiones",
    options=df['region'].unique(),
    default=df['region'].unique()
)

fecha_inicio = st.sidebar.date_input(
    "Fecha de Inicio",
    df['fecha_venta'].min()
)

fecha_fin = st.sidebar.date_input(
    "Fecha de Fin",
    df['fecha_venta'].max()
)

# Filtrar datos según selecciones
mask = (
    df['categoria'].isin(categoria_filter) &
    df['region'].isin(region_filter) &
    (df['fecha_venta'] >= pd.to_datetime(fecha_inicio)) &
    (df['fecha_venta'] <= pd.to_datetime(fecha_fin))
)
filtered_df = df[mask]

# Definición de KPIs
def calcular_kpis(data):
    ventas_totales = data['ventas'].sum()
    unidades_vendidas = data['unidades_vendidas'].sum()
    margen_beneficio = ((data['precio_venta'] - data['costo']) * data['unidades_vendidas']).sum()
    rotacion_inventario = (data['unidades_vendidas'] / data['inventario']).mean()
    tasa_devoluciones = (data['devoluciones'].sum() / data['unidades_vendidas'].sum()) * 100 if data['unidades_vendidas'].sum() > 0 else 0
    satisfaccion_cliente = data['calificacion_cliente'].mean()
    
    return {
        'Ventas Totales ($)': f"${ventas_totales:,.2f}",
        'Unidades Vendidas': f"{unidades_vendidas}",
        'Margen de Beneficio ($)': f"${margen_beneficio:,.2f}",
        'Rotación de Inventario': f"{rotacion_inventario:.2f}",
        'Tasa de Devoluciones (%)': f"{tasa_devoluciones:.2f}%",
        'Satisfacción del Cliente': f"{satisfaccion_cliente:.2f}/5"
    }

kpis = calcular_kpis(filtered_df)

# Contenedor para KPIs
st.markdown("## KPIs Principales")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Ventas Totales", kpis['Ventas Totales ($)'])
col2.metric("Unidades Vendidas", kpis['Unidades Vendidas'])
col3.metric("Margen de Beneficio", kpis['Margen de Beneficio ($)'])
col4.metric("Rotación de Inventario", kpis['Rotación de Inventario'])
col5.metric("Tasa de Devoluciones", kpis['Tasa de Devoluciones (%)'])
col6.metric("Satisfacción del Cliente", kpis['Satisfacción del Cliente'])

# Visualizaciones
st.markdown("## Visualizaciones")

# Gráfico de Ventas por Categoría
fig1 = px.bar(
    filtered_df.groupby('categoria')['ventas'].sum().reset_index(),
    x='categoria',
    y='ventas',
    color='categoria',
    title='Ventas por Categoría',
    labels={'ventas': 'Ventas ($)', 'categoria': 'Categoría'}
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de Tendencia de Ventas en el Tiempo
fig2 = px.line(
    filtered_df.groupby('fecha_venta')['ventas'].sum().reset_index(),
    x='fecha_venta',
    y='ventas',
    title='Tendencia de Ventas en el Tiempo',
    labels={'fecha_venta': 'Fecha de Venta', 'ventas': 'Ventas ($)'}
)
st.plotly_chart(fig2, use_container_width=True)

# Gráfico de Distribución de Satisfacción del Cliente
fig3 = px.histogram(
    filtered_df,
    x='calificacion_cliente',
    nbins=20,
    title='Distribución de Satisfacción del Cliente',
    labels={'calificacion_cliente': 'Calificación del Cliente'}
)
st.plotly_chart(fig3, use_container_width=True)

# Vista Detallada de Datos
st.markdown("## Vista Detallada de Datos")
st.dataframe(filtered_df)

# Actualización Automática del Dashboard Cada 60 Segundos
# Nota: Puedes ajustar el intervalo según tus necesidades (60000 ms = 60 segundos)
count = st_autorefresh(interval=60000, limit=None, key="dashboard_refresh")
