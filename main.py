import pandas as pd
from fastapi import FastAPI
import uvicorn
import ast
import joblib
from enum import Enum

class Genero(str, Enum):
    Accion = 'Action'
    Aventura = 'Adventure'
    Animacion_y_modelado = 'Animation &amp; Modeling'
    Audio = 'Audio Production'
    Casual = 'Casual'
    Design_e_ilustracion = 'Design &amp; Illustration'
    Acceso_temprano = 'Early Access'
    Educacion = 'Education'
    Gratis_para_jugar = 'Free to Play'
    Indie = 'Indie'
    Multijugador_masivo = 'Massively Multiplayer'
    Edicion_de_fotos = 'Photo Editing'
    RPG = 'RPG'
    Carreras = 'Racing'
    Simulacion = 'Simulation'
    Entrenamiento_de_software = 'Software Training'
    Deportes = 'Sports'
    Estrategia = 'Strategy'
    Utilidades = 'Utilities'
    Produccion_de_video = 'Video Production'
    Publicacion_web = 'Web Publishing'
    
class Especificaciones(str, Enum):
    Subtitulos_disponibles = 'Captions available'
    Cooperativo = 'Co-op'
    Comentarios_disponibles = 'Commentary available'
    Multijugador_entre_plataformas = 'Cross-Platform Multiplayer'
    Contenido_descargable = 'Downloadable Content'
    Soporte_completo_de_mando = 'Full controller support'
    Demo_del_juego = 'Game demo'
    Compras_en_la_aplicación = 'In-App Purchases'
    Incluye_Source_SDK = 'Includes Source SDK'
    Incluye_editor_de_niveles = 'Includes level editor'
    Co_op_local = 'Local Co-op'
    Multijugador_local = 'Local Multi-Player'
    MMO = 'MMO'
    Mods = 'Mods'
    Mods_requieren_HL1 = 'Mods (require HL1)'
    Mods_requieren_HL2 = 'Mods (require HL2)'
    Multijugador = 'Multi-player'
    Co_op_en_línea = 'Online Co-op'
    Multijugador_en_línea = 'Online Multi-Player'
    Soporte_parcial_de_mando = 'Partial Controller Support'
    Pantalla_compartida = 'Shared/Split Screen'
    Un_jugador = 'Single-player'
    Estadísticas = 'Stats'
    Logros_de_Steam = 'Steam Achievements'
    Almacenamiento_en_la_nube_de_Steam = 'Steam Cloud'
    Tablas_de_clasificación_de_Steam = 'Steam Leaderboards'
    Tarjetas_de_intercambio_de_Steam = 'Steam Trading Cards'
    Notificaciones_de_giro_de_Steam = 'Steam Turn Notifications'
    Taller_de_Steam = 'Steam Workshop'
    Coleccionables_de_SteamVR = 'SteamVR Collectibles'
    Valve_Anti_Cheat_habilitado = 'Valve Anti-Cheat enabled'

inf = pd.read_csv('steam_games.csv')

modelo = joblib.load('modelo_regresion.pkl')

inf['Year'] = inf['Year'].astype(str)

app = FastAPI()

@app.get("/genero/{Year}/Los 5 géneros más vendidos.")
def genero( Year: str ):
    juegos = (inf[inf['Year'] == Year])
    juegos['genres'] = juegos['genres'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    generos_desglosados = juegos['genres'].explode()
    generos_mas_vendidos = generos_desglosados.value_counts().head(5).index.tolist()
    return {'Los generos mas vendidos en el año': Year, 'son': generos_mas_vendidos}

@app.get("/juegos/{Year}/Lista con los juegos lanzados en el año.")
def juegos( Year: str ):
    filtro = (inf[inf['Year'] == Year])
    juego = filtro[['title']].values.tolist()
    return {'Los juegos que se lanzaron en el año': Year, 'son': juego}

@app.get("/specs/{Year}/Lista con los 5 specs que más se repiten")
def specs( Year: str ):
    juegos = (inf[inf['Year'] == Year])
    juegos['specs'] = juegos['specs'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    especificaciones_desglosadas = juegos['specs'].explode()
    especificaciones_mas_repetidas = especificaciones_desglosadas.value_counts().head(5).index.tolist()
    return {'Las especificaciones mas repetidas en el año': Year, 'son': especificaciones_mas_repetidas}

@app.get("/earlyacces/{Year}/Cantidad de juegos lanzados en un año con early access")
def earlyacces( Year: str ):
    juegos_early_access = inf[(inf['Year'] == Year) & (inf['early_access'] == True)]
    cantidad_juegos_early_access = juegos_early_access.shape[0]
    return {'La cantidad de juegos lanzados en el año': Year, 'es de': cantidad_juegos_early_access}

@app.get("/sentiment/{Year}/Cantidad de registros que se encuentren categorizados con un análisis de sentimiento.")
def sentiment( Year: str ):
    data_filtrada = inf[inf['Year'] == Year]
    data_filtrada['sentiment'] = data_filtrada['sentiment'].astype(str)
    data_filtrada = data_filtrada[~data_filtrada['sentiment'].str.contains(r'\d+ user reviews', case=False) & ~data_filtrada['sentiment'].isnull()]
    conteo_sentimiento = data_filtrada['sentiment'].value_counts()
    if 'nan' in conteo_sentimiento:
        del conteo_sentimiento['nan']
    return conteo_sentimiento.to_dict()

@app.get("/metascore/{Year}/Top 5 juegos según año con mayor metascore.")
def metascore( Year: str ):
    top_juegos_metascore = inf[inf['Year'] == Year].nlargest(5, 'metascore')
    juegoss = top_juegos_metascore[['title', 'metascore']]
    return {'Los juegos con mayor metascore y sus respectivos valores son': juegoss}

@app.get("/modelo de prediccion")
def prediccion(genero: Genero, especificaciones: Especificaciones):
    datos = {}
    for valor in Genero:
        datos[valor.value] = [1 if valor == genero else 0]
        
    for valor in Especificaciones:
        datos[valor.value] = [1 if valor == especificaciones else 0]
        
    df = pd.DataFrame(datos)
    precio = modelo.predict(df)
    return {'precio predecido': precio, 'RMSE del modelo': 10.773332764246002}