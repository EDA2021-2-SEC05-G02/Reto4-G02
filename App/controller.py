"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initAnalyzer():
    """
    Llama la funcion de inicializacion del modelo
    """
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos desde los archivos csv
    """
    # Carga de datos de aeropuertos
    loadAirports(analyzer)

    # Carga de datos de rutas
    loadRoutes(analyzer)

    # Carga de datos de ciudades
    LoadWorldCities(analyzer)

def loadAirports(analyzer):
    airportfile = cf.data_dir + "airports_full.csv"
    input_file = csv.DictReader(open(airportfile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        model.addAirport(analyzer, airport)
    return analyzer

def loadRoutes(analyzer):
    routesfile = cf.data_dir + "routes_full.csv"
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    for route in input_file:
        model.addRoute(analyzer, route)

    return analyzer

def LoadWorldCities(analyzer):
    worldcitiesfile = cf.data_dir + "worldcities.csv"
    input_file = csv.DictReader(open(worldcitiesfile, encoding="utf-8"),
                                delimiter=",")
    for city in input_file:
        model.addCity(analyzer, city)

    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
