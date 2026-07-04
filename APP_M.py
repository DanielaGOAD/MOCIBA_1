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

# --- Grupo 4: Frecuencia de mensajes ofensivos
frecuencia_mensajes = {
    "P9_01": "Recibir mensajes ofensivos, con insultos o burlas",
    "P9_02": "Recibir mensajes con amenazas",
    "P9_03": "Recibir mensajes sexuales no deseados",
    "P9_04": "Que alguien se hiciera pasar por usted",
    "P9_05": "Que publicaran información falsa o vergonzosa sobre usted",
    "P9_06": "Que alguien compartiera sus datos personales sin permiso",
    "P9_07": "Que alguien publicara fotos o videos suyos sin permiso",
    "P9_08": "Ser excluido(a) o ignorado(a) en redes sociales o juegos",
    "P9_09": "Recibir correos electrónicos ofensivos o groseros",
    "P9_10": "Ser objeto de chismes o rumores en internet",
    "P9_11": "Que alguien lo/la acosara sexualmente por internet",
    "P9_12": "Recibir propuestas de encuentros sexuales no deseados",
    "P9_13": "Otro tipo de acoso"
}

# --- Tipos de ciberacoso para los indicadores de agresor
tipos_ciberacoso_agresor = {k: v for k, v in ciberacoso.items() if k != "CUALQUIERA"}

# --- Mapeo de códigos de edad del agresor a rangos
mapeo_rangos_edad_agresor = {
    1: "Menores de 12",
    2: "12 a 17",
    3: "18 a 25",
    4: "26 a 35",
    5: "36 a 45",
    6: "46 a 60",
    7: "Más de 60"
}

# --- Mapeo de códigos de efectos del ciberacoso (P10_XX_j)
mapeo_efectos_ciberacoso = {
    1: "Nervios",
    2: "Miedo",
    3: "Estrés",
    4: "Desconfianza",
    5: "Frustración",
    6: "Inseguridad",
    7: "Enojo",
    8: "Problemas con familiares, pareja o amigos",
    9: "Pérdida de dinero",
    10: "Pérdida de trabajo",
    11: "Daño a imagen profesional/laboral",
    12: "Daño a imagen escolar (bullying)",
    13: "Daño a imagen personal",
    14: "Otro",
    15: "Nada"
}

# --- Mapeo de CVE_ENT a NOM_ENT (estándar INEGI)
mapeo_entidades = {
    1: "AGUASCALIENTES",
    2: "BAJA CALIFORNIA",
    3: "BAJA CALIFORNIA SUR",
    4: "CAMPECHE",
    5: "COAHUILA DE ZARAGOZA",
    6: "COLIMA",
    7: "CHIAPAS",
    8: "CHIHUAHUA",
    9: "CIUDAD DE MEXICO",
    10: "DURANGO",
    11: "GUANAJUATO",
    12: "GUERRERO",
    13: "HIDALGO",
    14: "JALISCO",
    15: "MEXICO",
    16: "MICHOACAN DE OCAMPO",
    17: "MORELOS",
    18: "NAYARIT",
    19: "NUEVO LEON",
    20: "OAXACA",
    21: "PUEBLA",
    22: "QUERETARO",
    23: "QUINTANA ROO",
    24: "SAN LUIS POTOSI",
    25: "SINALOA",
    26: "SONORA",
    27: "TABASCO",
    28: "TAMAULIPAS",
    29: "TLAXCALA",
    30: "VERACRUZ DE IGNACIO DE LA LLAVE",
    31: "YUCATAN",
    32: "ZACATECAS"
}

@st.cache_data(show_spinner="Cargando datos desde Google Drive...")
def cargar_datos_base():
    file_ids = [
        "1ojZcLZost0BM00yCGN8OLnu7XYyLpEYr",
        "1v08-7Jx4Iw3msAkgb1m01Im49s8gqCqO",
        "1v6OgDHRSqNHbDnph2ijFvZB6RyTBAAk8",
        "1WQj9dD8RUkAcTvwunTGkkT4FwDfh6-vi",
        "1J49basZDca_rINW_h89q1aIZRIh2z4Ap"

    ]

    # Generar todas las columnas posibles
    columnas_p5 = [f"P5_{i:02d}_{j}" for i in range(1, 14) for j in range(1, 4)]
    columnas_p7 = [f"P7_{i:02d}_{j}" for i in range(1, 14) for j in range(1, 4)]
    columnas_p10 = [f"P10_{i:02d}_{j}" for i in range(1, 14) for j in range(1, 4)]

    # CVE_ENT es OBLIGATORIA porque con ella generamos NOM_ENT si falta
    columnas_base = ["ANIO", "CVE_ENT", "SEXO", "FACTOR", "EDAD", "NIVEL", "P7_4"]
    # NOM_ENT se maneja por separado (se genera si no existe)
    
    columnas_preguntas = (
        list(uso_medidas_de_seguridad.keys()) + 
        list(medidas_de_seguridad.keys()) + 
        [k for k in ciberacoso.keys() if k != "CUALQUIERA"] +
        list(frecuencia_mensajes.keys()) +
        columnas_p5 +
        columnas_p7 +
        columnas_p10
    )

    dfs = []

    for file_id in file_ids:
        url = f"https://drive.google.com/uc?id={file_id}"
        output = io.BytesIO()
        gdown.download(url, output, quiet=True)
        output.seek(0)

        # PASO 1: Leer solo los encabezados para saber qué columnas existen
        df_headers = pd.read_csv(
            output,
            encoding="latin1",
            nrows=0,
            low_memory=False
        )
        columnas_existentes = set(df_headers.columns)
        
        # PASO 2: Intersectar con las columnas que necesitamos
        output.seek(0)
        
        columnas_a_usar = [col for col in (columnas_base + columnas_preguntas) 
                          if col in columnas_existentes]
        
        # También incluir NOM_ENT si existe
        if "NOM_ENT" in columnas_existentes:
            columnas_a_usar.append("NOM_ENT")
        
        # Verificar columnas faltantes (para debugging)
        columnas_faltantes = [col for col in (columnas_base + columnas_preguntas) 
                             if col not in columnas_existentes]
        
        nom_ent_faltante = "NOM_ENT" not in columnas_existentes
        
        if columnas_faltantes or nom_ent_faltante:
            mensaje = f"⚠️ Archivo {file_id[:10]}..."
            if nom_ent_faltante:
                mensaje += " - Se generará NOM_ENT desde CVE_ENT."
            if columnas_faltantes:
                mensaje += f" Columnas faltantes: {', '.join(columnas_faltantes[:5])}{'...' if len(columnas_faltantes) > 5 else ''}"
            st.info(mensaje)

        # PASO 3: Leer el CSV completo solo con las columnas que existen
        df_temp = pd.read_csv(
            output,
            encoding="latin1",
            usecols=columnas_a_usar,
            low_memory=False
        )
        
        # PASO 4: Agregar columnas faltantes con NaN
        for col in (columnas_base + columnas_preguntas):
            if col not in df_temp.columns:
                df_temp[col] = pd.NA
        
        # PASO 5: Generar NOM_ENT desde CVE_ENT si no existe
        if "NOM_ENT" not in df_temp.columns:
            # Asegurar que CVE_ENT sea numérico
            df_temp["CVE_ENT"] = pd.to_numeric(df_temp["CVE_ENT"], errors='coerce')
            # Mapear usando el diccionario
            df_temp["NOM_ENT"] = df_temp["CVE_ENT"].map(mapeo_entidades)
        
        dfs.append(df_temp)

    df_final = pd.concat(dfs, ignore_index=True)
    
    # Convertir TODAS las columnas de preguntas a numérico
    for col in columnas_preguntas:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
    
    df_final["CVE_ENT"] = pd.to_numeric(df_final["CVE_ENT"], errors='coerce')
    df_final["EDAD"] = pd.to_numeric(df_final["EDAD"], errors='coerce')
    df_final["NIVEL"] = pd.to_numeric(df_final["NIVEL"], errors='coerce')
    df_final["P7_4"] = pd.to_numeric(df_final["P7_4"], errors='coerce')
    
    # Asegurar que NOM_ENT siempre exista y sea string
    if "NOM_ENT" not in df_final.columns:
        df_final["NOM_ENT"] = df_final["CVE_ENT"].map(mapeo_entidades)
    else:
        # Si NOM_ENT existe pero tiene NaN (por CVE_ENT inválido), rellenar con el mapeo
        df_final["CVE_ENT_num"] = pd.to_numeric(df_final["CVE_ENT"], errors='coerce')
        df_final["NOM_ENT"] = df_final["NOM_ENT"].fillna(df_final["CVE_ENT_num"].map(mapeo_entidades))
        df_final = df_final.drop(columns=["CVE_ENT_num"])
        
    return df_final

df = cargar_datos_base()

def mapear_nivel_escolaridad(nivel):
    if pd.isna(nivel):
        return None
    nivel = int(nivel)
    if nivel in [1, 2, 3]:
        return "Básica"
    elif nivel in [4, 5, 6]:
        return "Media Superior"
    elif nivel in [7, 8, 9, 10, 11]:
        return "Superior"
    else:
        return None

st.title("📊 MOCIBA - Comparativa de Entidades")

tipo_variable = st.radio(
    "Seleccione el indicador",
    [
        "Uso de medidas de seguridad",
        "Medidas de seguridad",
        "Ciberacoso",
        "Ciberacoso por nivel de escolaridad",
        "Horas promedio de uso de internet",
        "Frecuencia de mensajes ofensivos",
        "Víctimas que conocían al agresor",
        "Edad de la persona acosadora",
        "Efectos del ciberacoso"
    ]
)

# --- Lógica condicional según el indicador seleccionado ---
if tipo_variable == "Ciberacoso por nivel de escolaridad":
    variable = "Cualquiera de las anteriores (Ciberacoso general)"
    variable_col = [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
    tipo_calculo = "cualquiera"
    anios_disponibles = sorted(df["ANIO"].dropna().unique(), reverse=True)
    anio_seleccionado = st.selectbox("Seleccione el año", anios_disponibles, index=0)

elif tipo_variable == "Horas promedio de uso de internet":
    variable_col = None
    tipo_calculo = "horas_promedio"
    solo_victimas = st.checkbox("🔍 Mostrar solo para víctimas de ciberacoso", value=False)
    anio_seleccionado = None

elif tipo_variable == "Frecuencia de mensajes ofensivos":
    variable = st.selectbox("Seleccione el tipo de acoso", list(frecuencia_mensajes.values()))
    variable_key = [k for k, v in frecuencia_mensajes.items() if v == variable][0]
    variable_col = variable_key
    tipo_calculo = "frecuencia"
    anios_disponibles = sorted(df["ANIO"].dropna().unique(), reverse=True)
    anio_seleccionado = st.selectbox("Seleccione el año", anios_disponibles, index=0)

elif tipo_variable == "Víctimas que conocían al agresor":
    tipo_acoso_seleccionado = st.selectbox(
        "Seleccione el tipo de ciberacoso",
        list(tipos_ciberacoso_agresor.values())
    )
    p4_key = [k for k, v in tipos_ciberacoso_agresor.items() if v == tipo_acoso_seleccionado][0]
    numero_acoso = p4_key.split("_")[1]
    variable_col = p4_key
    tipo_calculo = "conocian_agresor"
    anio_seleccionado = None
    solo_victimas = False

elif tipo_variable == "Edad de la persona acosadora":
    anios_disponibles = sorted(df["ANIO"].dropna().unique(), reverse=True)
    anio_seleccionado = st.selectbox("Seleccione el año", anios_disponibles, index=0)
    variable_col = None
    tipo_calculo = "edad_agresor"
    solo_victimas = False

elif tipo_variable == "Efectos del ciberacoso":
    anios_disponibles = sorted(df["ANIO"].dropna().unique(), reverse=True)
    anio_seleccionado = st.selectbox("Seleccione el año", anios_disponibles, index=0)
    variable_col = None
    tipo_calculo = "efectos_ciberacoso"
    solo_victimas = False

else:
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
    
    anio_seleccionado = None
    solo_victimas = False

sexo = st.selectbox("Sexo", ["Total", "Hombres", "Mujeres"])

# --- FILTRO DE EDAD: Solo aparece cuando se selecciona "Ciberacoso" ---
edad_min, edad_max = None, None
filtro_edad_activo = False

if tipo_variable == "Ciberacoso":
    st.markdown("---")
    filtro_edad_activo = st.checkbox("🔍 Filtrar por rango de edad", value=False)
    
    if filtro_edad_activo:
        rango_predefinido = st.selectbox(
            "Selecciona un rango predefinido",
            ["Personalizado", "12-19 (Adolescentes)", "20-29 (Jóvenes adultos)", "30-59 (Adultos)", "60+ (Adultos mayores)"]
        )
        
        if rango_predefinido == "Personalizado":
            col_edad1, col_edad2 = st.columns(2)
            with col_edad1:
                edad_min = st.number_input("Edad mínima", min_value=12, max_value=100, value=12, step=1)
            with col_edad2:
                edad_max = st.number_input("Edad máxima", min_value=12, max_value=100, value=19, step=1)
        elif rango_predefinido == "12-19 (Adolescentes)":
            edad_min, edad_max = 12, 19
        elif rango_predefinido == "20-29 (Jóvenes adultos)":
            edad_min, edad_max = 20, 29
        elif rango_predefinido == "30-59 (Adultos)":
            edad_min, edad_max = 30, 59
        else:
            edad_min, edad_max = 60, 100
        
        st.info(f"📌 Rango seleccionado: {edad_min} a {edad_max} años")

# Selección de dos estados para comparar
estados_unicos = sorted([x for x in df["NOM_ENT"].dropna().unique()])
opciones_estado = ["NACIONAL"] + estados_unicos

col1, col2 = st.columns(2)

with col1:
    estado_1 = st.selectbox("Estado 1 (comparar contra)", opciones_estado, index=0)

with col2:
    estado_2 = st.selectbox("Estado 2 (comparar contra)", opciones_estado, index=1 if len(opciones_estado) > 1 else 0)

if estado_1 == estado_2:
    st.warning("⚠️ Has seleccionado el mismo estado en ambos lados. Selecciona dos estados diferentes para comparar.")


# ===================== FUNCIONES DE CÁLCULO =====================

def calcular_porcentaje(df, variable_col, sexo, estado, tipo_calculo, edad_min=None, edad_max=None, anio=None):
    df_filtrado = df.copy()
    if anio is not None:
        df_filtrado = df_filtrado[df_filtrado["ANIO"] == anio]
    if sexo == "Hombres":
        df_filtrado = df_filtrado[df_filtrado["SEXO"] == 1].copy()
    elif sexo == "Mujeres":
        df_filtrado = df_filtrado[df_filtrado["SEXO"] == 2].copy()
    else:
        df_filtrado = df_filtrado[df_filtrado["SEXO"].isin([1, 2])].copy()
    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]
    if edad_min is not None and edad_max is not None:
        df_filtrado = df_filtrado[(df_filtrado["EDAD"] >= edad_min) & (df_filtrado["EDAD"] <= edad_max)].copy()

    resultados = []
    for anio_grupo, grupo in df_filtrado.groupby("ANIO"):
        if tipo_calculo == "simple":
            numerador = grupo.loc[grupo[variable_col] == 1, "FACTOR"].sum()
            denominador = grupo.loc[grupo[variable_col].isin([1, 2]), "FACTOR"].sum()
        else:
            mascara_ciberacoso = grupo[variable_col].eq(1).any(axis=1)
            numerador = grupo.loc[mascara_ciberacoso, "FACTOR"].sum()
            denominador = grupo["FACTOR"].sum()
        porcentaje = (numerador / denominador) * 100 if denominador > 0 else 0.0
        resultados.append({"ANIO": anio_grupo, "PORCENTAJE": round(porcentaje, 2)})
    return pd.DataFrame(resultados)


def calcular_ciberacoso_por_escolaridad(df, variable_col, estado, anio):
    df_filtrado = df.copy()
    df_filtrado = df_filtrado[df_filtrado["ANIO"] == anio]
    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]
    df_filtrado = df_filtrado[df_filtrado["NIVEL"].isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])]
    mascara_ciberacoso = df_filtrado[variable_col].eq(1).any(axis=1)
    df_victimas = df_filtrado[mascara_ciberacoso].copy()
    df_victimas["NIVEL_ESCOLARIDAD"] = df_victimas["NIVEL"].apply(mapear_nivel_escolaridad)

    resultados = []
    for sexo_codigo, sexo_nombre in [(1, "Hombres"), (2, "Mujeres")]:
        df_victimas_sexo = df_victimas[df_victimas["SEXO"] == sexo_codigo]
        total_victimas_sexo = df_victimas_sexo["FACTOR"].sum()
        victimas_por_nivel = df_victimas_sexo.groupby("NIVEL_ESCOLARIDAD")["FACTOR"].sum()
        for nivel in ["Básica", "Media Superior", "Superior"]:
            porcentaje = (victimas_por_nivel.get(nivel, 0) / total_victimas_sexo) * 100 if total_victimas_sexo > 0 else 0.0
            resultados.append({"SEXO": sexo_nombre, "NIVEL_ESCOLARIDAD": nivel, "PORCENTAJE": round(porcentaje, 2)})
    return pd.DataFrame(resultados)


def calcular_horas_promedio_internet(df, estado, solo_victimas=False):
    df_filtrado = df.copy()
    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]
    df_filtrado = df_filtrado[df_filtrado["P7_4"] < 98]
    if solo_victimas:
        columnas_ciberacoso = [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
        mascara_ciberacoso = df_filtrado[columnas_ciberacoso].eq(1).any(axis=1)
        df_filtrado = df_filtrado[mascara_ciberacoso]

    resultados = []
    for anio, grupo in df_filtrado.groupby("ANIO"):
        if len(grupo) > 0:
            suma_ponderada = (grupo["P7_4"] * grupo["FACTOR"]).sum()
            suma_factor = grupo["FACTOR"].sum()
            horas_promedio = suma_ponderada / suma_factor if suma_factor > 0 else 0.0
        else:
            horas_promedio = 0.0
        resultados.append({"ANIO": anio, "HORAS_PROMEDIO": round(horas_promedio, 2)})
    return pd.DataFrame(resultados)


def calcular_frecuencia_mensajes(df, variable_col, estado, anio):
    df_filtrado = df.copy()
    df_filtrado = df_filtrado[df_filtrado["ANIO"] == anio]
    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]
    df_filtrado = df_filtrado[df_filtrado["SEXO"].isin([1, 2])]

    resultados = []
    for sexo_codigo, sexo_nombre in [(1, "Hombres"), (2, "Mujeres")]:
        df_sexo = df_filtrado[df_filtrado["SEXO"] == sexo_codigo]
        denominador = df_sexo[df_sexo[variable_col].isin([1, 2, 3, 4])]["FACTOR"].sum()
        if denominador > 0:
            muchas_veces = (df_sexo[df_sexo[variable_col] == 1]["FACTOR"].sum() / denominador) * 100
            algunas_veces = (df_sexo[df_sexo[variable_col] == 2]["FACTOR"].sum() / denominador) * 100
            pocas_veces = (df_sexo[df_sexo[variable_col] == 3]["FACTOR"].sum() / denominador) * 100
            una_vez = (df_sexo[df_sexo[variable_col] == 4]["FACTOR"].sum() / denominador) * 100
        else:
            muchas_veces = algunas_veces = pocas_veces = una_vez = 0.0
        resultados.append({"SEXO": sexo_nombre, "Muchas veces": round(muchas_veces, 2), "Algunas veces": round(algunas_veces, 2), "Pocas veces": round(pocas_veces, 2), "Una vez": round(una_vez, 2)})
    return pd.DataFrame(resultados)


def calcular_victimas_conocian_agresor(df, p4_variable, numero_acoso, estado):
    df_filtrado = df.copy()
    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]
    
    col_p5_1 = f"P5_{numero_acoso}_1"
    col_p5_2 = f"P5_{numero_acoso}_2"
    col_p5_3 = f"P5_{numero_acoso}_3"
    
    columnas_existentes = [c for c in [col_p5_1, col_p5_2, col_p5_3] if c in df_filtrado.columns]
    
    if not columnas_existentes:
        return pd.DataFrame(columns=["ANIO", "PORCENTAJE"])
    
    columnas_ciberacoso = [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
    
    resultados = []
    
    for anio, grupo in df_filtrado.groupby("ANIO"):
        mascara_victima = grupo[columnas_ciberacoso].eq(1).any(axis=1)
        mascara_tipo_acoso = grupo[p4_variable] == 1
        
        mascara_conocia = pd.Series(False, index=grupo.index)
        for col in columnas_existentes:
            mascara_conocia = mascara_conocia | grupo[col].isin([1, 2, 3, 4, 5, 6, 7])
        
        mascara_final = mascara_tipo_acoso & mascara_conocia
        
        factor_victimas = grupo.loc[mascara_victima, "FACTOR"].sum()
        factor_conocidos = grupo.loc[mascara_final, "FACTOR"].sum()
        
        porcentaje = (factor_conocidos / factor_victimas) * 100 if factor_victimas > 0 else 0.0
        
        resultados.append({"ANIO": anio, "PORCENTAJE": round(porcentaje, 2)})
    
    return pd.DataFrame(resultados)


def calcular_edad_agresor_global(df, estado, anio):
    df_filtrado = df.copy()
    df_filtrado = df_filtrado[df_filtrado["ANIO"] == anio]
    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]
    
    columnas_ciberacoso = [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
    mascara_victima = df_filtrado[columnas_ciberacoso].eq(1).any(axis=1)
    df_victimas = df_filtrado[mascara_victima].copy()
    
    if len(df_victimas) == 0:
        return pd.DataFrame(columns=["RANGO_EDAD", "PORCENTAJE"])
    
    total_victimas = df_victimas["FACTOR"].sum()
    if total_victimas == 0:
        return pd.DataFrame(columns=["RANGO_EDAD", "PORCENTAJE"])
    
    columnas_p7 = [f"P7_{i:02d}_{j}" for i in range(1, 14) for j in range(1, 4)]
    columnas_existentes = [c for c in columnas_p7 if c in df_victimas.columns]
    
    if not columnas_existentes:
        return pd.DataFrame(columns=["RANGO_EDAD", "PORCENTAJE"])
    
    resultados = []
    for codigo_rango in range(1, 8):
        mascara_rango = pd.Series(False, index=df_victimas.index)
        for col in columnas_existentes:
            mascara_rango = mascara_rango | (df_victimas[col] == codigo_rango)
        
        factor_con_rango = df_victimas.loc[mascara_rango, "FACTOR"].sum()
        porcentaje = (factor_con_rango / total_victimas) * 100
        
        resultados.append({
            "RANGO_EDAD": mapeo_rangos_edad_agresor[codigo_rango],
            "PORCENTAJE": round(porcentaje, 2)
        })
    
    return pd.DataFrame(resultados)


def calcular_efectos_ciberacoso(df, estado, anio, sexo):
    df_filtrado = df.copy()
    df_filtrado = df_filtrado[df_filtrado["ANIO"] == anio]
    if estado != "NACIONAL":
        df_filtrado = df_filtrado[df_filtrado["NOM_ENT"] == estado]
    
    if sexo == "Hombres":
        df_filtrado = df_filtrado[df_filtrado["SEXO"] == 1].copy()
    elif sexo == "Mujeres":
        df_filtrado = df_filtrado[df_filtrado["SEXO"] == 2].copy()
    else:
        df_filtrado = df_filtrado[df_filtrado["SEXO"].isin([1, 2])].copy()
    
    columnas_ciberacoso = [k for k in ciberacoso.keys() if k != "CUALQUIERA"]
    mascara_victima = df_filtrado[columnas_ciberacoso].eq(1).any(axis=1)
    df_victimas = df_filtrado[mascara_victima].copy()
    
    if len(df_victimas) == 0:
        return pd.DataFrame(columns=["EFECTO", "PORCENTAJE"])
    
    total_victimas = df_victimas["FACTOR"].sum()
    if total_victimas == 0:
        return pd.DataFrame(columns=["EFECTO", "PORCENTAJE"])
    
    columnas_p10 = [f"P10_{i:02d}_{j}" for i in range(1, 14) for j in range(1, 4)]
    columnas_existentes = [c for c in columnas_p10 if c in df_victimas.columns]
    
    if not columnas_existentes:
        return pd.DataFrame(columns=["EFECTO", "PORCENTAJE"])
    
    resultados = []
    for codigo_efecto in range(1, 16):
        mascara_efecto = pd.Series(False, index=df_victimas.index)
        for col in columnas_existentes:
            mascara_efecto = mascara_efecto | (df_victimas[col] == codigo_efecto)
        
        factor_con_efecto = df_victimas.loc[mascara_efecto, "FACTOR"].sum()
        porcentaje = (factor_con_efecto / total_victimas) * 100
        
        resultados.append({
            "EFECTO": mapeo_efectos_ciberacoso[codigo_efecto],
            "PORCENTAJE": round(porcentaje, 2)
        })
    
    return pd.DataFrame(resultados)


# ===================== VISUALIZACIÓN =====================

if tipo_variable == "Ciberacoso por nivel de escolaridad":
    if estado_1 != estado_2:
        resultado_1 = calcular_ciberacoso_por_escolaridad(df, variable_col, estado_1, anio_seleccionado)
        resultado_2 = calcular_ciberacoso_por_escolaridad(df, variable_col, estado_2, anio_seleccionado)
        
        tabla_1 = resultado_1.pivot(index="NIVEL_ESCOLARIDAD", columns="SEXO", values="PORCENTAJE").fillna(0)
        tabla_2 = resultado_2.pivot(index="NIVEL_ESCOLARIDAD", columns="SEXO", values="PORCENTAJE").fillna(0)
        
        tabla_1.columns = [f"{col} - {estado_1}" for col in tabla_1.columns]
        tabla_2.columns = [f"{col} - {estado_2}" for col in tabla_2.columns]
        
        comparativa = pd.concat([tabla_1, tabla_2], axis=1).reset_index()
        
        st.subheader(f"Distribución de Víctimas de Ciberacoso por Nivel de Escolaridad - Año {anio_seleccionado}")
        st.info("💡 De todas las víctimas de ciberacoso de ese sexo, ¿qué porcentaje tiene ese nivel de escolaridad?")
        st.dataframe(comparativa, use_container_width=True)
        
        grafico_data = resultado_1.copy()
        grafico_data["ENTIDAD"] = estado_1
        grafico_data2 = resultado_2.copy()
        grafico_data2["ENTIDAD"] = estado_2
        grafico_completo = pd.concat([grafico_data, grafico_data2])
        
        st.bar_chart(grafico_completo, x="NIVEL_ESCOLARIDAD", y="PORCENTAJE", color="SEXO", x_label="Nivel de Escolaridad", y_label="Porcentaje de Víctimas (%)")

elif tipo_variable == "Horas promedio de uso de internet":
    if estado_1 != estado_2:
        resultado_1 = calcular_horas_promedio_internet(df, estado_1, solo_victimas)
        resultado_2 = calcular_horas_promedio_internet(df, estado_2, solo_victimas)
        
        comparativa = pd.merge(resultado_1, resultado_2, on="ANIO", how="outer", suffixes=(f"_{estado_1}", f"_{estado_2}")).fillna(0)
        comparativa = comparativa.rename(columns={f"HORAS_PROMEDIO_{estado_1}": estado_1, f"HORAS_PROMEDIO_{estado_2}": estado_2})
        comparativa = comparativa[["ANIO", estado_1, estado_2]]
        comparativa["Diferencia (horas)"] = round(comparativa[estado_1] - comparativa[estado_2], 2)
        
        titulo = "Horas Promedio de Uso de Internet - Solo Víctimas de Ciberacoso" if solo_victimas else "Horas Promedio de Uso de Internet - Población General"
        st.subheader(titulo)
        st.info("💡 Promedio ponderado de horas de uso de internet al día (excluyendo valores no especificados)")
        st.dataframe(comparativa, use_container_width=True)
        
        grafico_data = comparativa.melt(id_vars=["ANIO"], value_vars=[estado_1, estado_2], var_name="Entidad", value_name="Horas Promedio")
        st.line_chart(grafico_data, x="ANIO", y="Horas Promedio", color="Entidad", y_label="Horas al Día", x_label="Año")

elif tipo_variable == "Frecuencia de mensajes ofensivos":
    if estado_1 != estado_2:
        resultado_1 = calcular_frecuencia_mensajes(df, variable_col, estado_1, anio_seleccionado)
        resultado_2 = calcular_frecuencia_mensajes(df, variable_col, estado_2, anio_seleccionado)
        
        tabla_1 = resultado_1.set_index("SEXO")
        tabla_2 = resultado_2.set_index("SEXO")
        tabla_1.columns = [f"{col} - {estado_1}" for col in tabla_1.columns]
        tabla_2.columns = [f"{col} - {estado_2}" for col in tabla_2.columns]
        comparativa = pd.concat([tabla_1, tabla_2], axis=1).reset_index().rename(columns={"index": "Sexo"})
        
        st.subheader(f"Frecuencia de {variable} - Año {anio_seleccionado}")
        st.info("💡 Distribución porcentual de la frecuencia (Muchas veces, Algunas veces, Pocas veces, Una vez)")
        st.dataframe(comparativa, use_container_width=True)
        
        frecuencias = ["Muchas veces", "Algunas veces", "Pocas veces", "Una vez"]
        grafico_data = []
        for _, row in resultado_1.iterrows():
            for freq in frecuencias:
                grafico_data.append({"Frecuencia": freq, "Porcentaje": row[freq], "Sexo": row["SEXO"], "Entidad": estado_1})
        for _, row in resultado_2.iterrows():
            for freq in frecuencias:
                grafico_data.append({"Frecuencia": freq, "Porcentaje": row[freq], "Sexo": row["SEXO"], "Entidad": estado_2})
        
        st.bar_chart(pd.DataFrame(grafico_data), x="Frecuencia", y="Porcentaje", color="Sexo", x_label="Frecuencia", y_label="Porcentaje (%)")

elif tipo_variable == "Víctimas que conocían al agresor":
    if estado_1 != estado_2:
        resultado_1 = calcular_victimas_conocian_agresor(df, variable_col, numero_acoso, estado_1)
        resultado_2 = calcular_victimas_conocian_agresor(df, variable_col, numero_acoso, estado_2)
        
        if resultado_1.empty and resultado_2.empty:
            st.warning(f"⚠️ No se encontraron datos de identidad del agresor (P5_{numero_acoso}_1, P5_{numero_acoso}_2, P5_{numero_acoso}_3) en el archivo.")
        else:
            comparativa = pd.merge(resultado_1, resultado_2, on="ANIO", how="outer", suffixes=(f"_{estado_1}", f"_{estado_2}")).fillna(0)
            comparativa = comparativa.rename(columns={f"PORCENTAJE_{estado_1}": estado_1, f"PORCENTAJE_{estado_2}": estado_2})
            comparativa = comparativa[["ANIO", estado_1, estado_2]]
            comparativa["Diferencia (pp)"] = round(comparativa[estado_1] - comparativa[estado_2], 2)
            
            st.subheader(f"Víctimas que Conocían al Agresor - {tipo_acoso_seleccionado}")
            st.info(f"💡 De todas las víctimas de ciberacoso, ¿qué porcentaje sufrió '{tipo_acoso_seleccionado}' y conocía a la persona agresora?")
            st.dataframe(comparativa, use_container_width=True)
            
            grafico_data = comparativa.melt(id_vars=["ANIO"], value_vars=[estado_1, estado_2], var_name="Entidad", value_name="Porcentaje")
            st.line_chart(grafico_data, x="ANIO", y="Porcentaje", color="Entidad", y_label="Porcentaje (%)", x_label="Año")

elif tipo_variable == "Edad de la persona acosadora":
    if estado_1 != estado_2:
        resultado_1 = calcular_edad_agresor_global(df, estado_1, anio_seleccionado)
        resultado_2 = calcular_edad_agresor_global(df, estado_2, anio_seleccionado)
        
        if resultado_1.empty and resultado_2.empty:
            st.warning(f"⚠️ No se encontraron datos de edad del agresor en el archivo.")
        else:
            tabla_1 = resultado_1.set_index("RANGO_EDAD")
            tabla_2 = resultado_2.set_index("RANGO_EDAD")
            
            tabla_1.columns = [f"{col} - {estado_1}" for col in tabla_1.columns]
            tabla_2.columns = [f"{col} - {estado_2}" for col in tabla_2.columns]
            
            comparativa = pd.concat([tabla_1, tabla_2], axis=1).fillna(0).reset_index()
            comparativa = comparativa.rename(columns={"index": "Rango de Edad"})
            
            st.subheader(f"Edad de la Persona Acosadora - Año {anio_seleccionado}")
            st.info("💡 Porcentaje de víctimas de ciberacoso que reportaron al menos un agresor en cada rango de edad. Los porcentajes pueden sumar más del 100% porque una víctima puede tener agresores de diferentes rangos.")
            st.dataframe(comparativa, use_container_width=True)
            
            grafico_data = []
            for _, row in resultado_1.iterrows():
                grafico_data.append({
                    "Rango de Edad": row["RANGO_EDAD"],
                    "Porcentaje": row["PORCENTAJE"],
                    "Entidad": estado_1
                })
            for _, row in resultado_2.iterrows():
                grafico_data.append({
                    "Rango de Edad": row["RANGO_EDAD"],
                    "Porcentaje": row["PORCENTAJE"],
                    "Entidad": estado_2
                })
            
            df_grafico = pd.DataFrame(grafico_data)
            
            st.bar_chart(
                df_grafico,
                x="Rango de Edad",
                y="Porcentaje",
                color="Entidad",
                x_label="Edad del Agresor",
                y_label="Porcentaje de Víctimas (%)"
            )

elif tipo_variable == "Efectos del ciberacoso":
    if estado_1 != estado_2:
        resultado_1 = calcular_efectos_ciberacoso(df, estado_1, anio_seleccionado, sexo)
        resultado_2 = calcular_efectos_ciberacoso(df, estado_2, anio_seleccionado, sexo)
        
        if resultado_1.empty and resultado_2.empty:
            st.warning(f"⚠️ No se encontraron datos de efectos del ciberacoso (P10_XX_j) en el archivo.")
        else:
            tabla_1 = resultado_1.set_index("EFECTO")
            tabla_2 = resultado_2.set_index("EFECTO")
            
            tabla_1.columns = [f"{col} - {estado_1}" for col in tabla_1.columns]
            tabla_2.columns = [f"{col} - {estado_2}" for col in tabla_2.columns]
            
            comparativa = pd.concat([tabla_1, tabla_2], axis=1).fillna(0).reset_index()
            comparativa = comparativa.rename(columns={"index": "Efecto"})
            
            st.subheader(f"Efectos del Ciberacoso - Año {anio_seleccionado} - {sexo}")
            st.info("💡 Porcentaje de víctimas de ciberacoso que experimentaron cada efecto. Los porcentajes pueden sumar más del 100% porque una víctima puede experimentar múltiples efectos.")
            st.dataframe(comparativa, use_container_width=True)
            
            grafico_data = []
            for _, row in resultado_1.iterrows():
                grafico_data.append({
                    "Efecto": row["EFECTO"],
                    "Porcentaje": row["PORCENTAJE"],
                    "Entidad": estado_1
                })
            for _, row in resultado_2.iterrows():
                grafico_data.append({
                    "Efecto": row["EFECTO"],
                    "Porcentaje": row["PORCENTAJE"],
                    "Entidad": estado_2
                })
            
            df_grafico = pd.DataFrame(grafico_data)
            
            st.bar_chart(
                df_grafico,
                x="Efecto",
                y="Porcentaje",
                color="Entidad",
                x_label="Efecto",
                y_label="Porcentaje de Víctimas (%)"
            )

else:
    if estado_1 != estado_2:
        resultado_1 = calcular_porcentaje(df, variable_col, sexo, estado_1, tipo_calculo, edad_min, edad_max)
        resultado_2 = calcular_porcentaje(df, variable_col, sexo, estado_2, tipo_calculo, edad_min, edad_max)

        comparativa = pd.merge(resultado_1, resultado_2, on="ANIO", how="outer", suffixes=(f"_{estado_1}", f"_{estado_2}")).fillna(0)
        comparativa = comparativa.rename(columns={f"PORCENTAJE_{estado_1}": estado_1, f"PORCENTAJE_{estado_2}": estado_2})
        comparativa = comparativa[["ANIO", estado_1, estado_2]]
        comparativa["Diferencia (pp)"] = round(comparativa[estado_1] - comparativa[estado_2], 2)

        titulo_subheader = f"{variable} - Rango de edad: {edad_min} a {edad_max} años" if filtro_edad_activo else variable
        st.subheader(f"Comparativa: {titulo_subheader}")
        st.dataframe(comparativa, use_container_width=True)

        grafico_data = comparativa.melt(id_vars=["ANIO"], value_vars=[estado_1, estado_2], var_name="Entidad", value_name="Porcentaje")
        st.line_chart(grafico_data, x="ANIO", y="Porcentaje", color="Entidad", y_label="Porcentaje (%)", x_label="Año")
