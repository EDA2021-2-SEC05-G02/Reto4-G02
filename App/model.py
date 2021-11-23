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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from math import modf
from os import error
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """
    Inicializa el analizador 
    """
    try:
        analyzer = {
        'connections': None,
        'onlyroute': None,
        'paths': None,
        }

        """
        Se crea un mapa de los aeropuertos por IATA 
        """

        analyzer['IATA_Airport'] = mp.newMap(numelements=9076, 
                                         maptype='CHAINING',
                                         loadfactor=4.0,
                                         comparefunction=compareAirportIDs)

        """
        Se crea el mapa de los aeropuertos por nombre
        """
        analyzer['Name_Airport'] = mp.newMap(numelements=9076, 
                                         maptype='CHAINING',
                                         loadfactor=4.0,
                                         comparefunction=compareAirportIDs)


        """
        Se crea un grafo dirigido de las conexiones de las rutas
        """


        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=92606,
                                              comparefunction=compareAirportIDs)

        """
        Se crea un grafo no dirigido de las conexiones de las rutas
        """

        analyzer['onlyroute'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=92606,
                                              comparefunction=compareAirportIDs)


        """
        Se crea un mapa de las ciudades
        """
        analyzer['Cities'] = mp.newMap(numelements=92606,
                                        maptype='CHAINING',
                                        loadfactor=4.0,
                                        comparefunction=compareCities)
        
        


        return analyzer
        
    except Exception as exp:
        error.reraise(exp, 'Error in model:newAnalyzer')


# Funciones para agregar informacion a los  mapas

def addIATA_Airport(analyzer, airport):
    """
    Se agrega al mapa de aeropuertos el key(IATA) y value(aeropuerto).
    """
    mp.put(analyzer['IATA_Airport'], airport['IATA'], airport)
    return analyzer


def addName_Airport(analyzer, airport):
    """
    Se agrega al mapa de aeropuertos el key(Name) y value(IATA).
    """
    mp.put(analyzer['Name_Airport'], airport['Name'], airport['IATA'])
    return analyzer


def AddCity(analyzer, city):
    """
    Se agrega al mapa de ciudades el key(City) y value(city).
    """
    mp.put(analyzer['Cities'], city['city_ascii'], city)
    return analyzer

# Funciones para agregar informacion grafos

def addVertex(analyzer, airport):
    """
    Adiciona identificador IATA del aeropuerto como vertice del grafo

    """
    try: 
        if not gr.containsVertex(analyzer['connections'], airport['IATA']):
            gr.insertVertex(analyzer['connections'], airport['IATA'])
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'Error in model:addAirport')


def AddConnections(analyzer, routes):
    """
    Adiciona un arco entre dos aeropuertos.

    """
    edge = gr.getEdge(analyzer['connections'], routes['Departure'], routes['Destination'])
    if edge is None:
        gr.addEdge(analyzer['connections'], routes['Departure'], routes['Destination'], routes['distance_km'])

    edgeDestinationtoDeparture = gr.getEdge(analyzer['connections'], routes['Destination'], routes['Departure'])
    

    """
    Si el arco de destino a origen del grafo dirigido no esta vacio, se agregan los vertices de destino y origen al grafo no dirigido.
    Si el arco de destino a origen del grafo no dirigido esta vacio, se agrega el arco de destino a origen junto con el peso.

    """

    if edgeDestinationtoDeparture is not None:
        # Si no se contiene el vertice de destination en el grafo no dirigido, se agrega
        if not gr.containsVertex(analyzer['onlyroute'], routes['Destination']):
            gr.insertVertex(analyzer['onlyroute'], routes['Destination'])
        
        # Si no se contiene el vertice de departure en el grafo no dirigido, se agrega
        if not gr.containsVertex(analyzer['onlyroute'], routes['Departure']):
            gr.insertVertex(analyzer['onlyroute'], routes['Departure'])
        
        # Si arco que se busca obtener esta vacio, se agrega
        if gr.getEdge(analyzer['onlyroute'], routes['Destination'], routes['Departure']) is None:
            gr.addEdge(analyzer['onlyroute'], routes['Destination'], routes['Departure'], routes['distance_km'])

    return analyzer, edgeDestinationtoDeparture is not None


# Funciones de consulta

def Kosajaru(analyzer):
    """
    Se obtiene Kosajaru
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])


def SearchbyIATA(analyzer, IATA):
    """
    Buscar aeropuerto por IATA
    """        
    return me.getValue(mp.get(analyzer['IATA_Airport'], IATA))
    
def totalAirperGraph(analyzer):
    """
    Retorna el total de aeropuertos (vertices) de los grafos
    """
    conections = gr.numVertices(analyzer['connections'])
    onlyroute = gr.numVertices(analyzer['onlyroute'])
    return conections, onlyroute

def totalConnectionsperGraph(analyzer):
    """
    Retorna el total arcos de los grafos
    """
    conections = gr.numEdges(analyzer['connections'])
    onlyroute = gr.numEdges(analyzer['onlyroute'])
    return conections, onlyroute


def CitySize(analyzer):
    """
    Retorna el tamaño del mapa de ciudades
    """
    return mp.size(analyzer['Cities'])


# Requerimientos

#! Req 1

def AirInterconection(analyzer):

    """
    Retorna la lista de aeropuertos que tienen conexiones entre ellos en cada uno de los grafos y el total de conexiones
    """
    pass

#! Req 2

def AirCluster(analyzer, vertexA, vertexB):
    """
    Retorna el total de clusters presentes en la red de aeropuertos y devuelve un valor booleano si los dos aeropuertos estan en el mismo cluster.
    """
    total = scc.connectedComponents(analyzer['components'])
    samecluster =  scc.stronglyConnected(analyzer['components'], vertexA, vertexB)    
    return total, samecluster

# Funciones utilizadas para comparar elementos dentro de una lista

def compareAirportIDs(iatacode , airport):
    """
    Compara dos identificadores de aeropuertos
    """
    airportcode = me.getKey(airport)
    if (iatacode == airportcode):
        return 0
    elif (iatacode > airportcode):
        return 1
    else:
        return -1

def compareCities(city1 , city2):
    """
    Compara dos ciudades
    """
    citykey = me.getKey(city2)
    if (city1 == citykey):
        return 0
    elif (city1 > citykey):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1







# Funciones de ordenamiento
