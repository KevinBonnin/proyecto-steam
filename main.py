import pandas as pd
from fastapi import FastAPI
import uvicorn
import ast

inf = pd.read_csv('Proyecto Integrador I\proyecto-steam\steam_games.csv')

inf['año'] = inf['año'].astype(str)

app = FastAPI()

@app.get("/genero/{Año}")
def genero( Año: str ):
    juegos = (inf[inf['año'] == Año])
    juegos['genres'] = juegos['genres'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    generos_desglosados = juegos['genres'].explode()
    generos_mas_vendidos = generos_desglosados.value_counts().head(5).index.tolist()
    return {'Los generos mas vendidos en el año': Año, 'son': generos_mas_vendidos}

@app.get("/juegos/{Año}")
def juegos( Año: str ):
    filtro = (inf[inf['año'] == Año])
    juego = filtro[['title']].values.tolist()
    return {'Los juegos que se lanzaron en el año': Año, 'son': juego}

@app.get("/specs/{Año}")
def specs( Año: str ):
    juegos = (inf[inf['año'] == Año])
    juegos['specs'] = juegos['specs'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    especificaciones_desglosadas = juegos['specs'].explode()
    especificaciones_mas_repetidas = especificaciones_desglosadas.value_counts().head(5).index.tolist()
    return {'Las especificaciones mas repetidas en el año': Año, 'son': especificaciones_mas_repetidas}

@app.get("/earlyacces/{Año}")
def earlyacces( Año: str ):
    juegos_early_access = inf[(inf['año'] == Año) & (inf['early_access'] == True)]
    cantidad_juegos_early_access = juegos_early_access.shape[0]
    return {'La cantidad de juegos lanzados en el año': Año, 'es de': cantidad_juegos_early_access}

@app.get("/sentiment/{Año}")
def sentiment( Año: str ):
    data_filtrada = inf[inf['año'] == Año]
    data_filtrada['sentiment'] = data_filtrada['sentiment'].astype(str)
    data_filtrada = data_filtrada[~data_filtrada['sentiment'].str.contains(r'\d+ user reviews', case=False) & ~data_filtrada['sentiment'].isnull()]
    conteo_sentimiento = data_filtrada['sentiment'].value_counts()
    if 'nan' in conteo_sentimiento:
        del conteo_sentimiento['nan']
    return conteo_sentimiento.to_dict()

@app.get("/metascore/{Año}")
def metascore( Año: str ):
    top_juegos_metascore = inf[inf['año'] == Año].nlargest(5, 'metascore')
    juegoss = top_juegos_metascore[['title', 'metascore']]
    return {'Los juegos con mayor metascore y sus respectivos valores son': juegoss}