![Portada del Proyecto](recursos/img/portada_eda_matrix.png)

## 🐇 Descripción del Proyecto

Este proyecto realiza un Análisis Exploratorio de Datos (EDA) sobre la saga cinematográfica. El objetivo es contrastar algunas afirmaciones, polémicas para quienes somos defensores de su calidad como obra, que suelen realizarse acerca de la trilogía original ([_The Matrix_](https://letterboxd.com/film/the-matrix/), [_The Matrix Reloaded_](https://letterboxd.com/film/the-matrix-reloaded/) y [_The Matrix Revolutions_](https://letterboxd.com/film/the-matrix-revolutions/)). Mis hipótesis hablarán sobre la repercusión de la trilogía en el cine moderno, abordarán el nexo entre su popularidad y los papers de las últimas décadas y, por último, el motivo por el que la saga no se arraigó entre las mejores de la historia.

Lo interesante del proyecto no es solo conocer un poco más en profundidad la saga, sino también tocar temas tan curiosos como la proliferación de los **efectos especiales** en el séptimo arte, cómo ha evolucionado el género de la **ciencia ficción**, si es posible que **nuestra realidad sea una simulación** o cómo son los **guiones de la saga**, que serán muy relevantes para poder comprobar si la trilogía fue empeorando en calidad narrativa o es que los espectadores no se preocuparon en explorar la historia más allá de la gran pantalla.  

## 💊 Hipótesis

1.- **_The Matrix_ revolucionó el género de la ciencia ficción:** la película estableció un nuevo estándar de inversión en efectos visuales, alterando la distribución de presupuestos en el posterior cine de ciencia ficción. A partir de entonces, Las películas del género optaron por impulsar los efectos digitales, incluso imitando algunos de los alucinantes trucos de la trilogía.

2.- **¿Vivimos en una simulación? Ciencia ficción vs Papers**: existe un incremento significativo en la producción académica sobre la [_Teoría de la Simulación_](https://es.wikipedia.org/wiki/Hip%C3%B3tesis_de_simulaci%C3%B3n) en el campo de la Astrofísica y la Cosmología a raíz del estreno de _The Matrix_, consolidando a la saga como un referente más allá de la ficción.

3.- **El declive de la saga: ¿motivada por el descenso de calidad?**: se propone que con una mayor narrativa y más términos complejos, menor es la conexión emocional y la valoración del público general. En realidad, quizás las películas no eran peores, sino que no llegaron a ser comprendidas.

## 🔌 Datos

Dado que la temática de las hipótesis es variada, también lo serán las distintas fuentes de datos que tengo que utilizar para poder contrastarlas. En este caso, a continuación muestro cada hipótesis y las fuentes que serán utilizadas:

1.- **_The Matrix_ revolucionó el género de la ciencia ficción:** utilizo datasets de métricas de cine, obtenidos de Kaggle. En concreto, uso [IMDb Dataset](https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset) y [TMDB 5000 Movie Dataset.](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

2.- **¿Vivimos en una simulación? Ciencia ficción vs Papers**: para contrastar la hipótesis uso las librerías arXiv y scholarly. Además, también miraré si me resulta de utilidad la API de [OpenAlex](https://openalex.org/).

3.- **El declive de la saga: ¿motivada por el descenso de calidad?**: para acabar he eligo unos datasets muy curiosos, ya que cada uno de ellos contiene las transcripciones de las películas, que me servirán para estudiar si los guiones eran peores o, simplemente, se fueron complicando. Los datasets están agrupados en Kaggle bajo el nombre [The Matrix](https://www.kaggle.com/datasets/nixongeno/the-matrix-movie-transcripts).

## 💻 Tecnologías Utilizadas

* **Lenguaje:** Python 3.12

* **Análisis de datos:** Pandas, NumPy.

* **Visualización:** Matplotlib.

* **Procesamiento de Lenguaje:** NLTK / SpaCy (para análisis de guiones).

* **Apoyo presentación y archivos:** Gemini (Nano Banana 2)

## 💾 Estructura del [Repositorio]()

#### CARPETAS:

* **presentacion/:** se incluye el archivo de soporte para la exposición del EDA (10 minutos).

* **recursos/:** carpeta con material multimedia (img, audio, video), que servirá de apoyo en la presentación.

* **src/:** carpeta que contiene la parte fundamental del proyecto.  

    * **codigo/:** módulos de Python y archivos necesarios para que el EDA sea funcional.

    * **datos/:** datasets originales y procesados.

    * **notebooks/:** cuadernos de Jupyter con pruebas realizadas para plantear hipótesis y su resolución.

    * **memoria.ipynb:** cuaderno principal con el desarrollo completo, limpiezas, visualizaciones y conclusiones.

#### ARCHIVOS: 

* **presentacion_EDA**: explicación inicial del proyecto, donde se incluye el tema elegido, una breve explicación de la película y la saga, las hipótesis planteadas y cómo serán los primeros pasos para poder obtener conclusiones profesionales.

* **README.md:** archivo que será el punto de partida de quien entra al repositorio de GitHub para conocer qué es lo que se encontrará al acceder al EDA.

_Nota: Los archivos contenidos en src/data/brutos/ no se incluyen en este repositorio y deben ser descargados de sus fuentes originales, debido a restricciones de tamaño de GitHub._