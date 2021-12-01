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

from App.model import Kosajaru
import config as cf
import model
import csv
import prettytable 
from prettytable import PrettyTable
from DISClib.ADT import list as lt

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
    # Carga de todos los datos
    routes = loadInfo(analyzer)
    firstAirport = routes[1]
    # Inicializa Kosajaru
    Kosajaru(analyzer)
    return firstAirport

def loadInfo(analyzer):
    """
    Airports File
    """
    airportfile = cf.data_dir + "airports_full.csv"
    input_file = csv.DictReader(open(airportfile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        model.addVertex(analyzer, airport)
        model.addIATA_Airport(analyzer, airport)

    """
    Routes file
    """

    routesfile = cf.data_dir + "routes_full.csv"
    routes_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    first = True
    first_airport = None

    for routes in routes_file:
        _,dual = model.AddConnections(analyzer, routes)
        if dual and first:
            first = False
            first_airport = routes['Departure']
    
    first = model.SearchbyIATA(analyzer, first_airport)

    """
    Cities file
    """

    worldcitiesfile = cf.data_dir + "worldcities.csv"
    city_file = csv.DictReader(open(worldcitiesfile, encoding="utf-8"),
                                delimiter=",")
    for city in city_file:
        model.addCity(analyzer, city)
        
    return analyzer, first


def FirstAirportandLastCity():
    worldcitiesfile = cf.data_dir + "worldcities.csv"
    input_file = csv.DictReader(open(worldcitiesfile, encoding="utf-8"),
                                delimiter=",")
    lista = list(input_file)
    lastcity = lista[-1]

    airportfile = cf.data_dir + "airports_full.csv"
    input_file = csv.DictReader(open(airportfile, encoding="utf-8"),
                                delimiter=",")

    firstairport = next(input_file)
    return firstairport, lastcity
    



def SearchCity(analyzer, city):
    return model.SearchCity(analyzer, city)

def totalAirperGraph(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalAirperGraph(analyzer)


def totalConnectionsperGraph(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnectionsperGraph(analyzer)


def AirCluster(analyzer,vertexA, vertexB):
    """
    Numero de componentes fuertemente conectados
    """
    return model.AirCluster(analyzer,  vertexA, vertexB)


def getFistAirportperGraph(analyzer):
    """
    Primera parada del grafo
    """
    return model.getFistAirportperGraph(analyzer)

def CitySize(analyzer):
    """
    Numero de ciudades
    """
    return model.CitySize(analyzer)

def Kosaraju(analyzer):
    """
    Kosaraju
    """
    return model.Kosaraju(analyzer)

def OutOfService(analyzer, airIata):
    """
    Req 5
    """
    return model.OutOfService(analyzer, airIata)


def Mapa(info):
    """
    Req 7
    """
    return model.Mapa(info)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
