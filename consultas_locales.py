from fastapi import FastAPI
import uvicorn
import pandas as pd
import requests
import json

url = "https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json"

print("Descargando datos...")
response = requests.get(url)

data = response.json()  # Lista de películas

print("Descarga completa.\n")

df = pd.DataFrame(data)

print("Primeras filas del dataset:")
print(df.head(), "\n")

print("Columnas disponibles:")
print(df.columns, "\n")


#______________________________________________________________


print("Base de datos cargada. Total de películas:", len(df))
print("\nCONSULTAS DISPONIBLES:")
print("1 - Buscar películas por título")
print("2 - Buscar películas por año")
print("3 - Buscar películas por actor")
print("4 - Buscar películas por género")
print("5 - Salir\n")

while True:
    opcion = input("Elegí una opción (1-5): ")

    # SALIR
    if opcion == "5":
        print("Saliendo del programa...")
        break

    # BUSCAR POR TÍTULO
    elif opcion == "1":
        texto = input("Ingresá texto del título a buscar: ")
        resultado = df[df["title"].str.contains(texto, case=False, na=False)]
        print("\nResultados:")
        print(resultado.head(20), "\n")

    # BUSCAR POR AÑO
    elif opcion == "2":
        anio = input("Ingresá un año (ej: 1994): ")
        if anio.isdigit():
            anio = int(anio)
            resultado = df[df["year"] == anio]
            print("\nResultados:")
            print(resultado.head(20), "\n")
        else:
            print("Año inválido.\n")

    # BUSCAR POR ACTOR
    elif opcion == "3":
        actor = input("Ingresá el nombre del actor: ")
        resultado = df[df["cast"].apply(lambda lista: actor.lower() in [a.lower() for a in lista])]
        print("\nResultados:")
        print(resultado.head(20), "\n")

    # BUSCAR POR GÉNERO
    elif opcion == "4":
        genero = input("Ingresá un género (Action, Drama, Comedy, etc.): ")
        resultado = df[df["genres"].apply(lambda lista: genero.lower() in [g.lower() for g in lista])]
        print("\nResultados:")
        print(resultado.head(20), "\n")

    else:
        print("Opción inválida.\n")
#---------------------------------------------------------------------