﻿"""
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


from os import error
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import mergesort as mer
from haversine import haversine #para instalar: pip install haversine
assert cf
import pandas as pd
import folium
import webbrowser


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Carga de Datos

# Construccion de modelos

def newAnalyzer():
    """
    Inicializa el analizador 
    """
    try:
        analyzer = {}

        analyzer['lt cities'] = lt.newList('ARRAY_LIST')
        analyzer['lt airports'] = lt.newList('ARRAY_LIST')
        analyzer['lt routes'] = lt.newList('ARRAY_LIST')

        """
        Se crea un arbol de los aeropuertos por IATA
        """

        analyzer['IATA_Airport'] = om.newMap(omaptype='RBT', comparefunction=compareString)

        analyzer['LatitudeIndex'] = om.newMap(omaptype='RBT', comparefunction=compareFloat)

        
        """
        Se crea un mapa de las ciudades
        """
        analyzer['cities'] = mp.newMap(numelements=41002, 
                                       maptype='CHAINING',
                                       loadfactor= 4.0,
                                       comparefunction=compareCity)

        """
        Se crea un mapa de los aeropueros
        """

        analyzer['airports'] = mp.newMap(numelements=9076,
                                         maptype='CHAINING',
                                         loadfactor= 4.0,
                                         comparefunction=compareAirportIDs)


        """
        Se crea un grafo dirigido de las conexiones de las rutas
        """


        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=92606,
                                              comparefunction=compareAirportIDs)

        analyzer['reverse connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=92606,
                                              comparefunction=compareAirportIDs)

        """
        Se crea un grafo no dirigido de las conexiones de las rutas
        """

        analyzer['doubleroute'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=92606,
                                              comparefunction=compareAirportIDs)

        return analyzer
        
    except Exception as exp:
        error.reraise(exp, 'Error in model:newAnalyzer')

# Funciones para agregar informacion a los mapas

def addCity(analyzer, city):
    info = {}
    info['city_ascii'] = city['city_ascii']
    info['lat'] = city['lat']
    info['lng'] = city['lng']
    info['country'] = city['country']
    info['population'] = city['population']
    info['admin_name'] = city['admin_name']
    lt.addLast(analyzer['lt cities'], info)
    addCitiestoCity(analyzer, info)


def addAirport(analyzer, airport):
    info = {}
    info['id'] = airport['id']
    info['Name'] = airport['Name']
    info['City'] = airport['City']
    info['Country'] = airport['Country']
    info['IATA'] = airport['IATA']
    info['Latitude'] = float(airport['Latitude'])
    info['Longitude'] = float(airport['Longitude'])
    lt.addLast(analyzer['lt airports'], info)
    om.put(analyzer['IATA_Airport'], info['IATA'], info)
    updateLatitudeIndex(analyzer['LatitudeIndex'], info)

def addCitiestoCity(analyzer, info):
    cities = analyzer['cities']
    city_ascii = info['city_ascii'].lower()
    existcity = mp.contains(cities, city_ascii)
    if existcity:
        entry = mp.get(cities, city_ascii)
        city = me.getValue(entry)
    else: 
        city = newCity(city_ascii)
        mp.put(cities, city_ascii, city)
    
    lt.addLast(city['valor'], info)

def newCity(city):
    entry = {'city': "", 'valor': None}
    entry['city'] = city
    entry['valor'] = lt.newList('ARRAY_LIST')
    return entry



# Funciones para agregar informacion a arboles 

def updateLatitudeIndex(mapa, airport):
    airlatitude = round(airport['Latitude'],2)
    entry = om.get(mapa, airlatitude)
    if entry is None:
        latitudentry = newLatitude(airlatitude)
        om.put(mapa, airlatitude, latitudentry)
    else:
        latitudentry = me.getValue(entry)

    latitudentry['size'] += 1
    updateLongitudeIndex(latitudentry['Longitude'], airport)


def updateLongitudeIndex(mapa, airport):
    airlongitude = round(airport['Longitude'], 2)
    entry = om.get(mapa, airlongitude)
    if entry is None:
        longitudentry = newLongitude(airlongitude)
        om.put(mapa, airlongitude, longitudentry)
    else:
        longitudentry = me.getValue(entry)
    
    lt.addLast(longitudentry['airports'], airport)
    longitudentry['size'] += 1
    


def newLatitude(latitud):
    entry = {'Latitude': None, 'Longitude':None, 'size':0}
    entry['Latitude'] = latitud
    entry['Longitude'] = om.newMap(omaptype='RBT',
                                  comparefunction=compareFloat)
    return entry

def newLongitude(longitud):
    entry = {'Longitude': None,'airports': None, 'size':0}
    entry['Longitude'] = longitud
    entry['airports'] = lt.newList('ARRAY_LIST')
    return entry



# Funciones para agregar informacion grafos

def addVertex(analyzer, airport):
    """
    Adiciona identificador IATA del aeropuerto como vertice del grafo
    """
    try: 
        if not gr.containsVertex(analyzer['connections'], airport['IATA']):
            gr.insertVertex(analyzer['connections'], airport['IATA'])

        if not gr.containsVertex(analyzer['reverse connections'], airport['IATA']):
            gr.insertVertex(analyzer['reverse connections'], airport['IATA'])

        if not gr.containsVertex(analyzer['doubleroute'], airport['IATA']):
            gr.insertVertex(analyzer['doubleroute'], airport['IATA'])


        return analyzer

    except Exception as exp:
        error.reraise(exp, 'Error in model:addAirport')

def AddConnections(analyzer, routes):
    """
    Adiciona un arco entre dos aeropuertos.
    """
    lt.addLast(analyzer['lt routes'], routes)

    edge = gr.getEdge(analyzer['connections'], routes['Departure'], routes['Destination'])
    if edge is None:
        gr.addEdge(analyzer['connections'], routes['Departure'], routes['Destination'], routes['distance_km'])

    arrive = gr.getEdge(analyzer['reverse connections'], routes['Destination'], routes['Departure'])
    if arrive is None:
        gr.addEdge(analyzer['reverse connections'], routes['Destination'], routes['Departure'], routes['distance_km'])

    edgeDestinationtoDeparture = gr.getEdge(analyzer['connections'], routes['Destination'], routes['Departure'])
    
    """
    Si el arco de destino a origen del grafo dirigido no esta vacio, se agregan los vertices de destino y origen al grafo no dirigido.
    Si el arco de destino a origen del grafo no dirigido esta vacio, se agrega el arco de destino a origen junto con el peso.
    """
    if edgeDestinationtoDeparture is not None:
        
        # Si arco que se busca obtener esta vacio, se agrega
        if gr.getEdge(analyzer['doubleroute'], routes['Destination'], routes['Departure']) is None:
            gr.addEdge(analyzer['doubleroute'], routes['Destination'], routes['Departure'], routes['distance_km'])

    return analyzer, edgeDestinationtoDeparture is not None

# Funciones de consulta

def Kosajaru(analyzer):
    """
    Se obtiene Kosajaru
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])

def SearchbyIATA(analyzer, IATA):
    """
    Buscar aeropuerto por IATA y saca el valor
    """        
    return me.getValue(om.get(analyzer['IATA_Airport'], IATA))

def totalAirperGraph(analyzer):
    """
    Retorna el total de aeropuertos (vertices) de los grafos
    """
    conections = gr.numVertices(analyzer['connections'])
    doubleroute = gr.numVertices(analyzer['doubleroute'])
    return conections, doubleroute

def totalConnectionsperGraph(analyzer):
    """
    Retorna el total arcos de los grafos
    """
    conections = gr.numEdges(analyzer['connections'])
    doubleroute = gr.numEdges(analyzer['doubleroute'])
    return conections, doubleroute

def CitySize(analyzer):
    """
    Retorna el tamaño del mapa de ciudades
    """
    llaves = mp.keySet(analyzer['cities'])
    size = lt.size(llaves)
    return size

def getFirst(lista, num):
    """
    Retorna los primeros num elementos de una lista
    """
    lista = lt.subList(lista, 1, num)
    return lista

def getLast(lista, num):
    """
    Retorna los ultimos num elementos de una lista
    """
    lista = lt.subList(lista, lt.size(lista)-(num-1), num)
    return lista

def FirtsAndLast(primeros, ultimos):
    for item in lt.iterator(ultimos):
        lt.addLast(primeros, item)
    return primeros

# Requerimientos
#! Req 1
def AirInterconection(analyzer):
    """
    Retorna la lista de aeropuertos que tienen interconexiones entre ellos en cada uno de los grafos y el total de conexiones
    """
    interconnections=lt.newList(datastructure="ARRAY_LIST")
    vertices= gr.vertices(analyzer['connections'])
    for vertex in lt.iterator(vertices):
        inbound = gr.indegree(analyzer['connections'],vertex)
        outbound = gr.outdegree(analyzer['connections'],vertex)
        num_connections = inbound + outbound
        if num_connections == 0:
            continue
        airport=om.get(analyzer['IATA_Airport'], vertex)['value']
        info={'Airport':vertex,
              'Interconnections': num_connections,
              'Name':airport['Name'],
              'City':airport['City'],
              'Country': airport['Country'],
              'Inbound': inbound,
              'Outbound': outbound}
        lt.addLast(interconnections,info)
    mer.sort(interconnections, cmpInterconnections)
    return interconnections
    
#! Req 2
def AirCluster(analyzer, vertexA, vertexB):
    """
    Retorna el total de clusters presentes en la red de aeropuertos y devuelve un valor booleano si los dos aeropuertos estan en el mismo cluster.
    """    
    total = scc.connectedComponents(analyzer['components'])
    samecluster =  scc.stronglyConnected(analyzer['components'], vertexA, vertexB)  
    return total, samecluster

#! Req 3
def SearchCity(analyzer, city):
    cities = mp.get(analyzer['cities'], city)
    value = None
    if cities:
        value = me.getValue(cities)['valor']
    return value


#! Req 4

#! Req 5
def OutOfService(analyzer, airIata):
    grafo = analyzer['connections']
    adjacents = gr.adjacents(grafo,airIata)
    reverse = analyzer['reverse connections']
    reverse_adj = gr.adjacents(reverse,airIata)
    airportsInfo = analyzer['IATA_Airport']
    affected = lt.newList('ARRAY_LIST')

    for iata in lt.iterator(adjacents):
        info = om.get(airportsInfo, iata)['value']
        lt.addLast(affected, info)

    for iata in lt.iterator(reverse_adj):
        if not lt.isPresent(adjacents, iata):
            info = om.get(airportsInfo, iata)['value']
            lt.addLast(affected, info)  
    return affected

#! Req 6

#! Req 7
def Mapa(info):
    df = pd.DataFrame(columns=['IATA', 'Name', 'City', 'Country', 'Latitude', 'Longitude'])
    for airport in lt.iterator(info):
        df.loc[len(df)] = [airport['IATA'], airport['Name'], airport['City'], airport['Country'], airport['Latitude'], airport['Longitude']]
        
    mapa = folium.Map(location=[45.5236, -122.6750])
    df.apply(lambda row:folium.Marker(location=[row["Latitude"], row["Longitude"]], 
            radius=10,Tooltip="Click me!", popup=folium.Popup(folium.Html(
            """
            <link href="style.css" rel="stylesheet" type="text/css">
            <table>
                <tr>
                    <th>Airport</th>
                    <th>Information</th>
                </tr>
                <tr>
                    <td>IATA</td>
                    <td>{IATA}</td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td>{Name}</td>
                </tr>
                <tr>
                    <td>City</td>
                    <td>{City}</td>
                </tr>
                <tr>
                    <td>Country</td>
                    <td>{Country}</td>
                </tr>
                <tr>
                    <td>Latitude</td>
                    <td>{Latitude}</td>
                </tr>
                <tr>
                    <td>Longitude</td>
                    <td>{Longitude}</td>
                </tr>
            </table>
            """
            .format(**row), script=True),  
            min_width=300, max_width=300), icon=folium.Icon(color='purple')).add_to(mapa), axis=1)

    mapa.save('mapa.html')
    webbrowser.open('mapa.html')

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

def compareCity(keyname , city):
    cityentry = me.getKey(city)
    if (keyname == cityentry):
        return 0
    elif (keyname > cityentry):
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

def compareString(str1, str2):
    """
    Compara dos strings
    """
    if (str1) == (str2):
        return 0
    elif (str1) > (str2):
        return 1
    else:
        return -1

def compareFloat(num1, num2):
    """
    Compara dos Floats
    """
    num1 = float(num1)
    num2 = float(num2)
    if (num1 == num2):
        return 0
    elif (num1 > num2):
        return 1
    else:
        return -1

def cmpInterconnections (a1,a2):
    return a1['Interconnections']>a2['Interconnections']

# Funciones auxiliares

def getDistance (departure, arrival):
    """
    distancia en kilometros entre 2 puntos 
    departure = (latitud, longitud)
    arrival = (latitud, longitud)


    Tomado de: https://pypi.org/project/haversine/
    """
    return haversine(departure, arrival)

def getNearestAirport(city, aumento):
    lat = city['lat']
    lng = city['lng']

    #Aumentar 10km aprox 

    expan_lat = aumento * 0.09 # entre lat 0 y lat 0.09 hay una distancia aprox de 10 km
    expan_lng = aumento * 0.09 # entre lng 0 y lng 0.09 hay una distancia aprox de 10 km

    