import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from PIL import Image
import io
import base64
import numpy as np
import time


# Configurar la página
st.set_page_config(page_title="ENSO y Precipitación - Chocó Andino", layout="wide")

# Estilo visual mejorado, dinámico y elegante
st.markdown(
    """
    <style>
        html, body, .main {
            background-color: #f0f4fa;
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #17375e;
            font-weight: 600;
        }
        .stSidebar {
            background-color: #e6f0ff !important;
        }
        .css-18e3th9 {
            padding: 2rem;
        }
        .block-container {
            padding: 2rem 3rem;
        }
        .stButton>button {
            background: linear-gradient(90deg, #004c99, #0073e6);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #0055aa, #0080ff);
            transform: scale(1.05);
        }
        .st-bb {
            background-color: #dbefff;
            border-left: 6px solid #2a7fff;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .footer {
            text-align: center;
            font-size: 13px;
            color: #7a7a7a;
            padding-top: 2rem;
        }
        .stRadio > div {
            background-color: #f2f8ff;
            border-radius: 8px;
            padding: 0.8rem 1rem;
            box-shadow: inset 0 0 0 1px #cce0ff;
        }
        .stRadio > div > label {
            color: #174c85;
            font-weight: 500;
        }
        .stSelectbox > div > div {
            background-color: #f5fbff;
            border-radius: 5px;
        }
    </style>
    <style>
    /* 🔧 Mejora visual de todos los filtros */

    .stMultiSelect div[data-baseweb="select"], 
    .stSelectbox div[data-baseweb="select"], 
    .stRadio > div, 
    .stCheckbox > div {
        background-color: #ffffff !important;
        color: #1a3f66 !important;
        border-radius: 8px !important;
        border: 1px solid #c0d4f7 !important;
        font-size: 16px !important;
        font-weight: 500;
        box-shadow: none !important;
    }

    /* Opciones internas */
    [data-baseweb="select"] span {
        color: #1a3f66 !important;
    }

    /* Etiquetas de multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #e6f2ff !important;
        color: #0c2d59 !important;
        font-weight: 600;
    }

    /* Hover de opciones */
    [data-baseweb="menu"] > div {
        background-color: #f0f4fa !important;
        color: #17375e !important;
    }

    /* Texto de etiquetas */
    .stSelectbox label, 
    .stRadio label, 
    .stMultiSelect label {
        font-weight: bold;
        color: #1a3f66;
        font-size: 15px;
    }
    </style>

""",
    unsafe_allow_html=True,
)


# --- Sidebar personalizado ---
st.sidebar.image("images/logo.png", use_container_width=True)  # Cambié use_column_width a use_container_width

st.sidebar.markdown("## 🌿 ENSO-Chocó App")


def boton_exportar(fig, nombre="grafico"):
    buffer = io.BytesIO()
    fig.write_image(buffer, format="png")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{nombre}.png">📥 Descargar imagen</a>'
    return href


opciones = st.sidebar.radio(
    "📂 Secciones disponibles:",
    (
        "📘 Introducción",
        "📈 Análisis Gráfico",
        "📊 Comparar Estaciones",
        "🌿 NDVI - Análisis Anual",
        "📊 Correlaciones",
        "🌊 Wavelet",
        "🗺️ Mapa Interactivo",
    ),
)


st.markdown(
    """
<div class="footer">
  📍 Proyecto académico - Análisis multivariable ENSO y precipitación en el Chocó Andino 🌧️<br>
  Desarrollado con ❤️ en Python + Streamlit
</div>
""",
    unsafe_allow_html=True,
)

# --- Introducción ---
if opciones == "📘 Introducción":


    st.title("🌎 Proyecto: ENSO y Precipitación en el Chocó Andino")
    
    # HTML como cadena de texto
    html_code = """
    <div style="background-color: #f8f8f8; padding: 3rem; border-radius: 15px; box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);">
        <div style="text-align: center;">
            <h2 style="color: #004d7a; font-size: 30px; font-weight: bold; margin-bottom: 20px;">El Fenómeno ENSO</h2>
            <p style="font-size: 20px; color: #595959; line-height: 1.6; max-width: 800px; margin: 0 auto;">
                El fenómeno <strong>ENSO</strong> es un evento climático interanual que altera significativamente las condiciones atmosféricas y oceánicas a nivel global. 
                Este fenómeno se presenta en tres fases: <strong>El Niño</strong>, <strong>La Niña</strong> y una fase <strong>Neutra</strong>, 
                cada una con impactos distintos sobre los sistemas naturales y humanos, especialmente en la distribución de las lluvias y temperaturas en regiones tropicales.
            </p>
        </div>

        <div style="background-color: #ffffff; padding: 2rem; margin-top: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);">
            <h3 style="color: #004d7a; font-size: 24px; font-weight: bold;">🎯 Objetivo del Proyecto</h3>
            <p style="font-size: 18px; color: #595959; line-height: 1.6;">
                Este proyecto analiza la relación entre los eventos ENSO (El Niño, La Niña y Neutro) y la precipitación en el <strong>Chocó Andino</strong> entre los años 
                <strong>1992 y 2022</strong>, utilizando herramientas estadísticas y de visualización avanzada.
            </p>
        </div>

        <div style="background-color: #ffffff; padding: 2rem; margin-top: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);">
            <h3 style="color: #004d7a; font-size: 24px; font-weight: bold;">🔬 Metodología</h3>
            <p style="font-size: 18px; color: #595959; line-height: 1.6;">
                Se emplean análisis estadísticos rigurosos, visualizaciones interactivas y mapas dinámicos para evaluar el impacto de los eventos ENSO en las estaciones meteorológicas ubicadas en la región.
            </p>
        </div>

        <div style="background-color: #ffffff; padding: 2rem; margin-top: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05); display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1; padding-right: 20px;">
                <h3 style="color: #004d7a; font-size: 24px; font-weight: bold;">👥 Integrantes</h3>
                <p style="font-size: 18px; color: #595959; line-height: 1.6;">
                    <span style="font-weight: bold; color: #1f4e79;">💼 Lizeth Aguilar</span> <br>
                    <span style="font-weight: bold; color: #1f4e79;">🎓 Jessica Quinga</span> <br>
                    <span style="font-weight: bold; color: #1f4e79;">🔬 Deysi Remache</span> 
                </p>
            </div>
         </div>
    """
    
    # Usamos st.components.v1.html para procesar el HTML
    components.html(html_code, height=1200)

    st.success("Usa el panel lateral para navegar entre las secciones del proyecto.")


# --- Análisis Gráfico ---
elif opciones == "📈 Análisis Gráfico":
    st.markdown("## 📈 Análisis Gráfico por Estación")

    estaciones = [
        "Estacion 1",
        "Estacion 2",
        "Estacion 3",
        "Estacion 4",
        "Estacion 5",
        "Estacion 6",
    ]
    estacion_sel = st.selectbox("🌍 Selecciona una estación:", estaciones)
# --- Submenú de análisis gráfico ---
    ruta = f"data/{estacion_sel}/"

    try:
        # Cargar y preparar datos
        df_box = pd.read_excel(ruta + "Boxplot precipitacion y spi.xlsx")
        df_spi = pd.read_excel(ruta + "SPI.xlsx")

        df_box.rename(
            columns={"Precipitacion (mm)": "Precipitación", "FECHA": "Fecha"},
            inplace=True,
        )
        df_spi.rename(columns={"FECHA": "Fecha"}, inplace=True)
        df_box["Fecha"] = pd.to_datetime(df_box["Fecha"])
        df_spi["Fecha"] = pd.to_datetime(df_spi["Fecha"])
        df_box["Año"] = df_box["Fecha"].dt.year
        df_box["Mes"] = df_box["Fecha"].dt.month_name()

        analisis = st.selectbox("🔍 Elige qué análisis deseas visualizar:", [
            "📦 Boxplots",
            "📉 Series Temporales",
            "📎 Dispersión SPI vs Precipitación",
            "🧭 Panel Climático",
            "🛠️ Visualizador Personalizado"
        ])
        
        # Función de filtro visual elegante
        def aplicar_filtros(df, key):
            with st.expander("🎛️ Filtros", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    años = st.multiselect(
                        "Años",
                        sorted(df["Año"].unique()),
                        default=sorted(df["Año"].unique()),
                        key=f"{key}_a",
                    )
                with col2:
                    meses = st.multiselect(
                        "Meses",
                        df["Mes"].unique(),
                        default=df["Mes"].unique(),
                        key=f"{key}_m",
                    )
                with col3:
                    fases = st.multiselect(
                        "Fase ENSO",
                        df["Fase_ENSO"].unique(),
                        default=df["Fase_ENSO"].unique(),
                        key=f"{key}_f",
                    )
            return df[
                (df["Año"].isin(años))
                & (df["Mes"].isin(meses))
                & (df["Fase_ENSO"].isin(fases))
            ]
            
        if analisis == "📦 Boxplots":
            # 📦 Boxplot Precipitación
            st.subheader("📦 Boxplot de Precipitación")
            df_ppt = aplicar_filtros(df_box, "box_ppt")
            fig1 = px.box(
                df_ppt,
                x="Fase_ENSO",
                y="Precipitación",
                color="Fase_ENSO",
                points="all",
                color_discrete_map={"Niño": "red", "Niña": "blue", "Neutro": "gray"},
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(boton_exportar(fig1, "boxplot_precipitacion"), unsafe_allow_html=True)

    # Interpretación
            med_nino = df_ppt[df_ppt["Fase_ENSO"] == "Niño"]["Precipitación"].median()
            med_nina = df_ppt[df_ppt["Fase_ENSO"] == "Niña"]["Precipitación"].median()
            med_neutro = df_ppt[df_ppt["Fase_ENSO"] == "Neutro"]["Precipitación"].median()
            st.info(f"🔎 Medianas: Niño = {med_nino:.1f} mm, Niña = {med_nina:.1f} mm, Neutro = {med_neutro:.1f} mm.")

            # 📦 Boxplot SPI
            st.subheader("📦 Boxplot de SPI")
            df_spi_box = aplicar_filtros(df_box, "box_spi")
            fig2 = px.box(
                df_spi_box,
                x="Fase_ENSO",
                y="SPI",
                color="Fase_ENSO",
                points="all",
                color_discrete_map={"Niño": "red", "Niña": "blue", "Neutro": "gray"},
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown(boton_exportar(fig2, "boxplot_spi"), unsafe_allow_html=True)

            med_spi = df_spi_box.groupby("Fase_ENSO")["SPI"].median().round(2)
            st.info(f"🔎 Mediana SPI por fase ENSO: {med_spi.to_dict()}")

            # 📉 Serie SPI
            
            
        elif analisis == "📉 Series Temporales": 
            st.subheader("📉 Serie Temporal SPI")
            with st.expander("🎛️ Filtros", expanded=False):
                años_spi = st.multiselect(
                    "Años SPI",
                    sorted(df_spi["Fecha"].dt.year.unique()),
                    default=sorted(df_spi["Fecha"].dt.year.unique()),
                    key="serie_spi",
                )
            df_spi_f = df_spi[df_spi["Fecha"].dt.year.isin(años_spi)]
            fig3 = px.line(
                df_spi_f,
                x="Fecha",
                y="SPI",
                markers=True,
                line_shape="spline",
                color_discrete_sequence=["black"],
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(boton_exportar(fig3, "serie_spi"), unsafe_allow_html=True)
            # 🌧️ Serie Precipitación
            st.subheader("🌧️ Serie Temporal Precipitación")
            df_precip_linea = aplicar_filtros(df_box, "serie_ppt")
            fig4 = px.line(
                df_precip_linea,
                x="Fecha",
                y="Precipitación",
                color="Fase_ENSO",
                line_shape="spline",
                markers=True,
                color_discrete_map={"Niño": "red", "Niña": "blue", "Neutro": "gray"},
            )
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown(boton_exportar(fig4, "serie_precipitacion"), unsafe_allow_html=True)


        elif analisis == "📎 Dispersión SPI vs Precipitación":
            # 📊 Barras anuales
            st.subheader("📊 Precipitación Anual Acumulada")
            df_barras = aplicar_filtros(df_box, "barras")
            df_barras_grouped = df_barras.groupby(["Año", "Fase_ENSO"], as_index=False)[
                "Precipitación"
            ].sum()
            fig5 = px.bar(
                df_barras_grouped,
                x="Año",
                y="Precipitación",
                color="Fase_ENSO",
                color_discrete_map={"Niño": "red", "Niña": "blue", "Neutro": "gray"},
            )
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown(boton_exportar(fig5, "barras_anuales"), unsafe_allow_html=True)

            # 📎 Dispersión SPI vs Precipitación
            st.subheader("📎 Relación SPI vs Precipitación")
            df_disp = aplicar_filtros(df_box, "dispersion")
            fig6 = px.scatter(
                df_disp,
                x="SPI",
                y="Precipitación",
                color="Fase_ENSO",
                trendline="ols",
                color_discrete_map={"Niño": "red", "Niña": "blue", "Neutro": "gray"},
            )
            fig6.update_traces(marker=dict(size=10))
            st.plotly_chart(fig6, use_container_width=True)
            st.markdown(boton_exportar(fig6, "dispersión_spi_precipitacion"), unsafe_allow_html=True)
        
        elif analisis == "🧭 Panel Climático":
# ===================== 🌎 DASHBOARD CLIMÁTICO =====================
            st.markdown("---")
            st.markdown("<h3 style='color:#1f4e79;'>🧭 Panel Climático Resumen</h3>", unsafe_allow_html=True)

            # --- KPIs
            spi_median = df_box["SPI"].median()
            spi_min = df_box["SPI"].min()
            spi_max = df_box["SPI"].max()
            ppt_total = df_box["Precipitación"].sum()
            años_unicos = df_box["Año"].nunique()

            # Clasificación climática
            if spi_median <= -1:
                categoria = "🌵 Seca"
            elif -1 < spi_median < 1:
                categoria = "🌤️ Normal"
            else:
                categoria = "🌧️ Húmeda"

            # --- Mini gráfico SPI mensual
            fig_spi = px.line(df_box, x="Fecha", y="SPI", title="", height=200,
                            color_discrete_sequence=["royalblue"])
            fig_spi.update_layout(
                margin=dict(l=10, r=10, t=20, b=20),
                xaxis_title="",
                yaxis_title="SPI",
                template="simple_white"
            )

            # --- Precipitación anual acumulada
            df_anual = df_box.groupby("Año", as_index=False)["Precipitación"].sum()
            fig_ppt = px.bar(df_anual, x="Año", y="Precipitación",
                            title="📊 Precipitación Anual Acumulada",
                            color_discrete_sequence=["mediumseagreen"],
                            height=250)
            fig_ppt.update_layout(template="plotly_white")

            # --- Layout de tarjetas e indicadores
            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("📉 SPI (mediana)", f"{spi_median:.2f}")
            col2.metric("🧭 Clasificación", categoria)
            col3.metric("🔽 SPI mínimo", f"{spi_min:.2f}")
            col4.metric("🔼 SPI máximo", f"{spi_max:.2f}")
            col5.metric("🌧️ Precipitación total", f"{ppt_total:,.0f} mm")

            # --- Mostrar gráficos
            col6, col7 = st.columns(2)
            with col6:
                st.plotly_chart(fig_spi, use_container_width=True)
            with col7:
                st.plotly_chart(fig_ppt, use_container_width=True)

        elif analisis == "🛠️ Visualizador Personalizado":
            st.markdown("---")
            st.subheader("🛠️ Visualizador de Gráficos Personalizado")

            df_custom = aplicar_filtros(df_box, "grafico_custom")

            # Variables disponibles
            variables_numericas = ["SPI", "Precipitación"]
            variables_x = ["Fecha", "Año", "Mes", "SPI", "Precipitación"]

            colx, coly, coltipo = st.columns(3)

            with colx:
                eje_x = st.selectbox("📌 Eje X:", variables_x, index=0)
            with coly:
                eje_y = st.multiselect("📈 Eje Y (puedes elegir varias):", variables_numericas, default=["SPI"])
            with coltipo:
                tipo = st.radio("📊 Tipo de gráfico:", ["Línea", "Dispersión", "Barras"], horizontal=True)

            # Construcción del gráfico dinámico
            fig = px.line()  # Base vacía

            for y in eje_y:
                if tipo == "Línea":
                    fig.add_scatter(x=df_custom[eje_x], y=df_custom[y], name=y, mode="lines+markers")
                elif tipo == "Dispersión":
                    fig.add_scatter(x=df_custom[eje_x], y=df_custom[y], name=y, mode="markers")
                elif tipo == "Barras":
                    fig.add_bar(x=df_custom[eje_x], y=df_custom[y], name=y)

            fig.update_layout(
                title="📊 Gráfico Personalizado",
                xaxis_title=eje_x,
                yaxis_title="Valor",
                legend_title="Variables",
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")

elif opciones == "📊 Comparar Estaciones":
    st.markdown("# 📊 Comparación Interactiva entre Estaciones")
    st.markdown("Selecciona una o más estaciones para comparar sus métricas climáticas de forma profesional e interactiva.")

    estaciones = ["Estacion 1", "Estacion 2", "Estacion 3", "Estacion 4", "Estacion 5", "Estacion 6"]

    with st.container():
        st.markdown("""
        <style>
        .stMultiSelect>div>div>div {
            background-color: #f7fbff;
            border: 1px solid #dbeaff;
            border-radius: 8px;
            padding: 0.5rem;
        }
        .metric-card {
            background: linear-gradient(to top, #e0f2f7, #f9fbfc);
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s;
        }
        .metric-card:hover {
            transform: scale(1.03);
        }
        .metric-card h5 {
            margin-bottom: 0.3rem;
            color: #1f4e79;
            font-size: 15px;
        }
        .metric-card p {
            font-size: 26px;
            margin: 0;
            font-weight: bold;
            color: #073763;
        }
        .styled-table {
            background-color: #ffffff;
            border-radius: 10px;
            border: 1px solid #dde9f3;
        }
        </style>
        """, unsafe_allow_html=True)

    estaciones_sel = st.multiselect("🎯 Escoge las estaciones a comparar:", estaciones, default=["Estacion 1", "Estacion 2"])

    if not estaciones_sel:
        st.warning("⚠️ Debes seleccionar al menos una estación.")
    else:
        dfs = []
        for est in estaciones_sel:
            try:
                ruta = f"data/{est}/"
                df = pd.read_excel(ruta + "Boxplot precipitacion y spi.xlsx")
                df.rename(columns={"Precipitacion (mm)": "Precipitación", "FECHA": "Fecha"}, inplace=True)
                df["Fecha"] = pd.to_datetime(df["Fecha"])
                df["Año"] = df["Fecha"].dt.year
                df["Mes"] = df["Fecha"].dt.month_name()
                df["Estación"] = est
                dfs.append(df)
            except Exception as e:
                st.error(f"❌ Error al cargar datos de {est}: {e}")

        if dfs:
            df_total = pd.concat(dfs)

            with st.expander("🎛️ Filtros globales para la comparación"):
                col1, col2 = st.columns(2)
                with col1:
                    años = st.multiselect("Años", sorted(df_total["Año"].unique()), default=sorted(df_total["Año"].unique()))
                with col2:
                    meses = st.multiselect("Meses", df_total["Mes"].unique(), default=df_total["Mes"].unique())

            df_total = df_total[(df_total["Año"].isin(años)) & (df_total["Mes"].isin(meses))]
            
            
            # Agrega después de aplicar filtros globales:
            resumen = df_total.groupby("Estación")[["SPI", "Precipitación"]].agg({
                "SPI": ["median", "min", "max"],
                "Precipitación": ["mean", "median", "min", "max"]
            }).round(2)
            resumen.columns = ["_".join(col).strip() for col in resumen.columns.values]
            resumen.reset_index(inplace=True)

            comparacion = st.selectbox("📌 Elige el tipo de comparación que deseas visualizar:", [
                "📈 Tabla resumen de métricas",
                "📦 Boxplots SPI y Precipitación",
                "📉 Serie temporal SPI promedio",
                "🌧️ Precipitación anual acumulada",
                "🧭 Panel comparativo por estación",
                "🔥 Mapa de calor de métricas por estación"
            ])

            if comparacion == "📈 Tabla resumen de métricas":
                st.markdown("## 📋 Tabla Resumen Estadístico")
                resumen = df_total.groupby("Estación")[["SPI", "Precipitación"]].agg({
                    "SPI": ["median", "min", "max"],
                    "Precipitación": ["mean", "median", "min", "max"]
                }).round(2)
                resumen.columns = ["_".join(col).strip() for col in resumen.columns.values]
                resumen.reset_index(inplace=True)
                st.dataframe(resumen.style.set_properties(**{
                    'background-color': '#f4faff',
                    'color': '#002c4d',
                    'border-color': '#dee6f0',
                    'font-size': '16px',
                    'font-weight': '500'
                }), use_container_width=True)

                # Interpretación automática
                try:
                    est_humeda = resumen.loc[resumen["Precipitación_mean"].idxmax(), "Estación"]
                    est_spi_ext = resumen.loc[resumen["SPI_max"].idxmax(), "Estación"]
                    est_spi_sec = resumen.loc[resumen["SPI_min"].idxmin(), "Estación"]
                    st.success(f"📌 La estación con mayor precipitación promedio es **{est_humeda}**.\n\n📈 El SPI más alto fue registrado en **{est_spi_ext}** y el más bajo en **{est_spi_sec}**.")
                except:
                    st.info("No se pudo generar interpretación automática.")

            elif comparacion == "📦 Boxplots SPI y Precipitación":
                st.subheader("📦 Boxplot de SPI por Estación")
                fig_spi = px.box(df_total, x="Estación", y="SPI", color="Estación")
                st.plotly_chart(fig_spi, use_container_width=True)

                st.subheader("📦 Boxplot de Precipitación por Estación")
                fig_ppt = px.box(df_total, x="Estación", y="Precipitación", color="Estación")
                st.plotly_chart(fig_ppt, use_container_width=True)

            elif comparacion == "📉 Serie temporal SPI promedio":
                st.subheader("📉 SPI Promedio Anual por Estación")
                df_linea = df_total.groupby(["Año", "Estación"], as_index=False)["SPI"].mean()
                fig_linea = px.line(df_linea, x="Año", y="SPI", color="Estación", markers=True)
                st.plotly_chart(fig_linea, use_container_width=True)

            elif comparacion == "🌧️ Precipitación anual acumulada":
                st.subheader("🌧️ Precipitación Total Anual por Estación")
                df_bar = df_total.groupby(["Año", "Estación"], as_index=False)["Precipitación"].sum()
                fig_bar = px.bar(df_bar, x="Año", y="Precipitación", color="Estación", barmode="group")
                st.plotly_chart(fig_bar, use_container_width=True)

            elif comparacion == "🧭 Panel comparativo por estación":
                st.markdown("---")
                st.markdown("## 🧭 Panel Comparativo Profesional")
                colsets = st.columns(len(estaciones_sel))
                for i, est in enumerate(estaciones_sel):
                    sub = df_total[df_total["Estación"] == est]
                    spi_median = sub["SPI"].median()
                    ppt_total = sub["Precipitación"].sum()
                    categoria = "🌵 Seca" if spi_median <= -1 else "🌤️ Normal" if spi_median < 1 else "🌧️ Húmeda"
                    with colsets[i]:
                        st.markdown(f"### {est}")
                        st.markdown(f"<div class='metric-card'><h5>SPI Mediana</h5><p>{spi_median:.2f}</p></div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='metric-card'><h5>Clasificación</h5><p>{categoria}</p></div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='metric-card'><h5>Precipitación Total</h5><p>{ppt_total:,.0f} mm</p></div>", unsafe_allow_html=True)

            elif comparacion == "🔥 Mapa de calor de métricas por estación":
                st.subheader("🔥 Comparación Visual con Mapa de Calor")

                resumen_heat = resumen.set_index("Estación").copy()

                fig_heatmap = px.imshow(
                    resumen_heat,
                    text_auto=True,
                    color_continuous_scale="YlGnBu",
                    aspect="auto",
                    labels=dict(color="Valor"),
                    height=500
                )

                fig_heatmap.update_layout(
                    template="plotly_white",
                    title="🔍 Comparación Numérica de Métricas por Estación",
                    xaxis_title="Métrica",
                    yaxis_title="Estación",
                    font=dict(size=14)
                )

                st.plotly_chart(fig_heatmap, use_container_width=True)

                # Botón de descarga
                import io
                buf = io.BytesIO()
                fig_heatmap.write_image(buf, format="png")
                st.download_button("📥 Descargar mapa de calor como PNG", data=buf.getvalue(), file_name="heatmap_estaciones.png")


elif opciones == "🌊 Wavelet":
    st.title("🌊 Análisis Wavelet por Estación (con PyWavelets)")

    import os
    import pandas as pd
    import numpy as np
    import pywt
    import matplotlib.pyplot as plt
    import io

    # === Estaciones disponibles ===
    estaciones = ["Estacion 1", "Estacion 2", "Estacion 3", "Estacion 4", "Estacion 5", "Estacion 6"]
    estacion_sel = st.selectbox("📍 Selecciona una estación:", estaciones)

    base_path = "data"
    archivo = os.path.join(base_path, estacion_sel, "wavelet 1.xlsx")

    if not os.path.exists(archivo):
        st.error("❌ No se encontró el archivo wavelet 1.xlsx para la estación seleccionada.")
    else:
        try:
            df = pd.read_excel(archivo)
            df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
            df = df.dropna(subset=["FECHA"])
            df = df.sort_values("FECHA")

            # Variables numéricas disponibles
            variables = df.select_dtypes(include="number").columns.tolist()
            if not variables:
                st.warning("⚠️ No hay variables numéricas para analizar.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    variable = st.selectbox("📊 Variable a analizar:", variables)
                with col2:
                    wavelet_type = st.selectbox("🌐 Tipo de wavelet:", ["mexh", "gaus1", "gaus2", "morl"], index=0)

                col3, col4 = st.columns(2)
                with col3:
                    num_escala = st.slider("🔍 Número de escalas", min_value=32, max_value=256, value=128, step=16)
                with col4:
                    colormap = st.selectbox("🎨 Paleta de colores", ["coolwarm", "viridis", "plasma", "inferno", "cividis"], index=0)

                signal = df[variable].interpolate(method="linear").fillna(method="bfill").values
                t = np.arange(len(signal))

                # --- Serie original ---
                fig2, ax2 = plt.subplots(figsize=(10, 3))
                ax2.plot(df["FECHA"], signal, color="steelblue")
                ax2.set_title(f"Serie Temporal Original - {variable}")
                ax2.set_xlabel("Fecha")
                ax2.set_ylabel(variable)
                ax2.grid(True)
                st.pyplot(fig2)

                # --- Transformada Wavelet Continua ---
                scales = np.arange(1, num_escala)
                coef, freqs = pywt.cwt(signal, scales, wavelet=wavelet_type)

                fig, ax = plt.subplots(figsize=(10, 5))
                im = ax.imshow(
                    np.abs(coef),
                    extent=[t[0], t[-1], scales[-1], scales[0]],
                    cmap=colormap,
                    aspect='auto',
                    vmax=np.percentile(np.abs(coef), 99)
                )
                ax.set_title(f"Wavelet Transform ({variable}) - {wavelet_type}")
                ax.set_ylabel("Escala")
                ax.set_xlabel("Índice de Tiempo")
                ax.invert_yaxis()
                fig.colorbar(im, ax=ax, label="Magnitud")

                st.pyplot(fig)

                # --- Descargar imagen ---
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                st.download_button("📅 Descargar gráfico Wavelet", buf.getvalue(), file_name=f"wavelet_{estacion_sel}_{variable}.png", mime="image/png")

                # --- Explicación ---
                with st.expander("ℹ️ ¿Qué muestra este gráfico Wavelet?"):
                    st.markdown("""
                    - La **transformada wavelet continua** permite identificar patrones periódicos o multiescalares.
                    - Las **escalas más bajas** detectan eventos de alta frecuencia (cambios rápidos).
                    - Las **escalas más altas** detectan patrones a largo plazo (tendencias).
                    - El color indica la **magnitud de la energía** en esa escala y momento.
                    """)
        except Exception as e:
            st.error(f"❌ Error al procesar el análisis Wavelet: {e}")

# --- NDVI y SPI ---
elif opciones == "🌿 NDVI - Análisis Anual":
    st.title("🌿 Análisis Dinámico del NDVI Promedio Anual (1992–2022)")

    # --- Estilo personalizado ---
    st.markdown("""
        <style>
        .main { background-color: #f5faff; }
        h1, h2, h3, h4 { color: #003366; }
        .stMetric { font-size: 18px !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- Cargar datos ---
    df_ndvi = pd.read_excel("data/NDVI/NDVI anual.xlsx")
    df_ndvi = df_ndvi[["Año", "NDVI Anual"]].dropna()

    # --- Tabs ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 KPIs", "📈 Evolución NDVI", "🚨 Anomalías",
        "🔢 Comparación de Periodos", "🧐 Conclusiones"
    ])

    # TAB 1: KPIs
    with tab1:
        st.subheader("📊 Indicadores Clave")
        rango = st.slider("Selecciona el periodo de análisis:", int(df_ndvi["Año"].min()), int(df_ndvi["Año"].max()), value=(1992, 2022))
        df_filtrado = df_ndvi[(df_ndvi["Año"] >= rango[0]) & (df_ndvi["Año"] <= rango[1])]

        # Filtro de NDVI por umbral
        ndvi_min, ndvi_max = st.slider("Filtrar NDVI entre:", 0.0, 1.0, (0.2, 0.8))
        df_filtrado = df_filtrado[(df_filtrado["NDVI Anual"] >= ndvi_min) & (df_filtrado["NDVI Anual"] <= ndvi_max)]

        promedio = df_filtrado["NDVI Anual"].mean()
        minimo = df_filtrado["NDVI Anual"].min()
        maximo = df_filtrado["NDVI Anual"].max()
        std = df_filtrado["NDVI Anual"].std()
        tendencia = "⬆️ Ascendente" if df_filtrado["NDVI Anual"].iloc[-1] > df_filtrado["NDVI Anual"].iloc[0] else "⬇️ Descendente"

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Promedio", f"{promedio:.3f}")
        col2.metric("Mínimo", f"{minimo:.3f}")
        col3.metric("Máximo", f"{maximo:.3f}")
        col4.metric("Desviación", f"{std:.3f}")
        col5.metric("Tendencia", tendencia)

        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Descargar datos como CSV", csv, "ndvi_filtrado.csv", "text/csv")

    # TAB 2: Evolución NDVI
    with tab2:
        st.subheader("📈 Evolución del NDVI con Análisis de Tendencia")

        # Ajuste lineal
        fig_line = px.scatter(df_filtrado, x="Año", y="NDVI Anual", trendline="ols",
                              title="NDVI Promedio Anual con Ajuste Lineal",
                              labels={"NDVI Anual": "NDVI"}, color_discrete_sequence=["#2e8b57"])
        fig_line.update_traces(marker=dict(size=8))
        st.plotly_chart(fig_line, use_container_width=True)

        # Histograma
        if st.toggle("Mostrar histograma de NDVI"):
            fig_hist = px.histogram(df_filtrado, x="NDVI Anual", nbins=10,
                                    title="Distribución de NDVI", color_discrete_sequence=["#4682b4"])
            st.plotly_chart(fig_hist, use_container_width=True)

        # 📊 Animación impactante del NDVI anual
                # 📽️ Animación personalizada del NDVI anual
        # 📽️ Animación estilizada del NDVI anual (versión final)
        st.markdown("### 🎞️ Animación Visual del NDVI Promedio Anual")
        st.markdown(
            "Explora visualmente la evolución del NDVI año por año con una presentación clara, estilizada y profesional."
        )

        # Preparar datos
        df_anim = df_filtrado.copy()
        df_anim["NDVI Etiqueta"] = df_anim["NDVI Anual"].apply(lambda x: f"{x:.3f}")

        # Crear animación de una sola barra por año
        fig_anim = px.bar(
            df_anim,
            x=["NDVI"] * len(df_anim),
            y="NDVI Anual",
            animation_frame="Año",
            text="NDVI Etiqueta",
            range_y=[0, 1],
            color="NDVI Anual",
            color_continuous_scale="Viridis",
            title="🌿 Evolución Anual del NDVI",
            labels={"NDVI Anual": "NDVI"}
        )

        # Estilo profesional
        fig_anim.update_layout(
            height=500,
            margin=dict(t=60, b=30, l=40, r=40),
            plot_bgcolor="#f4faff",
            paper_bgcolor="#f4faff",
            font=dict(family="Segoe UI", size=16, color="#003366"),
            xaxis=dict(showticklabels=False),
            coloraxis_showscale=False,
            showlegend=False,
            transition={"duration": 500, "easing": "linear"}
        )

        # Estética de las barras
        fig_anim.update_traces(
            textposition="outside",
            marker_line_color="#003366",
            marker_line_width=2
        )

        # Mostrar animación
        st.plotly_chart(fig_anim, use_container_width=True)




    # TAB 3: Anomalías
    with tab3:
        st.subheader("🚨 Detección Automática de Anomalías")
        media = promedio
        df_filtrado["Anómalo"] = df_filtrado["NDVI Anual"].apply(
            lambda x: "🔴 Muy bajo" if x < media - std else ("🟢 Muy alto" if x > media + std else "⚪ Normal")
        )
        st.dataframe(df_filtrado[["Año", "NDVI Anual", "Anómalo"]], use_container_width=True)

        fig_ano = px.line(df_filtrado, x="Año", y="NDVI Anual", markers=True,
                          title="Análisis Temporal del NDVI con Anotaciones")
        for _, row in df_filtrado.iterrows():
            if row["Anómalo"] != "⚪ Normal":
                fig_ano.add_annotation(x=row["Año"], y=row["NDVI Anual"], text=row["Anómalo"],
                                       showarrow=True, arrowhead=1, ax=0, ay=-30, bgcolor="#f9f9f9")
        st.plotly_chart(fig_ano, use_container_width=True)

    # TAB 4: Comparación de Periodos
    with tab4:
        st.subheader("Comparador Interactivo de Periodos")
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.slider("Periodo 1", min_value=rango[0], max_value=rango[1], value=(1992, 2005))
        with col2:
            p2 = st.slider("Periodo 2", min_value=rango[0], max_value=rango[1], value=(2006, 2022))

        df_p1 = df_ndvi[(df_ndvi["Año"] >= p1[0]) & (df_ndvi["Año"] <= p1[1])]
        df_p2 = df_ndvi[(df_ndvi["Año"] >= p2[0]) & (df_ndvi["Año"] <= p2[1])]

        c1, c2 = st.columns(2)
        c1.metric("Promedio P1", f"{df_p1['NDVI Anual'].mean():.3f}")
        c2.metric("Promedio P2", f"{df_p2['NDVI Anual'].mean():.3f}")

        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(px.line(df_p1, x="Año", y="NDVI Anual", title="NDVI - Periodo 1"), use_container_width=True)
        with col4:
            st.plotly_chart(px.line(df_p2, x="Año", y="NDVI Anual", title="NDVI - Periodo 2"), use_container_width=True)

    # TAB 5: Conclusiones
    with tab5:
        st.subheader("🧐 Conclusión Automatizada del Análisis")

        if promedio < 0.4:
            st.warning("El NDVI promedio es bajo. Posible degradación o pérdida de vegetación.")
        elif promedio > 0.6:
            st.success("El NDVI promedio es alto. Vegetación saludable en el periodo analizado.")
        else:
            st.info("NDVI en nivel moderado. Sin cambios extremos, pero debe mantenerse vigilancia.")

        st.markdown("#### 🔹 Recomendaciones:")
        st.markdown("- Monitoreo continuo anual con datos satelitales actualizados.")
        st.markdown("- Complementar con variables climáticas (SPI, temperatura, humedad).")
        st.markdown("- Realizar análisis espacial si se cuenta con datos raster por zonas.")

        comentario = st.text_area("💬 Anotaciones del analista (opcional):", placeholder="Escribe tus observaciones...")



# --- Correlaciones ---
elif opciones == "📊 Correlaciones":
    st.markdown("# 📊 Matriz de Correlación entre Variables Climáticas")
    st.markdown("Explora las relaciones estadísticas entre precipitación, temperatura, humedad y SPI por estación o comparando dos.")

    estaciones = ["Estacion 1", "Estacion 2", "Estacion 3", "Estacion 4", "Estacion 5", "Estacion 6"]
    modo = st.radio(
        "🔍 ¿Qué deseas hacer?",
        [
            "🔹 Ver una sola estación",
            "🔸 Comparar dos estaciones",
            "📽️ Heatmap Animado por Año"
        ],
        horizontal=True
    )


    if modo == "🔹 Ver una sola estación":
        estacion_sel = st.selectbox("📍 Selecciona la estación", estaciones)

        try:
            ruta = f"data/{estacion_sel}/Heatmap de correlación.xlsx"
            df_corr = pd.read_excel(ruta)
            df_numeric = df_corr.select_dtypes(include='number')
            variables_disponibles = df_numeric.columns.tolist()

            with st.expander("🎛️ Filtros de variables para correlación", expanded=False):
                st.markdown("""
                    <style>
                    .stMultiSelect>div>div>div {
                        background-color: #ffffff !important;
                        border-radius: 6px;
                        border: 1px solid #c7dbf4 !important;
                        font-size: 15px !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                seleccion = st.multiselect(
                    label="📌 Selecciona variables numéricas:",
                    options=variables_disponibles,
                    default=variables_disponibles,
                    key="filtro_variables_corr"
                )


            if len(seleccion) < 2:
                st.warning("⚠️ Selecciona al menos dos variables para mostrar la matriz.")
            else:
                matriz = df_corr[seleccion].corr().round(2)

                fig = px.imshow(
                    matriz,
                    text_auto=True,
                    color_continuous_scale="RdBu_r",
                    zmin=-1,
                    zmax=1,
                    aspect="auto",
                    labels=dict(color="Correlación"),
                    title=f"🔗 Correlación - {estacion_sel}"
                )
                fig.update_layout(template="plotly_white", height=500)
                st.plotly_chart(fig, use_container_width=True, key=f"cor_{estacion_sel}")


            # Descargar
            import io
            buf = io.BytesIO()
            fig.write_image(buf, format="png")
            st.download_button(
                label="📥 Descargar como PNG",
                data=buf.getvalue(),
                file_name=f"correlacion_{estacion_sel}.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"❌ Error al cargar la correlación de {estacion_sel}: {e}")

    elif modo == "🔸 Comparar dos estaciones":
        col1, col2 = st.columns(2)
        with col1:
            est1 = st.selectbox("📌 Estación A", estaciones, key="select_a")
        with col2:
            est2 = st.selectbox("📌 Estación B", estaciones, key="select_b")

        with st.expander("🎛️ Filtrar variables a comparar", expanded=False):
            try:
                df_tmp = pd.read_excel(f"data/{est1}/Heatmap de correlación.xlsx")
                variables_numericas = df_tmp.select_dtypes(include='number').columns.tolist()
                seleccion_vars = st.multiselect(
                    "🔢 Selecciona las variables numéricas a comparar",
                    options=variables_numericas,
                    default=variables_numericas,
                    key="vars_comparar"
                )
            except:
                seleccion_vars = []
                st.warning("⚠️ No se pudieron cargar las variables disponibles.")

        try:
            def cargar_corr(est):
                df = pd.read_excel(f"data/{est}/Heatmap de correlación.xlsx")
                df = df[seleccion_vars] if seleccion_vars else df.select_dtypes(include='number')
                return df.corr().round(2)

            corr1 = cargar_corr(est1)
            corr2 = cargar_corr(est2)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### 🔷 {est1}")
                fig1 = px.imshow(corr1, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
                fig1.update_layout(template="plotly_white", title="", height=400)
                st.plotly_chart(fig1, use_container_width=True, key=f"plot_{est1}_1")

            with col2:
                st.markdown(f"### 🔶 {est2}")
                fig2 = px.imshow(corr2, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
                fig2.update_layout(template="plotly_white", title="", height=400)
                st.plotly_chart(fig2, use_container_width=True, key=f"plot_{est2}_2")

        except Exception as e:
            st.error(f"❌ Error al comparar estaciones: {e}")
            

    elif modo == "📽️ Heatmap Animado por Año":
        st.markdown("## 📽️ Evolución Temporal de Correlaciones")
        estacion_sel = st.selectbox("🎯 Selecciona la estación para animación", estaciones, key="est_anim")

        try:
            ruta = f"data/{estacion_sel}/Heatmap de correlación.xlsx"
            df = pd.read_excel(ruta)

            # Crear FECHA si no existe
            if "FECHA" not in df.columns:
                if "Año" in df.columns and "Mes" in df.columns:
                    meses_es = {
                        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
                        "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
                        "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
                    }
                    df["Mes_num"] = df["Mes"].map(meses_es)
                    df["FECHA"] = pd.to_datetime(
                        df["Año"].astype(str) + "-" + df["Mes_num"].astype(str).str.zfill(2) + "-01",
                        format="%Y-%m-%d", errors="coerce"
                    )

            df["Fecha"] = pd.to_datetime(df["FECHA"], errors="coerce")
            df["Año"] = df["Fecha"].dt.year
            df.drop(columns=["FECHA", "Mes_num"], inplace=True, errors="ignore")

            # Variables numéricas
            variables = df.select_dtypes(include="number").columns.tolist()
            selected_vars = st.multiselect("📊 Variables a incluir", variables, default=variables)
            
            df = df.dropna(subset=["Precipitacion (mm)", "Temperatura (°C)", "Humedad (%)", "SPI"])

            years = sorted(df["Año"].dropna().unique())

            # Controles de animación
            col_a, col_b, col_c = st.columns([1, 1, 2])
            with col_a:
                run_animation = st.checkbox("▶️ Animar automáticamente", value=False)
            with col_b:
                anim_speed = st.slider("⏱️ Velocidad", 0.3, 2.0, value=1.0, step=0.1)
            with col_c:
                año_manual = st.selectbox("📅 Ver año específico", years, key="año_manual")

            placeholder = st.empty()

            if run_animation:
                
                st.info("🔁 Animación automática activa")

                direccion = st.radio("↔️ Dirección de la animación:", ["↪️ Adelante", "↩️ Atrás"], horizontal=True)
                start_idx = years.index(año_manual)

                if direccion == "↪️ Adelante":
                    años_animados = years[start_idx:]
                else:
                    años_animados = list(reversed(years[:start_idx + 1]))

                for year in años_animados:
                    df_year = df[df["Año"] == year]
                    if len(df_year) >= 2 and all(var in df_year.columns for var in selected_vars):
                        corr = df_year[selected_vars].corr().dropna(axis=1, how='all').dropna(axis=0, how='all')
                        if not corr.empty:
                            fig = px.imshow(
                                corr,
                                text_auto=True,
                                color_continuous_scale="RdBu_r",
                                zmin=-1, zmax=1,
                                title=f"🔗 Correlaciones - {estacion_sel} ({year})"
                            )
                            fig.update_layout(template="plotly_white", height=500)
                            placeholder.plotly_chart(fig, use_container_width=True)
                            time.sleep(anim_speed)
                        else:
                            st.text(f"[DEBUG] Año {year} tiene {len(df_year)} filas válidas.")
                            st.text(f"[DEBUG] Variables numéricas: {df_year[selected_vars].columns.tolist()}")

                            st.warning(f"⚠️ No hay correlaciones válidas en {year} para {estacion_sel}.")

            else:
    # Mostrar solo un año manual
                df_year = df[df["Año"] == año_manual]
                df_year_clean = df_year[selected_vars].dropna()

                if df_year_clean.shape[0] >= 2:
                    corr = df_year_clean.corr().round(2)
                    fig = px.imshow(
                        corr,
                        text_auto=True,
                        color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1,
                        title=f"🔗 Correlaciones - {estacion_sel} ({año_manual})"
                    )
                    fig.update_layout(template="plotly_white", height=500)
                    placeholder.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No hay datos suficientes para ese año.")

        except Exception as e:
            st.error(f"❌ Error al generar el heatmap animado: {e}")





# --- Análisis Wavelet ---
elif opciones == "🗺️ Mapa Interactivo":
    st.title("📍 Estaciones Meteorológicas en el Chocó Andino")

    import streamlit as st
    import pandas as pd
    import json
    import pydeck as pdk
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    
    # === Coordenadas ===
    estaciones_coords = {
        "Estación 1": {"coord": (-78.4869, 1.1538)},
        "Estación 2": {"coord": (-78.8486, 1.1657)},
        "Estación 3": {"coord": (-78.9639, 0.7483)},
        "Estación 4": {"coord": (-79.8566, 0.5698)},
        "Estación 5": {"coord": (-79.1721, 0.3316)},
        "Estación 6": {"coord": (-79.2675, 0.1138)},
    }

    # === Selección de variable ===
    variable_opciones = {
        "Precipitación": "Precipitacion (mm)",
        "SPI": "SPI",
        "Temperatura": "Temperatura (Â°C)",
        "Humedad": "Humedad (%)"
    }
    variable_amigable = st.selectbox("Selecciona la variable:", list(variable_opciones.keys()))
    variable = variable_opciones[variable_amigable]

    # === Cargar datos desde Excel ===
    base_path = "data"
    datos_estaciones = {}
    for nombre, info in estaciones_coords.items():
        estacion_num = nombre.split(" ")[-1]
        archivo = f"{base_path}/Estacion {estacion_num}/Resumen_Anual.xlsx"
        try:
            df = pd.read_excel(archivo)
            datos_estaciones[nombre] = df
        except:
            continue

    año_seleccionado = st.slider(
        "Selecciona el año:",
        min_value=1992,
        max_value=2022,
        value=1992,
        step=1,
        format="%d"
    )

    # === Rango y color ===
    valores = []
    for df in datos_estaciones.values():
        if variable in df.columns:
            valores.extend(df[variable].dropna().values)

    if not valores:
        st.warning(f"No se encontraron datos para la variable '{variable_amigable}' en los archivos cargados.")
        st.stop()

    min_val, max_val = min(valores), max(valores)
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    cmap = plt.get_cmap("RdYlBu")

    # === Datos de estaciones para el mapa ===
    # === Preparar estaciones con criticidad ===
    stations_data = []
    estaciones_temporales = []

    for nombre, info in estaciones_coords.items():
        lat, lon = info["coord"][1], info["coord"][0]
        df = datos_estaciones.get(nombre)
        if df is not None and año_seleccionado in df["Año"].values:
            row = df[df["Año"] == año_seleccionado]
            if not row.empty and variable in row.columns:
                valor = row[variable].values[0]

                # Calcular criticidad
                if variable == "SPI":
                    criticidad = abs(valor)
                elif variable == "Humedad (%)":
                    criticidad = max(0, valor - 90)
                elif variable == "Temperatura (Â°C)":
                    criticidad = max(0, valor - 25)
                else:
                    criticidad = 0

                estaciones_temporales.append((nombre, criticidad, lat, lon, valor, df))

    # === Determinar estaciones más y menos críticas ===
    if estaciones_temporales:
        max_critica = max(estaciones_temporales, key=lambda x: x[1])[0]
        min_critica = min(estaciones_temporales, key=lambda x: x[1])[0]

        # === Asignar colores e íconos ===
        for nombre, criticidad, lat, lon, valor, df in estaciones_temporales:
            # Colores según condición
            if variable == "SPI" and valor <= -1:
                color = [255, 0, 0, 255]
            elif variable == "SPI" and valor >= 1:
                color = [0, 0, 200, 255]
            elif variable == "Humedad (%)" and valor >= 90:
                color = [128, 0, 128, 255]
            elif variable == "Temperatura (Â°C)" and valor >= 25:
                color = [255, 215, 0, 255]
            else:
                rgba_float = mcolors.to_rgba(cmap(norm(valor)))
                color = [int(x * 255) for x in rgba_float]

            # Íconos personalizados
            if nombre == max_critica:
                icono_usar = {
                    "url": "https://cdn-icons-png.flaticon.com/512/564/564619.png",  # peligro máximo
                    "width": 128, "height": 128, "anchorY": 128
                }
            elif nombre == min_critica:
                icono_usar = {
                    "url": "https://cdn-icons-png.flaticon.com/512/190/190411.png",  # leve alerta
                    "width": 128, "height": 128, "anchorY": 128
                }
            else:
                icono_usar = {
                    "url": "https://cdn-icons-png.flaticon.com/512/252/252035.png",  # estación normal
                    "width": 128, "height": 128, "anchorY": 128
                }

            # Agregar estación al mapa
            stations_data.append({
                "name": nombre,
                "latitude": lat,
                "longitude": lon,
                "elevation": 10000,
                "color": color,
                "value": round(valor, 2),
                "año": año_seleccionado,
                "icon_data": icono_usar
            })


    # === Capa: estaciones (círculo grande) ===
    station_layer = pdk.Layer(
        "ScatterplotLayer",
        stations_data,
        get_position=["longitude", "latitude"],
        get_elevation="elevation",
        get_fill_color="color",
        get_radius=2500,
        radius_min_pixels=4,
        pickable=True,
    )

    # === Capa: ícono de estación meteorológica ===
    icon_layer = pdk.Layer(
        "IconLayer",
        stations_data,
        get_icon="icon_data",
        get_position=["longitude", "latitude"],
        get_size=8,           # Aumentado
        size_scale=10,
        pickable=True
    )

    # === Capa: polígono (Chocó Andino) ===
    with open(f"{base_path}/choco_andino_export.geojson", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    polygon_layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        stroked=True,
        filled=True,
        extruded=False,
        get_fill_color="[102, 189, 99, 50]",  # verde claro con transparencia
        get_line_color=[26, 152, 80],
        get_line_width=2,
        pickable=False,
    )

    # === Vista 3D ===
    view_state = pdk.ViewState(
        latitude=0.6,
        longitude=-79,
        zoom=8,
        pitch=50,
        bearing=0
    )

    # === Renderizar todas las capas ===
    r = pdk.Deck(
        layers=[polygon_layer, station_layer, icon_layer],
        initial_view_state=view_state,
        map_style="light",
        tooltip={
            "html": "<b>{name}</b><br>Valor: {value}<br>Año: {año}",
            "style": {"backgroundColor": "rgba(0, 0, 0, 0.7)", "color": "white"}
        }
    )

    # Mostrar el mapa 3D y capturar eventos de clic
    deck_event = st.pydeck_chart(r)

# === Crear columnas para leyenda y tabla ===
    col1, col2 = st.columns([1, 1])

    # === Columna izquierda: leyenda de colores ===
    with col1:
        st.markdown("#### 🎨 Leyenda")
        fig, ax = plt.subplots(figsize=(3.5, 0.3))
        fig.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.3)

        cbar = plt.colorbar(
            plt.cm.ScalarMappable(norm=norm, cmap=cmap),
            cax=ax,
            orientation='horizontal'
        )
        cbar.set_label(f"{variable_amigable} ({round(min_val, 2)} - {round(max_val, 2)})", fontsize=8)
        cbar.ax.tick_params(labelsize=6)

        st.pyplot(fig)

    # === Columna derecha: tabla de estación seleccionada ===
    with col2:
        estacion_seleccionada = st.selectbox("Selecciona una estación para ver sus datos:", list(datos_estaciones.keys()))
        df = datos_estaciones[estacion_seleccionada]
        df_año = df[df["Año"] == año_seleccionado]

        st.markdown(f"### 📊 Detalles de {estacion_seleccionada} - {año_seleccionado}")
        st.dataframe(df_año)

