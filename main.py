import pandas as pd
from fastapi import FastAPI
import uvicorn
import ast

inf = pd.read_csv('steam_games.csv')

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