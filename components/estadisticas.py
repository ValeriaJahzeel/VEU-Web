# components/estadisticas.py
# ------------------------------------------------------------------
#  Estadísticas mensuales  • Selector Año/Mes en español
#  - Por defecto muestra el mes y año actuales
#  - Botón “Aplicar” debajo y centrado
# ------------------------------------------------------------------
from datetime import datetime
import calendar
import locale

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.connection import obtener_reportes

# ╭────────── 1. Carga de datos ────────────────────────────────────╮
@st.cache_data(ttl=600)
def _load_reportes_df() -> pd.DataFrame:
    data = obtener_reportes()
    df = pd.DataFrame(data)
    if not df.empty:
        df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"])
        df["fk_reporte_tipo"] = df["fk_reporte_tipo"].astype("Int64")
    return df

@st.cache_data
def _load_tipos() -> dict:
    try:
        df_tipo = pd.read_csv("csv_ejemplos/tipo_rows.csv")
        return dict(zip(df_tipo["id_tipo"], df_tipo["nombre_tipo"]))
    except FileNotFoundError:
        return {}

TIPO_LABEL = _load_tipos()

# Meses en español (fallback en caso de que locale falle)
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except locale.Error:
    pass
ES_MES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# ╭────────── 2. Función principal ────────────────────────────────╮
def mostrar_estadisticas():
    df = _load_reportes_df()
    st.markdown("## Estadísticas por mes")

    if df.empty:
        st.info("Sin datos disponibles.")
        return

    # Filtro opcional por CP
    cp = st.session_state.get("filtro_cp")
    if cp:
        df = df[df["codigo_postal"] == cp]

    hoy = datetime.now()

    # Años disponibles hasta el actual
    anios_disp = df["fecha_creacion"].dt.year.drop_duplicates().sort_values()

    # Selectores compactos
    col_a, col_b = st.columns(2)

    with col_a:
        anio_sel = st.selectbox(
            "Año",
            anios_disp,
            index=list(anios_disp).index(
                hoy.year if hoy.year in anios_disp.values else anios_disp.iloc[-1]
            ),
            key="filtro_anio",
        )

    # Meses disponibles para el año seleccionado
    meses_disp = (
        df[df["fecha_creacion"].dt.year == anio_sel]["fecha_creacion"]
        .dt.month.drop_duplicates().sort_values()
    )
    if anio_sel == hoy.year:
        meses_disp = meses_disp[meses_disp <= hoy.month]

    with col_b:
        mes_sel = st.selectbox(
            "Mes",
            list(meses_disp),
            format_func=lambda m: ES_MES[m],
            index=list(meses_disp).index(
                hoy.month if anio_sel == hoy.year else meses_disp.iloc[-1]
            ),
            key="filtro_mes",
        )

    # Botón “Aplicar” en una fila aparte, centrado
    col_btn = st.columns([1, 1, 1])[1]
    with col_btn:
        buscar = st.button("Aplicar", use_container_width=True)

    # Ejecutar al primer render o cuando se pulse
    if ("ejecutar_estadisticas" not in st.session_state) or buscar:
        st.session_state["ejecutar_estadisticas"] = True
    else:
        st.stop()

    # Rango de fechas del mes seleccionado
    fecha_ini = datetime(anio_sel, mes_sel, 1)
    ultimo_dia = calendar.monthrange(anio_sel, mes_sel)[1]
    fecha_fin = (
        datetime(anio_sel, mes_sel, hoy.day)
        if (anio_sel == hoy.year and mes_sel == hoy.month)
        else datetime(anio_sel, mes_sel, ultimo_dia)
    )

    df_mes = df[(df["fecha_creacion"] >= fecha_ini) & (df["fecha_creacion"] <= fecha_fin)]
    if df_mes.empty:
        st.warning("No hay reportes para el mes seleccionado.")
        return

    # ── Serie temporal multillínea ────────────────────────────────
    df_mes["dia"] = df_mes["fecha_creacion"].dt.day
    serie = df_mes.groupby(["dia", "fk_reporte_tipo"]).size().reset_index(name="tot")
    serie["tipo"] = serie["fk_reporte_tipo"].map(
        lambda x: TIPO_LABEL.get(x, f"Tipo {x}")
    )

    # Índice completo de días
    N_dias = fecha_fin.day
    dias = pd.DataFrame({"dia": range(1, N_dias + 1)})

    lines = []
    for tipo, sub in serie.groupby("tipo"):
        merged = dias.merge(sub[["dia", "tot"]], on="dia", how="left").fillna(0)
        merged["tipo"] = tipo
        lines.append(merged)

    serie_full = pd.concat(lines, ignore_index=True)
    serie_full["tot"] = serie_full["tot"].astype(int)

    fig_line = px.line(
        serie_full, x="dia", y="tot", color="tipo", markers=True,
        title=f"Reportes por día – {ES_MES[mes_sel]} {anio_sel}",
        labels={"dia": "Día del mes", "tot": "N° reportes", "tipo": "Tipo"}
    )
    fig_line.update_xaxes(dtick=1, range=[1, N_dias])
    fig_line.update_yaxes(dtick=1)

    st.plotly_chart(fig_line, use_container_width=True)

    # ── Distribución mensual ──────────────────────────────────────
    tipos_mes = (
        df_mes.groupby("fk_reporte_tipo").size().reset_index(name="cantidad")
        .sort_values("cantidad", ascending=False)
    )
    tipos_mes["tipo"] = tipos_mes["fk_reporte_tipo"].map(
        lambda x: TIPO_LABEL.get(x, f"Tipo {x}")
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.pie(tipos_mes, values="cantidad", names="tipo",
                   title="Distribución por tipo (mes)"),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            px.bar(tipos_mes, x="tipo", y="cantidad",
                   title="Cantidad de reportes por tipo (mes)",
                   labels={"tipo": "Tipo", "cantidad": "Cantidad"}),
            use_container_width=True
        )
