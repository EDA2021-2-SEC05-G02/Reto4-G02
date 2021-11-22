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
        'Airports': None,
        'Cities': None,
        'connections': None,
        'components': None,
        }

        """
        Se crea un mapa de los aeropuertos
        """

        analyzer['Airports'] = mp.newMap(numelements=9076, 
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
        # Falta - Crear grafo no dirigido 
        """




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


    

# Funciones para agregar informacion

def addAirport(analyzer, airport):
    """
    Adiciona identificador IATA del aeropuerto como vertice del grafo
    y se agrega al mapa de aeropuertos el key(IATA) y value(aeropuerto).
    """
    try: 
        if not gr.containsVertex(analyzer['connections'], airport['IATA']):
            gr.insertVertex(analyzer['connections'], airport['IATA'])
    
        mp.put(analyzer['Airports'], airport['IATA'], airport)

    except Exception as exp:
        error.reraise(exp, 'Error in model:addAirport')

def AddCity(analyzer, city):
    """
    Agrega una ciudad al mapa de ciudades
    """
    mp.put(analyzer['Cities'], city['city'], city)
    return analyzer


def AddConnections(analyzer, routes):
    """
    Adiciona un arco entre dos aeropuertos.
    Se obtiene el arco de departure a destination y viceversa.
    """
    edge = gr.getEdge(analyzer['connections'], routes['Departure'], routes['Destination'])
    if edge is None:
        gr.addEdge(analyzer['connections'], routes['Departure'], routes['Destination'], routes['distance_km'])

    edgeDeparturetoDestination = gr.getEdge(analyzer['connections'], routes['Departure'], routes['Destination'])
    edgeDestinationtoDeparture = gr.getEdge(analyzer['connections'], routes['Destination'], routes['Departure'])
    # Obtener el edge del grafo no dirigido y agregalo como vertice.
    
    return analyzer


# Funciones para creacion de datos

# Funciones de consulta

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])

def totalAir(analyzer):
    """
    Retorna el total de aeropuertos (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])



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
