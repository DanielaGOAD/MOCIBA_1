import streamlit as st
import pandas as pd
import io
import gdown

# --- Grupo 1: Uso de medidas de seguridad
uso_medidas_de_seguridad = {
    "P1": "En la ciudad"
}

# --- Grupo 2: Medidas de seguridad
medidas_de_seguridad = {
    "P2_1": "crear o poner contraseñas (claves, huella digital, patrón, etcétera)",
    "P2_2": "Instalar o actualizar programas antivirus, cortafuegos o antiespías",
    "P2_3": "Bloquear ventanas emergentes del navegador",
    "P2_4": "Cambiar periódicamente las contraseñas.",
    "P2_5": "No ingresar a sitios web inseguros o páginas desconocidas",
    "P2_6": "No abrir ni guardar archivos que envían personas desconocidas",
    "P2_7": "No publicar su correo o número telefónico en redes sociales",
    "P2_8": "Otra"
}

@st.cache_data(show_spinner="Cargando datos desde Google Drive...")
def cargar_datos_base():
    file_ids = [
        "1ojZcLZost0BM00yCGN8OLnu7XYyLpEYr"
    ]

    columnas = (
        ["ANIO", "CVE_ENT", "NOM_ENT", "SEXO", "FACTOR"]
        + list(uso_medidas_de_seguridad.keys())
        + list(medidas_de_seguridad.keys())
    )

    dfs = []

    for file_id in file_ids:
        url = f"https://drive.google.com/uc?id={file_id}"
        output = io.BytesIO()
        gdown.download(url, output, quiet=True)
        output.seek(0)

        df_temp = pd.read_csv(
            output,
            encoding="latin1",
            usecols=columnas,
            low_memory=False
        )
        dfs.append(df_temp)

    df_final = pd.concat(dfs, ignore_index=True)
    
    todas_preguntas = list(uso_medidas_de_seguridad.keys()) + list(medidas_de_seguridad.keys())
    for col in todas_preguntas:
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
        
    return df_final

df = cargar_datos_base()

st.title("📊 MOCIBA - Comparativa de Entidades")

tipo_variable = st.radio(
    "Seleccione el indicador",
    ["Uso de medidas de seguridad", "Medidas de seguridad"]
)

if tipo_variable == "Uso de medidas de seguridad":
    opciones = uso_medidas_de_seguridad
else:
    opciones = medidas_de_seguridad

variable = st.selectbox(
    "Seleccione la variable",
    list(opciones.values())
)

variable_col = [k for k, v in opciones.items() if v == variable][0]

sexo = st.selectbox("Sexo", ["Total", "Hombres", "Mujeres"])

# --- NUEVA SECCIÓN: Selección de dos estados para comparar ---
estados_unicos = sorted([x for x in df["NOM_ENT"].dropna().unique()])
opciones_estado = ["NACIONAL"] + estados_unicos

col1, col2 = st.columns(2)

with col1:
    estado_1 = st.selectbox("Estado 1 (comparar contra)", opciones_estado, index=0)

with col2:
    estado_2 = st.selectbox("Estado 2 (comparar contra)", opciones_estado, index=1 if len(opciones_estado) > 1 else 0)

# Validación: si seleccionan el mismo estado en ambos
if estado_1 == estado_2:
    st.warning("⚠️ Has seleccionado el mismo estado en ambos lados. Selecciona dos estados diferentes para comparar.")


def calcular_porcentaje(df, variable, sexo, estado):
    """Calcula el porcentaje por año para un estado específico."""
    if sexo == "Hombres":
        df_filtrado = df[df["SEXO"] == 1].copy()
    elif sexo == "Mujeres":
        df_filtrado = df[df["SEXO"] == 2].copy()
    else:
        df_filtrado = df[df["SEXO"].isin([1, 2])].copy()

    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]

    resultados = []
    for anio, grupo in df_filtrado.groupby("ANIO"):
        numerador = grupo.loc[grupo[variable] == 1, "FACTOR"].sum()
        denominador = grupo.loc[grupo[variable].isin([1, 2]), "FACTOR"].sum()

        if denominador > 0:
            porcentaje = (numerador / denominador) * 100
        else:
            porcentaje = 0.0

        resultados.append({
            "ANIO": anio,
            "PORCENTAJE": round(porcentaje, 2)
        })

    return pd.DataFrame(resultados)


# --- Solo ejecutar si los estados son diferentes ---
if estado_1 != estado_2:
    resultado_1 = calcular_porcentaje(df, variable_col, sexo, estado_1)
    resultado_2 = calcular_porcentaje(df, variable_col, sexo, estado_2)

    # Unir los dos resultados por año (outer join para no perder años)
    comparativa = pd.merge(
        resultado_1, resultado_2,
        on="ANIO", how="outer", suffixes=(f"_{estado_1}", f"_{estado_2}")
    ).fillna(0)

    # Renombrar columnas para que se vean más limpias
    comparativa = comparativa.rename(columns={
        f"PORCENTAJE_{estado_1}": estado_1,
        f"PORCENTAJE_{estado_2}": estado_2
    })

    # Ordenar columnas: ANIO, Estado1, Estado2
    comparativa = comparativa[["ANIO", estado_1, estado_2]]

    # Calcular diferencia entre ambos estados
    comparativa["Diferencia (pp)"] = round(comparativa[estado_1] - comparativa[estado_2], 2)

    st.subheader(f"Comparativa: {variable}")
    st.dataframe(comparativa, use_container_width=True)

    # --- Gráfico comparativo con dos líneas ---
    # Streamlit necesita el dataframe en formato "largo" para graficar múltiples series
    grafico_data = comparativa.melt(
        id_vars=["ANIO"],
        value_vars=[estado_1, estado_2],
        var_name="Entidad",
        value_name="Porcentaje"
    )

    st.line_chart(
        grafico_data,
        x="ANIO",
        y="Porcentaje",
        color="Entidad",
        y_label="Porcentaje (%)",
        x_label="Año"
    )
