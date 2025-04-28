# components/estadisticas.py
# ------------------------------------------------------------------
#  Estadísticas basadas en datos REALES de Supabase
# ------------------------------------------------------------------
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
from utils.connection import obtener_reportes     # ← tu función central

# ──────────────────────────────────────────────────────────────────
# 1. Cargar datos (con caché)
# ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def _load_reportes_df():
    data = obtener_reportes()              # lista de dicts
    df = pd.DataFrame(data)
    if df.empty:
        return df
    df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"])
    df["fk_reporte_tipo"] = df["fk_reporte_tipo"].astype("Int64")
    return df


@st.cache_data
def _load_tipos():
    """Catálogo id_tipo → nombre legible."""
    try:
        df_tipo = pd.read_csv("csv_ejemplos/tipo_rows.csv")     # ajusta ruta si fuese otra
        return dict(zip(df_tipo["id_tipo"], df_tipo["nombre_tipo"]))
    except FileNotFoundError:
        st.warning("No se encontró tipo_rows.csv; usaré IDs como etiqueta.")
        return {}


TIPO_LABEL = _load_tipos()

# ──────────────────────────────────────────────────────────────────
# 2. Renderizar estadísticas
# ──────────────────────────────────────────────────────────────────
def mostrar_estadisticas():
    df = _load_reportes_df()

    st.markdown("<h2 class='sub-header'>Estadísticas</h2>", unsafe_allow_html=True)

    if df.empty:
        st.info("Sin datos disponibles en la base.")
        return

    # 2-A. Aplicar filtros globales --------------------------------
    periodo = st.session_state.get("filtro_periodo", "Última semana")
    cp      = st.session_state.get("filtro_cp")

    hoy = datetime.now()
    if periodo == "Última semana":
        df = df[df["fecha_creacion"] >= hoy - timedelta(days=7)]
    elif periodo == "Último mes":
        df = df[df["fecha_creacion"] >= hoy - timedelta(days=30)]
    elif periodo == "Últimos 3 meses":
        df = df[df["fecha_creacion"] >= hoy - timedelta(days=90)]
    # “Todo” → sin filtro

    if cp:
        df = df[df["codigo_postal"] == cp]

    if df.empty:
        st.info("No existen registros para los filtros seleccionados.")
        return

    # 2-B. Serie temporal ------------------------------------------
    serie = (df.groupby(df["fecha_creacion"].dt.date)
               .size().reset_index(name="reportes")
               .sort_values("fecha_creacion"))
    st.plotly_chart(
        px.line(serie, x="fecha_creacion", y="reportes",
                title="Reportes por día",
                labels={"fecha_creacion": "Fecha", "reportes": "Número de reportes"}),
        use_container_width=True
    )

    # 2-C. Distribución por tipo -----------------------------------
    tipos = (df.groupby("fk_reporte_tipo")
               .size().reset_index(name="cantidad")
               .sort_values("cantidad", ascending=False))
    tipos["tipo"] = tipos["fk_reporte_tipo"].map(
        lambda x: TIPO_LABEL.get(x, f"Tipo {x}")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            px.pie(tipos, values="cantidad", names="tipo",
                   title="Distribución de reportes por tipo"),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            px.bar(tipos, x="tipo", y="cantidad",
                   title="Cantidad de reportes por tipo",
                   labels={"tipo": "Tipo de reporte", "cantidad": "Cantidad"}),
            use_container_width=True
        )
