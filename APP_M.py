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

# --- Grupo 3: Ciberacoso
ciberacoso = {
    "CUALQUIERA": "Cualquiera de las anteriores (Ciberacoso general)",
    "P4_01": "Recibir correos electrónicos ofensivos o groseros",
    "P4_02": "Ser objeto de chismes o rumores en internet",
    "P4_03": "Recibir mensajes ofensivos o groseros por redes sociales",
    "P4_04": "Recibir mensajes ofensivos o groseros por mensajería instantánea",
    "P4_05": "Ser excluido(a) o ignorado(a) en redes sociales o juegos en línea",
    "P4_06": "Que publicaran información falsa o vergonzosa sobre usted en internet",
    "P4_07": "Que alguien se hiciera pasar por usted en internet",
    "P4_08": "Que alguien publicara fotos o videos suyos sin su permiso",
    "P4_09": "Recibir amenazas o intimidaciones por internet",
    "P4_10": "Que alguien compartiera sus datos personales sin su permiso",
    "P4_11": "Recibir propuestas sexuales no deseadas por internet",
    "P4_12": "Que alguien lo/la acosara sexualmente por internet",
    "P4_13": "Otro tipo de ciberacoso"
}

@st.cache_data(show_spinner="Cargando datos desde Google Drive...")
def cargar_datos_base():
    file_ids = ["1ojZcLZost0BM00yCGN8OLnu7XYyLpEYr"]

    # Agregamos EDAD a las columnas requeridas
    columnas = (
        ["ANIO", "CVE_ENT", "NOM_ENT", "SEXO", "FACTOR", "EDAD"]
        + list(uso_medidas_de_seguridad.keys())
        + list(medidas_de_seguridad.keys())
        + [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
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
    
    # Convertir columnas a numérico
    todas_preguntas = (
        list(uso_medidas_de_seguridad.keys()) + 
        list(medidas_de_seguridad.keys()) + 
        [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
    )
    for col in todas_preguntas + ["EDAD"]:
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
        
    return df_final

df = cargar_datos_base()

st.title("📊 MOCIBA - Comparativa de Entidades")

tipo_variable = st.radio(
    "Seleccione el indicador",
    ["Uso de medidas de seguridad", "Medidas de seguridad", "Ciberacoso"]
)

if tipo_variable == "Uso de medidas de seguridad":
    opciones = uso_medidas_de_seguridad
elif tipo_variable == "Medidas de seguridad":
    opciones = medidas_de_seguridad
else:
    opciones = ciberacoso

variable = st.selectbox("Seleccione la variable", list(opciones.values()))
variable_key = [k for k, v in opciones.items() if v == variable][0]

if variable_key == "CUALQUIERA":
    variable_col = [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
    tipo_calculo = "cualquiera"
else:
    variable_col = variable_key
    tipo_calculo = "simple"

sexo = st.selectbox("Sexo", ["Total", "Hombres", "Mujeres"])

# --- NUEVO: Filtro por rango de edad ---
rangos_edad = {
    "Todas las edades": None,
    "12 a 19 años": (12, 19),
    "20 a 29 años": (20, 29),
    "30 a 39 años": (30, 39),
    "40 a 49 años": (40, 49),
    "50 a 59 años": (50, 59),
    "60 y más años": (60, 120)
}
rango_edad_seleccionado = st.selectbox("Rango de edad", list(rangos_edad.keys()))

# Selección de dos estados
estados_unicos = sorted([x for x in df["NOM_ENT"].dropna().unique()])
opciones_estado = ["NACIONAL"] + estados_unicos

col1, col2 = st.columns(2)
with col1:
    estado_1 = st.selectbox("Estado 1", opciones_estado, index=0)
with col2:
    estado_2 = st.selectbox("Estado 2", opciones_estado, index=1 if len(opciones_estado) > 1 else 0)

if estado_1 == estado_2:
    st.warning("⚠️ Selecciona dos estados diferentes para comparar.")

def calcular_porcentaje(df, variable_col, sexo, estado, tipo_calculo, rango_edad_key):
    # Filtrar por sexo
    if sexo == "Hombres":
        df_f = df[df["SEXO"] == 1].copy()
    elif sexo == "Mujeres":
        df_f = df[df["SEXO"] == 2].copy()
    else:
        df_f = df[df["SEXO"].isin([1, 2])].copy()

    # Filtrar por estado
    if estado != "NACIONAL":
        df_f = df_f[df_f["NOM_ENT"] == estado]

    # Filtrar por edad
    if rango_edad_key:
        min_e, max_e = rango_edad_key
        df_f = df_f[df_f["EDAD"].between(min_e, max_e)]

    resultados = []
    for anio, grupo in df_f.groupby("ANIO"):
        if tipo_calculo == "simple":
            numerador = grupo.loc[grupo[variable_col] == 1, "FACTOR"].sum()
            denominador = grupo.loc[grupo[variable_col].isin([1, 2]), "FACTOR"].sum()
        else:
            # Lógica OR: cualquiera de las columnas P4_XX == 1
            mascara = grupo[variable_col].eq(1).any(axis=1)
            numerador = grupo.loc[mascara, "FACTOR"].sum()
            denominador = grupo["FACTOR"].sum() # Total poblacional filtrado

        if denominador > 0:
            porcentaje = (numerador / denominador) * 100
        else:
            porcentaje = 0.0

        resultados.append({"ANIO": anio, "PORCENTAJE": round(porcentaje, 2)})

    return pd.DataFrame(resultados)

if estado_1 != estado_2:
    rango_key = rangos_edad[rango_edad_seleccionado]
    
    resultado_1 = calcular_porcentaje(df, variable_col, sexo, estado_1, tipo_calculo, rango_key)
    resultado_2 = calcular_porcentaje(df, variable_col, sexo, estado_2, tipo_calculo, rango_key)

    comparativa = pd.merge(
        resultado_1, resultado_2, on="ANIO", how="outer", suffixes=(f"_{estado_1}", f"_{estado_2}")
    ).fillna(0)

    comparativa = comparativa.rename(columns={
        f"PORCENTAJE_{estado_1}": estado_1,
        f"PORCENTAJE_{estado_2}": estado_2
    })
    comparativa = comparativa[["ANIO", estado_1, estado_2]]
    comparativa["Diferencia (pp)"] = round(comparativa[estado_1] - comparativa[estado_2], 2)

    st.subheader(f"Comparativa: {variable}")
    st.dataframe(comparativa, use_container_width=True)

    grafico_data = comparativa.melt(
        id_vars=["ANIO"], value_vars=[estado_1, estado_2],
        var_name="Entidad", value_name="Porcentaje"
    )

    st.line_chart(
        grafico_data, x="ANIO", y="Porcentaje", color="Entidad",
        y_label="Porcentaje (%)", x_label="Año"
    )
