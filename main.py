from fastapi import FastAPI
import requests
import pandas as pd
import json

# ---------------------------------------------------
# DESCARGAR DATOS DEL JSON
# ---------------------------------------------------

url = "https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json"

app = FastAPI(
    title="API de Películas",
    description="Servidor API para consultar y modificar datos del JSON de películas.",
    version="1.0"
)             
response = requests.get(url)

if response.status_code != 200:
        raise Exception("Error al descargar el JSON")

movies = response.json()


print("Datos cargados correctamente.")
# ---------------------------------------------------
# CREAR LA APLICACIÓN FASTAPI
# ---------------------------------------------------

@app.get("/")
def home():
    """
    Endpoint raíz.
    Retorna un mensaje indicando que la API está funcionando.
    """
    return {"mensaje": "API de películas funcionando correctamente"}


@app.get("/movies")
def get_movies(page: int = 1, size: int = 50):
    """
    Retorna una lista paginada de películas.

    Parámetros:
        page (int): número de página (comienza en 1).
        size (int): cantidad de elementos por página.

    Retorna:
        Un diccionario con:
            - page: número de página
            - size: tamaño de página
            - total: cantidad total de películas
            - total_pages: cantidad total de páginas
            - data: lista de películas de esa página
    """
    total = len(movies)
    total_pages = (total + size - 1) // size  # Redondeo hacia arriba

    if page < 1 or page > total_pages:
        return {"error": "Página fuera de rango"}

    start = (page - 1) * size
    end = start + size

    return {
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages,
        "data": movies[start:end]
    }


@app.get("/movies/{id}")
def get_movie_by_id(id: int):
    """
    Busca una película por su índice dentro de la lista.
    
    Parámetros:
        id (int): posición de la película en la lista.
    
    Retorna:
        La película correspondiente o un mensaje de error si el ID es inválido.
    """
    if id < 0 or id >= len(movies):
        return {"error": "ID fuera de rango"}
    return movies[id]


@app.get("/movies/title/")
def search_by_title(title: str = None):
    """
    Busca películas cuyos títulos contengan una palabra o texto dado.
    
    Parámetros:
        title (str): texto a buscar dentro del título.
    
    Retorna:
        Lista de películas cuyo título contiene el texto ingresado.
    """
    if title is None:
        return {"error": "Debe ingresar un título"}
    result = [m for m in movies if title.lower() in m["title"].lower()]
    return result


@app.get("/movies/year/")
def search_by_year(year: int = None):
    """
    Busca películas por año de estreno.
    
    Parámetros:
        year (int): año a buscar.
    
    Retorna:
        Lista de películas estrenadas en ese año.
    """
    if year is None:
        return {"error": "Debe ingresar un año"}
    result = [m for m in movies if m["year"] == year]
    return result


@app.get("/movies/actor/")
def search_by_actor(actor: str = None):
    """
    Busca películas en función del nombre de un actor.
    
    Parámetros:
        actor (str): nombre del actor.
    
    Retorna:
        Lista de películas en las que participa ese actor.
    """
    if actor is None:
        return {"error": "Debe ingresar un actor"}
    result = [m for m in movies if actor.lower() in [c.lower() for c in m["cast"]]]
    return result


@app.get("/movies/genre/")
def search_by_genre(genre: str = None):
    """
    Busca películas según un género específico.
    
    Parámetros:
        genre (str): género a buscar (Drama, Action, Comedy, etc.).
    
    Retorna:
        Lista de películas que pertenecen a ese género.
    """
    if genre is None:
        return {"error": "Debe ingresar un género"}
    result = [m for m in movies if genre.lower() in [g.lower() for g in m["genres"]]]
    return result


# ---------------------------------------------------
# ENDPOINTS POST, PUT, DELETE (MODIFICACIÓN)
# ---------------------------------------------------

@app.post("/movies")
def add_movie(movie: dict):
    """
    Agrega una nueva película a la lista.
    
    Parámetros:
        movie (dict): objeto JSON que representa la nueva película.
    
    Retorna:
        Mensaje confirmando la operación y los datos agregados.
    """
    movies.append(movie)
    return {"mensaje": "Película agregada", "pelicula": movie}


@app.put("/movies/{id}")
def update_movie(id: int, new_data: dict):
    """
    Modifica los datos de una película existente.
    
    Parámetros:
        id (int): índice de la película a modificar.
        new_data (dict): datos a actualizar.
    
    Retorna:
        Mensaje confirmando la modificación y la película actualizada.
    """
    if id < 0 or id >= len(movies):
        return {"error": "ID fuera de rango"}
    movies[id].update(new_data)
    return {"mensaje": "Película actualizada", "pelicula": movies[id]}


@app.delete("/movies/{id}")
def delete_movie(id: int):
    """
    Elimina una película por su ID.
    
    Parámetros:
        id (int): índice de la película a eliminar.
    
    Retorna:
        Mensaje confirmando la eliminación y la película eliminada.
    """
    if id < 0 or id >= len(movies):
        return {"error": "ID fuera de rango"}
    eliminada = movies.pop(id)
    return {"mensaje": "Película eliminada", "pelicula": eliminada}