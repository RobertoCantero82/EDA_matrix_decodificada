# ─────────────────────────────────────────────
# Librerías
# ─────────────────────────────────────────────

import os
import time

# ─────────────────────────────────────────────
# Directorio de trabajo
# ─────────────────────────────────────────────

# Sitúa el directorio de trabajo en la raíz del proyecto (EDA_matrix_decodificada/)
# independientemente de desde dónde se ejecute el script.
# Esto garantiza que todas las rutas relativas del código (src/datos/...) funcionen siempre.
# __file__ es la ruta absoluta de este archivo (main.py)
# dirname lo sube un nivel: src/codigo/ → src/
# dirname de nuevo lo sube otro nivel: src/ → EDA_matrix_decodificada/
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

import numpy as np
import pandas as pd

import arxiv
from dotenv import load_dotenv

from funciones import (
    extraer_generos, sci_fi, extraer_efectos,
    ngrams, buscar_videos_youtube,
    vocab_limpio, top_personajes, top_frases,
)

# ─────────────────────────────────────────────
# Recursos NLTK
# ─────────────────────────────────────────────

nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)


# =============================================================================
# HIPÓTESIS 1 — The Matrix revolucionó el género de la ciencia ficción
# =============================================================================

# ── Parte 1: Evolución de los presupuestos ───────────────────────────────────

OUTPUT_DIR_H1 = 'src/datos/procesados/hipotesis_1'
os.makedirs(OUTPUT_DIR_H1, exist_ok=True)

ruta_hipotesis1 = "src/datos/brutos/hipotesis_1/tmdb_5000_movies.csv"

df_5000movies = pd.read_csv(ruta_hipotesis1)
print(f"Dataset cargado con {df_5000movies.shape[0]} películas y {df_5000movies.shape[1]} columnas")

columnas_fuera = ["homepage", "keywords", "original_language", "original_title", "overview", "popularity", "production_countries", "production_companies", "runtime", "spoken_languages", "status", "tagline", "vote_average", "vote_count"]

df_5000movies_limpio = df_5000movies.drop(columns=columnas_fuera)
df_5000movies_limpio = df_5000movies_limpio.dropna(subset=["release_date"])
df_5000movies_limpio["genres"] = df_5000movies_limpio["genres"].apply(extraer_generos)

df_5000movies_scifi = df_5000movies_limpio[df_5000movies_limpio["genres"].apply(sci_fi)]
df_5000movies_scifi['release_date'] = pd.to_datetime(df_5000movies_scifi['release_date'])
df_5000movies_scifi['year'] = df_5000movies_scifi['release_date'].dt.year
df_5000movies_scifi = df_5000movies_scifi[df_5000movies_scifi['budget'] > 0]

df_5000movies_scifi.to_csv('src/datos/procesados/hipotesis_1/peliculas_scifi_presupuestos.csv', index=False)

presupuesto_anual = df_5000movies_scifi.groupby('year')['budget'].mean().reset_index()
presupuesto_anual.columns = ['year', 'presupuesto_medio']
presupuesto_anual['presupuesto_medio'] = presupuesto_anual['presupuesto_medio'].round(0).astype(int)
presupuesto_anual = presupuesto_anual[presupuesto_anual['year'] >= 1977]

fig, ax = plt.subplots(figsize=(14, 6))

colores = []
for year in presupuesto_anual['year']:
    if year == 1978:
        colores.append('#204829')
    elif year == 1999:
        colores.append('red')
    elif year < 1999:
        colores.append('#22b455')
    else:
        colores.append('#92e5a1')

ax.bar(presupuesto_anual['year'], presupuesto_anual['presupuesto_medio'] / 1_000_000, color=colores, alpha=0.8)
ax.axvline(1999, color='#80ce87', linestyle='--', linewidth=2)

leyenda = [
    Patch(color='#80ce87', label='Superman (1978)'),
    Patch(color='#22b455', label='Antes de The Matrix'),
    Patch(color='#80ce87', label='The Matrix (1999)'),
    Patch(color='#92e5a1', label='Después de The Matrix'),
]
ax.legend(handles=leyenda, fontsize=10)
ax.set_title('Presupuesto medio de películas de ciencia ficción (1977–2016)', fontsize=18, fontweight='bold')
ax.set_xlabel('Año', fontsize=12)
ax.set_ylabel('Presupuesto medio (en millones de dólares)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR_H1, 'presupuesto_scifi.png'), dpi=150, bbox_inches='tight')
plt.show()

# ── Parte 2: Evolución de los especialistas en VFX ───────────────────────────

creditos = pd.read_csv('src/datos/brutos/hipotesis_1/tmdb_5000_credits.csv')
creditos['efectos'] = creditos['crew'].apply(extraer_efectos)
creditos['total_personas_efectos'] = creditos['efectos'].apply(len)

df_efectos = df_5000movies_scifi.merge(creditos[['movie_id', 'total_personas_efectos']], left_on='id', right_on='movie_id')
df_efectos.to_csv('src/datos/procesados/hipotesis_1/peliculas_scifi_efectos.csv', index=False)

efectos_anual = df_efectos.groupby('year')['total_personas_efectos'].mean().reset_index()
efectos_anual.columns = ['year', 'media_trabajadores_efectos']
efectos_anual['media_trabajadores_efectos'] = efectos_anual['media_trabajadores_efectos'].round(0).astype(int)
efectos_anual = efectos_anual[efectos_anual['year'] >= 1977]

fig, ax = plt.subplots(figsize=(14, 6))

colores = []
for year in efectos_anual['year']:
    if year == 1978:
        colores.append('#204829')
    elif year == 1999:
        colores.append('red')
    elif year < 1999:
        colores.append('#22b455')
    else:
        colores.append('#92e5a1')

ax.bar(efectos_anual['year'], efectos_anual['media_trabajadores_efectos'], color=colores, alpha=0.8)
ax.axvline(1999, color='#80ce87', linestyle='--', linewidth=2)

leyenda = [
    Patch(color='#80ce87', label='Superman (1978)'),
    Patch(color='#22b455', label='Antes de The Matrix'),
    Patch(color='#80ce87', label='The Matrix (1999)'),
    Patch(color='#92e5a1', label='Después de The Matrix'),
]
ax.legend(handles=leyenda, fontsize=10)
ax.set_title('Especialistas en VFX en películas de ciencia ficción (1977–2016)', fontsize=18, fontweight='bold')
ax.set_xlabel('Año', fontsize=12)
ax.set_ylabel('Número medio de especialistas VFX', fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR_H1, 'especialistas_vfx.png'), dpi=150, bbox_inches='tight')
plt.show()


# =============================================================================
# HIPÓTESIS 2 — La realidad como simulación: de la ficción a la cultura popular
# =============================================================================

# ── Parte 1: Análisis de papers en arXiv ─────────────────────────────────────

cliente = arxiv.Client(page_size=10, delay_seconds=3, num_retries=3)

queries = [
    "simulation hypothesis physics",
    "simulated universe cosmology",
    "digital physics reality",
    "Nick Bostrom simulation argument",
    "simulation argument philosophy"
]

todos_resultados = []
for query in queries:
    busqueda = arxiv.Search(query=query, max_results=50, sort_by=arxiv.SortCriterion.Relevance)
    for paper in cliente.results(busqueda):
        todos_resultados.append({
            "titulo": paper.title,
            "anio": paper.published.year,
            "categoria": paper.primary_category,
            "query": query
        })

df_papers = pd.DataFrame(todos_resultados).drop_duplicates(subset='titulo')

categorias_relevantes = [
    'physics.pop-ph', 'gr-qc', 'quant-ph',
    'astro-ph', 'astro-ph.CO', 'physics.hist-ph',
]
df_papers_filtrado = df_papers[df_papers['categoria'].isin(categorias_relevantes)]

# ── Parte 2: Google Ngrams ────────────────────────────────────────────────────

OUTPUT_DIR = 'src/datos/procesados/hipotesis_2'
os.makedirs(OUTPUT_DIR, exist_ok=True)

terminos_en = ['simulation theory', 'virtual reality', 'what is reality', 'philosophy of mind']
terminos_es = ['teoría de la simulación', 'realidad virtual', 'qué es la realidad', 'filosofía de la mente']

print('Descargando libros en inglés...')
df_en = ngrams(terminos_en, corpus='en-2019')
print(f'OK — {len(df_en)} años')

print('Descargando libros en español...')
df_es = ngrams(terminos_es, corpus='es-2019')
print(f'OK — {len(df_es)} años')

df_en.to_csv(os.path.join(OUTPUT_DIR, 'ngrams_en.csv'), index=False)
df_es.to_csv(os.path.join(OUTPUT_DIR, 'ngrams_es.csv'), index=False)
print('CSVs guardados')

fig, axes = plt.subplots(2, 4, figsize=(18, 9))
fig.patch.set_facecolor('#0f0f23')

colores_en = ['#4fc3f7', '#69f0ae', '#ffca28', '#ff7043']
labels_en  = ['"simulation theory"', '"virtual reality"', '"what is reality"', '"philosophy of mind"']
colores_es = ['#80cbc4', '#a5d6a7', '#ffe082', '#ef9a9a']
labels_es  = ['"teoría de la\nsimulación"', '"realidad virtual"', '"qué es la realidad"', '"filosofía de la mente"']

for i, (col, label, color) in enumerate(zip(terminos_en, labels_en, colores_en)):
    ax = axes[0][i]
    ax.set_facecolor('#1a1a2e')
    if col in df_en.columns:
        ax.fill_between(df_en['year'], df_en[col], alpha=0.25, color=color)
        ax.plot(df_en['year'], df_en[col], color=color, linewidth=2)
    ax.axvline(1999, color='white', linestyle='--', linewidth=1.4, alpha=0.6)
    ax.text(2000, ax.get_ylim()[1] * 0.88, '1999', color='white', fontsize=7, alpha=0.7)
    ax.set_title(label, fontsize=9.5, fontweight='bold', color=color)
    ax.tick_params(colors='white', labelsize=8)
    ax.spines[:].set_color('#444466')
    ax.grid(True, alpha=0.10, color='white')
    if i == 0:
        ax.set_ylabel('Frecuencia en libros (EN)', color='white', fontsize=9)

for i, (col, label, color) in enumerate(zip(terminos_es, labels_es, colores_es)):
    ax = axes[1][i]
    ax.set_facecolor('#1a1a2e')
    if col in df_es.columns:
        ax.fill_between(df_es['year'], df_es[col], alpha=0.25, color=color)
        ax.plot(df_es['year'], df_es[col], color=color, linewidth=2)
    ax.axvline(1999, color='white', linestyle='--', linewidth=1.4, alpha=0.6)
    ax.text(2000, ax.get_ylim()[1] * 0.88, '1999', color='white', fontsize=7, alpha=0.7)
    ax.set_title(label, fontsize=9.5, fontweight='bold', color=color)
    ax.tick_params(colors='white', labelsize=8)
    ax.spines[:].set_color('#444466')
    ax.grid(True, alpha=0.10, color='white')
    if i == 0:
        ax.set_ylabel('Frecuencia en libros (ES)', color='white', fontsize=9)

fig.suptitle('Conceptos filosóficos de Matrix en libros publicados entre 1980 y 2019\nFila superior: inglés  |  Fila inferior: español',
             fontsize=13, fontweight='bold', color='white', y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'ngrams_bilingue.png'), dpi=150, bbox_inches='tight', facecolor='#0f0f23')

# ── Parte 3: YouTube ──────────────────────────────────────────────────────────

load_dotenv('../.env')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
print('Key cargada:', YOUTUBE_API_KEY is not None)

queries_en = [
    'simulation theory explained matrix',
    'are we living in a simulation philosophy',
    'matrix philosophy explained',
    'what is reality philosophy',
    'virtual reality consciousness philosophy'
]
queries_es = [
    'teoría de la simulación matrix explicada',
    'vivimos en una simulación filosofía',
    'filosofía de matrix explicada',
    'qué es la realidad filosofía',
    'realidad virtual conciencia filosofía'
]

dfs = []
print('Buscando en inglés...')
for q in queries_en:
    print(f'  → {q}')
    dfs.append(buscar_videos_youtube(q, YOUTUBE_API_KEY, lang='en'))
    time.sleep(1)

print('Buscando en español...')
for q in queries_es:
    print(f'  → {q}')
    dfs.append(buscar_videos_youtube(q, YOUTUBE_API_KEY, lang='es'))
    time.sleep(1)

df_youtube = pd.concat(dfs).drop_duplicates(subset='titulo').reset_index(drop=True)
df_youtube = df_youtube[df_youtube['vistas'] > 0]
df_youtube['fecha'] = pd.to_datetime(df_youtube['fecha'], errors='coerce')
df_youtube['año'] = df_youtube['fecha'].dt.year

print(f'\nVídeos únicos: {len(df_youtube)}')
print(f'  Inglés:  {len(df_youtube[df_youtube["idioma"]=="en"])}')
print(f'  Español: {len(df_youtube[df_youtube["idioma"]=="es"])}')

df_youtube.to_csv(os.path.join(OUTPUT_DIR, 'youtube_matrix_filosofia.csv'), index=False)

por_año_idioma = df_youtube.groupby(["año", "idioma"])["vistas"].sum().reset_index()
por_año_idioma["vistas_M"] = por_año_idioma["vistas"] / 1_000_000
pivot = por_año_idioma.pivot(index="año", columns="idioma", values="vistas_M").fillna(0)
pivot = pivot[pivot.index >= 2010]

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor("#0f0f23")
ax.set_facecolor("#1a1a2e")

años = pivot.index
x = np.arange(len(años))
ancho = 0.55

ax.bar(x, pivot.get("en", 0), ancho, color="#4fc3f7", alpha=0.85, label="Inglés", zorder=3)
ax.bar(x, pivot.get("es", 0), ancho, bottom=pivot.get("en", 0), color="#69f0ae", alpha=0.85, label="Español", zorder=3)

años_lista = list(años)
for i, año in enumerate(años):
    en_val = pivot["en"].get(año, 0) if "en" in pivot.columns else 0
    es_val = pivot["es"].get(año, 0) if "es" in pivot.columns else 0
    total = en_val + es_val
    if total > 5:
        ax.text(i, total + 0.5, f"{total:.0f}M", ha="center", va="bottom", fontsize=8, color="white", fontweight="bold")

for año_evento, label, color in [
    (2016, 'Musk\n"simulación"', "#ffca28"),
    (2021, "Resurrections", "#ff7043"),
    (2022, "ChatGPT", "#ce93d8"),
]:
    if año_evento in años_lista:
        idx = años_lista.index(año_evento)
        ax.axvline(idx - 0.5, color=color, linestyle="--", linewidth=1.2, alpha=0.6)
        ylim = ax.get_ylim()
        ax.text(idx - 0.38, (ylim[1] - ylim[0]) * 0.88 + ylim[0], label, color=color, fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#0f0f23", alpha=0.6, edgecolor="none"))

ax.set_xticks(x)
ax.set_xticklabels(años, rotation=45, color="white", fontsize=9)
ax.set_xlabel("Año", fontsize=12, color="white")
ax.set_ylabel("Visualizaciones totales (millones)", fontsize=12, color="white")
ax.tick_params(colors="white")
ax.spines[:].set_color("#444466")
ax.grid(True, axis="y", alpha=0.12, color="white")
ax.set_title("Visualizaciones anuales en YouTube\nsobre filosofía, simulación y realidad virtual (inglés vs español)",
             fontsize=13, fontweight="bold", color="white", pad=12)
ax.legend(fontsize=11, framealpha=0.3, facecolor="#1a1a2e", labelcolor="white", edgecolor="#555577", loc="upper left")
ax.text(0.01, 0.03,
        "Búsquedas: simulation theory matrix, matrix philosophy, what is reality, realidad virtual, vivimos en una simulación...",
        transform=ax.transAxes, fontsize=7.5, color="#aaaaaa", style="italic")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "youtube_barras.png"), dpi=150, bbox_inches="tight", facecolor="#0f0f23")


# =============================================================================
# HIPÓTESIS 3 — El declive de la saga: ¿motivada por el descenso de calidad?
# =============================================================================

DATA_DIR = os.path.join('src', 'datos', 'procesados', 'hipotesis_3')
OUTPUT_DIR = DATA_DIR

m1 = pd.read_csv(os.path.join(DATA_DIR, 'matrix1_clean.csv'))
m2 = pd.read_csv(os.path.join(DATA_DIR, 'matrix2_clean.csv'))
m3 = pd.read_csv(os.path.join(DATA_DIR, 'matrix3_clean.csv'))

print(f'Matrix 1: {len(m1)} líneas de diálogo')
print(f'Matrix 2: {len(m2)} líneas de diálogo')
print(f'Matrix 3: {len(m3)} líneas de diálogo')

sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

for df in [m1, m2, m3]:
    df['sentimiento'] = df['Character_dialogue'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
    df['num_palabras'] = df['Character_dialogue'].str.split().str.len()

vocab1 = vocab_limpio(m1)
vocab2 = vocab_limpio(m2)
vocab3 = vocab_limpio(m3)

riqueza1 = len(set(vocab1)) / len(vocab1) * 100
riqueza2 = len(set(vocab2)) / len(vocab2) * 100
riqueza3 = len(set(vocab3)) / len(vocab3) * 100

pers1 = m1['Character_Name'].nunique()
pers2 = m2['Character_Name'].nunique()
pers3 = m3['Character_Name'].nunique()

print('Métricas calculadas:')
print(f'  Personajes: {pers1} / {pers2} / {pers3}')
print(f'  Riqueza léxica: {riqueza1:.1f}% / {riqueza2:.1f}% / {riqueza3:.1f}%')
print(f'  Sentimiento medio: {m1["sentimiento"].mean():.3f} / {m2["sentimiento"].mean():.3f} / {m3["sentimiento"].mean():.3f}')
print(f'  Media palabras/frase: {m1["num_palabras"].mean():.1f} / {m2["num_palabras"].mean():.1f} / {m3["num_palabras"].mean():.1f}')

# ── Gráfico 1: Top 10 personajes por líneas de diálogo (horizontal, 3 columnas) ──

top1 = top_personajes(m1)
top2 = top_personajes(m2)
top3 = top_personajes(m3)

fig, axes = plt.subplots(1, 3, figsize=(16, 7))
fig.patch.set_facecolor('#020204')

datos = [
    (top1, 'Matrix 1', '#204829', f'{pers1} personajes en total'),
    (top2, 'Matrix 2', '#22b455', f'{pers2} personajes en total'),
    (top3, 'Matrix 3', '#92e5a1', f'{pers3} personajes en total'),
]

for ax, (top, titulo, color, subtitulo) in zip(axes, datos):
    ax.set_facecolor('#020204')
    bars = ax.barh(top.index, top.values, color=color, alpha=0.80, zorder=3)
    for bar, val in zip(bars, top.values):
        ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2, str(val), va='center', fontsize=9, color='white')
    ax.set_title(f'{titulo}\n{subtitulo}', fontsize=12, fontweight='bold', color=color, pad=10)
    ax.set_xlabel('Líneas de diálogo', fontsize=10, color='white')
    ax.tick_params(colors='white', labelsize=9)
    ax.spines[:].set_color('#204829')
    ax.grid(True, axis='x', alpha=0.10, color='white')

fig.suptitle('Top 10 personajes por líneas de diálogo — Saga Matrix\n¿Cómo se fragmenta el protagonismo en las secuelas?',
             fontsize=13, fontweight='bold', color='white', y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'personajes_dialogo.png'), dpi=150, bbox_inches='tight', facecolor='#020204')
plt.show()

# ── Gráfico 2: Complejidad del guion vs Valoración IMDb ──────────────────────

peliculas = ['The Matrix', 'Matrix Reloaded', 'Matrix Revolutions']
imdb = [8.7, 7.2, 6.7]
personajes = [pers1, pers2, pers3]
riqueza = [riqueza1, riqueza2, riqueza3]

fig, ax1 = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#020204')
ax1.set_facecolor('#020204')

x = range(3)
bars1 = ax1.bar([i - 0.2 for i in x], personajes, width=0.35, color='#22b455', alpha=0.80, label='Nº personajes', zorder=3)
bars2 = ax1.bar([i + 0.2 for i in x], riqueza, width=0.35, color='#92e5a1', alpha=0.80, label='Riqueza léxica (%)', zorder=3)

for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{int(bar.get_height())}', ha='center', fontsize=10, color='white', fontweight='bold')
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{bar.get_height():.1f}%', ha='center', fontsize=10, color='white', fontweight='bold')

ax1.set_ylabel('Personajes / Riqueza léxica (%)', fontsize=11, color='white')
ax1.set_xticks(range(3))
ax1.set_xticklabels(peliculas, fontsize=12, color='white')
ax1.set_ylim(0, 100)
ax1.tick_params(colors='white')
ax1.spines[:].set_color('#204829')
ax1.grid(axis='y', alpha=0.12, color='white')

ax2 = ax1.twinx()
ax2.plot(range(3), imdb, color='#80ce87', linewidth=2.5, marker='o', markersize=10, label='IMDb', zorder=4)
ax2.set_ylabel('Valoración IMDb', fontsize=11, color='#80ce87')
ax2.set_ylim(0, 10)
ax2.tick_params(axis='y', colors='#92e5a1')
ax2.spines[:].set_color('#204829')

for i, v in enumerate(imdb):
    ax2.annotate(f'{v}', xy=(i, v), xytext=(0, 12), textcoords='offset points',
                 ha='center', fontsize=11, color='#80ce87', fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
           fontsize=10, framealpha=0.3, facecolor='#020204',
           labelcolor='white', edgecolor='#80ce87', loc='upper right')

ax1.set_title('Complejidad del guion vs Valoración IMDb — Saga Matrix',
              fontsize=13, fontweight='bold', color='white', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'complejidad_imdb.png'), dpi=150, bbox_inches='tight', facecolor='#020204')
plt.show()

# ── Gráfico 3: Top personajes apilado vertical (3 subplots) ──────────────────

fig, axes = plt.subplots(3, 1, figsize=(12, 14))
fig.patch.set_facecolor('#020204')

for ax, top, pelicula, color in zip(axes, [top1, top2, top3],
                                    ['The Matrix', 'Matrix Reloaded', 'Matrix Revolutions'],
                                    ['#204829', '#22b455', '#92e5a1']):
    ax.set_facecolor('#020204')
    labels = top.index.tolist()
    vals = top.values
    bars = ax.barh(list(range(len(top))), vals, color=color, alpha=0.80, zorder=3)
    for bar, val in zip(bars, vals):
        ax.text(val + 0.3, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=9, color='white')
    ax.set_yticks(list(range(len(top))))
    ax.set_yticklabels(labels, fontsize=9, color='white')
    ax.set_xlabel('Líneas de diálogo', fontsize=10, color='white')
    ax.set_title(f'{pelicula} — Top personajes', fontsize=12, fontweight='bold', color=color, pad=8)
    ax.tick_params(colors='white')
    ax.spines[:].set_color('#204829')
    ax.grid(True, axis='x', alpha=0.10, color='white')

fig.suptitle('Top personajes por líneas de diálogo — Saga Matrix',
             fontsize=13, fontweight='bold', color='white', y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'personajes_dialogo_vertical.png'), dpi=150, bbox_inches='tight', facecolor='#020204')
plt.show()

# ── Gráfico 4: Las 5 frases más largas por película ──────────────────────────

top1 = top_frases(m1)
top2 = top_frases(m2)
top3 = top_frases(m3)

fig, axes = plt.subplots(3, 1, figsize=(12, 14))
fig.patch.set_facecolor('#020204')

for ax, top, pelicula, color in zip(axes, [top1, top2, top3],
                                    ['The Matrix', 'Matrix Reloaded', 'Matrix Revolutions'],
                                    ['#204829', '#22b455', '#92e5a1']):
    ax.set_facecolor('#020204')
    labels = top['Character_Name'].tolist()
    vals = top['num_palabras'].values
    bars = ax.barh(list(range(len(top))), vals, color=color, alpha=0.80, zorder=3)
    for bar, val in zip(bars, vals):
        ax.text(val + 0.3, bar.get_y() + bar.get_height()/2, f'{val} palabras', va='center', fontsize=9, color='white')
    ax.set_yticks(list(range(len(top))))
    ax.set_yticklabels(labels, fontsize=9, color='white')
    ax.set_xlabel('Palabras', fontsize=10, color='white')
    ax.set_title(f'{pelicula} — Top 5 frases más largas', fontsize=12, fontweight='bold', color=color, pad=8)
    ax.tick_params(colors='white')
    ax.spines[:].set_color('#204829')
    ax.grid(True, axis='x', alpha=0.10, color='white')

fig.suptitle('Las frases más largas de cada película — Saga Matrix\n¿Quién pronuncia los grandes monólogos y en qué entrega?',
             fontsize=13, fontweight='bold', color='white', y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'longitud_B_top_frases.png'), dpi=150, bbox_inches='tight', facecolor='#020204')
plt.show()