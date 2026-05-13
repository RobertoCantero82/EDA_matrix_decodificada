import ast
import time

import pandas as pd
import requests
from nltk.corpus import stopwords


# =============================================================================
# HIPÓTESIS 1
# =============================================================================

def extraer_generos(texto):
    """Convierte el string JSON de géneros en una lista de nombres."""
    lista = ast.literal_eval(texto)
    return [genero["name"] for genero in lista]


def sci_fi(generos):
    """Devuelve True si la película es de ciencia ficción."""
    return "Science Fiction" in generos


def extraer_efectos(texto):
    """Extrae los nombres de las personas del departamento de Visual Effects."""
    lista = ast.literal_eval(texto)
    return [persona['name'] for persona in lista if persona['department'] == 'Visual Effects']


# =============================================================================
# HIPÓTESIS 2
# =============================================================================

def ngrams(terms, start=1980, end=2019, corpus='en-2019', smoothing=3):
    """Descarga frecuencias de términos desde la API de Google Ngrams."""
    url = 'https://books.google.com/ngrams/json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://books.google.com/ngrams'
    }
    params = {
        'content': ','.join(terms),
        'year_start': start,
        'year_end': end,
        'corpus': corpus,
        'smoothing': smoothing
    }
    r = requests.get(url, params=params, headers=headers, timeout=20)
    data = r.json()
    df = pd.DataFrame({'year': list(range(start, end + 1))})
    for serie in data:
        df[serie['ngram']] = serie['timeseries']
    return df


def buscar_videos_youtube(query, api_key, lang, max_results=50):
    """
    Busca vídeos en YouTube por término y devuelve un DataFrame con sus métricas.
    Hace dos llamadas a la API: una para obtener IDs y otra para las estadísticas.
    """
    # Paso 1: buscar IDs
    r = requests.get(
        'https://www.googleapis.com/youtube/v3/search',
        params={
            'part': 'snippet', 'q': query, 'type': 'video',
            'maxResults': max_results, 'order': 'viewCount',
            'relevanceLanguage': lang, 'key': api_key
        }, timeout=15
    )
    items = r.json().get('items', [])
    ids = [item['id']['videoId'] for item in items if 'videoId' in item['id']]
    if not ids:
        return pd.DataFrame()

    # Paso 2: obtener estadísticas por ID
    r2 = requests.get(
        'https://www.googleapis.com/youtube/v3/videos',
        params={'part': 'statistics,snippet', 'id': ','.join(ids), 'key': api_key},
        timeout=15
    )
    resultados = []
    for v in r2.json().get('items', []):
        stats   = v.get('statistics', {})
        snippet = v.get('snippet', {})
        fecha_str = snippet.get('publishedAt', '')
        fecha = pd.to_datetime(fecha_str[:10]) if fecha_str else pd.NaT
        resultados.append({
            'titulo':      snippet.get('title', ''),
            'canal':       snippet.get('channelTitle', ''),
            'fecha':       fecha,
            'año':         fecha.year if pd.notna(fecha) else None,
            'vistas':      int(stats.get('viewCount', 0)),
            'likes':       int(stats.get('likeCount', 0)),
            'comentarios': int(stats.get('commentCount', 0)),
            'idioma':      lang,
            'query':       query
        })
    return pd.DataFrame(resultados)


# =============================================================================
# HIPÓTESIS 3
# =============================================================================

def vocab_limpio(df):
    """Devuelve el vocabulario de un guion sin stopwords ni símbolos."""
    stop_words = set(stopwords.words('english'))
    palabras = df['Character_dialogue'].str.cat(sep=' ').lower().split()
    return [w for w in palabras if w not in stop_words and w.isalpha()]


def top_personajes(df, n=10):
    """Devuelve los n personajes con más líneas de diálogo (Series)."""
    return df.groupby('Character_Name').size().sort_values(ascending=True).tail(n)


def top_frases(df, n=5):
    """Devuelve las n frases más largas con el personaje que las pronuncia (DataFrame)."""
    return df.nlargest(n, 'num_palabras')[['Character_Name', 'num_palabras']].reset_index(drop=True)