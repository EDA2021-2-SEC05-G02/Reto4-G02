"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import threading
import time as tm
from DISClib.ADT import stack
import controller
from DISClib.ADT import list as lt
import prettytable 
from prettytable import PrettyTable
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información de los aeropuertos")
    print("2- (Req 1) Encontrar puntos de interconexión aérea")
    print("3- (Req 2) Encontrar clústeres de tráfico aéreo")
    print("4- (Req 3) Encontrar la ruta más corta entre ciudades")
    print("5- (Req 4) Utilizar las millas de viajero")
    print("6- (Req 5) Cuantificar el efecto de un aeropuerto cerrado")
    print("7- (Bono) Comparar con servicio WEB externo")
    print("8- (Bono) Visualizar gráficamente los requerimientos")
    print("0- Salir")

def printFirstLastCity(cities):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ['City', 'Country','Lat', 'Lng', 'population']
   city1 = lt.firstElement(cities)
   city2 = lt.lastElement(cities)
   x.add_row([city1['city_ascii'], city1['country'], city1['lat'], city1['lng'], city1['population']])
   x.add_row([city2['city_ascii'], city2['country'], city2['lat'], city2['lng'], city2['population']])
   print(x)

def printFirstLastAirport(airports):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ["IATA", "Name", "City", "Country", "Latitude", "Longitude"]
   air1 = lt.firstElement(airports)
   air2 = lt.lastElement(airports)
   x.add_row([air1['IATA'], air1['Name'], air1['City'], air1['Country'], air1['Latitude'], air1['Longitude']])
   x.add_row([air2['IATA'], air2['Name'], air2['City'], air2['Country'], air2['Latitude'], air2['Longitude']])
   print(x)

def printAirports(airports):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ["IATA", "Name", "City", "Country", "Latitude", "Longitude"]
   for airport in lt.iterator(airports):
        x.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country'], airport['Latitude'], airport['Longitude']])
   print(x)

def printCitiesSameName (cities):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ['#','City', 'Population', 'Latitude', 'Longitude', 'Country', 'Admin_name']
   i = 0
   for city in lt.iterator(cities):
       i+=1
       x.add_row([i, city['city_ascii'], city['population'], city['lat'], city['lng'], city['country'], city['admin_name']])
   print(x)

def printAirInterconection(airport):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ['IATA', 'Airport (Name)', 'City', 'Country', 'Connections', 'Inbound', 'Outbound',]
   for air in lt.iterator(airport):
       x.add_row([air['Airport'], air['Name'], air['City'], air['Country'], air['Interconnections'], air['Inbound'], air['Outbound']])
   print(x)

def LoadData(cont):
    print("Cargando información de los aeropuertos ....")
    controller.loadData(cont)
    vertex = controller.totalAirperGraph(cont)
    edges = controller.totalConnectionsperGraph(cont)
    city = lt.size(cont['lt cities'])

    print("\n=== Airport-Routes DiGraph ===")
    print("Nodes/Vertex:", vertex[0], "loaded airports.")
    print("Edges:", edges[0], "loaded routes.")
    print("First & last Airport loaded in the DiGraph:")
    printFirstLastAirport(cont['lt airports'])

    print("\n=== Airport-Routes Graph ===")
    print("Nodes/Vertex:", vertex[1], "loaded airports.")
    print("Edges:", edges[1], "loaded routes.")
    print("First & last Airport loaded in the Graph:")
    printFirstLastAirport(cont['lt airports'])

    print("\n=== City Network ===")
    print("The number of cities are:", city)
    print("First & last City loaded in data structure:")
    printFirstLastCity(cont['lt cities'])

#Requerimientos
def Req1(cont):
    airports=controller.AirInterconection(cont)
    top5 = controller.getFirst(airports, 5)
    print("="*15, "Req No. 1 Inputs", "="*15)
    print("Most connected airports in network (TOP 5) ")
    print("Number of airports in network:", lt.size(cont['lt airports']), "\n")

    print("="*15, "Req No. 1 Answer", "="*15)
    print('Connected airports inside network: ',lt.size(airports))
    print("TOP 5 most connected airports...")
    printAirInterconection(top5)

def Req2(cont):
    air1 = input('Ingrese el IATA del aeropuerto 1: ').upper()
    air2 = input('Ingrese el IATA del aeropuerto 2: ').upper()
    airport = controller.AirCluster(cont, air1, air2)

    print("="*15, "Req No. 2 Inputs", "="*15)
    print("Airport-1 IATA Code:", air1)
    print("Airport-2 IATA Code:", air2, "\n")

    print("="*15, "Req No. 2 Answer", "="*15)
    print("Number of SCC in Airport-Route network:", airport[0])
    print("Does Airport-1 & Airport-2 with IATA code", air1, "and", air2, "belong together?", airport[1])

def Req3(cont):
    depa_city = input('Ingrese la ciudad de origen: ')
    arriv_city = input('\nIngrese la ciudad de destino: ')

    arriv_cities = controller.SearchCity(cont, arriv_city.lower())
    depa_cities = controller.SearchCity(cont, depa_city.lower())
    departure = lt.firstElement(depa_cities)
    arrival = lt.firstElement(arriv_cities)

    if lt.size(depa_cities) > 1:
        print("Se encontraron", lt.size(depa_cities), "ciudades de origen con el mismo nombre")
        printCitiesSameName(depa_cities)
        num_depacity = input("Seleccione el numero de la ciudad que quiere consultar: ")
        departure = lt.getElement(depa_cities,num_depacity)

    if lt.size(arriv_cities) > 1:
        print("Se encontraron", lt.size(arriv_cities), "ciudades de destino con el mismo nombre")
        printCitiesSameName(arriv_cities)
        num_destcity = input("Seleccione el numero de la ciudad que quiere consultar: ")
        arrival = lt.getElement(arriv_cities,num_destcity)
        

    print("="*15, "Req No. 3 Inputs", "="*15)
    print("Depature city:", depa_city)
    print("Arrival city:", arriv_city, "\n")

    print("="*15, "Req No. 3 Answer", "="*15)
    print("+++ The departure airport in", depa_city, "is +++")
    #TODO Imprimir el aeropuerto mas cercano de la ciudad de origen
    print("\n+++ The arrival airport in", arriv_city, "is +++")
    #TODO Imprimir el aeropuerto mas cercano de la ciudad de destino

    print("\n+++ Dijkstra's Trip details +++")
    print(" - Total distance:" , "(km)") #TODO Calcular la distancia entre Aeropueto de origen y de destimo + distancia entre la ciudad y el Aeropueto de origen
    print(" - Trip Path:")
    #TODO Imprimir el camino
    print(" -Trip Stops:")
    #TODO Imprimir los aeropuertos en el que se hace escala + origen y destino

def Req4(cont): 
    city = ""
    airIata = ""
    millas = ""
    print("="*15, "Req No. 4 Inputs", "="*15)
    print("Departure IATA code:", airIata)
    print("Available Travel Miles:",millas, "\n")

    print("="*15, "Req No. 4 Answer", "="*15)
    print("+++ Departure Airport for IATA code:", airIata, "+++")
    #TODO imprimir info del aeropuerto
    print("\n- Number of possible airports:") #TODO
    print("- Max traveling distance between airports:", "(km).") #TODO
    print("- Passenger avalaible traveling miles:", "(km).") #TODO
    print("\n+++ Longest possible route with airport", airIata, "+++")
    print("- Longest possible path distance:", "(km).") #TODO
    print("- Longest possible path details:")
    #TODO imprimir info del camino
    print("-----")
    print("The passeenger needs", "miles to complete the trip.") #TODO
    print("-----")

def Req5(cont):
    airIata = input('Ingrese el IATA del aeropuerto fuera de servicio: ').upper()
    vertex = controller.totalAirperGraph(cont)
    edges = controller.totalConnectionsperGraph(cont)
    affected = controller.OutOfService(cont, airIata)

    print("="*15, " Req No. 5 Inputs ", "="*15)
    print("Closing the airport with IATA code:", airIata)
    print("\n--- Airport-Routes DiGraph ---")
    print("Original number of Airports:", vertex[0], "and Routes:", edges[0])
    print("--- Airport-Routes Graph ---")
    print("Original number of Airports:", vertex[1], "and Routes:", edges[1])

    print("\n+++ Removing Airport with IATA:", airIata, "+++")
    print("\n--- Airport-Routes DiGraph ---")
    print("Original number of Airports:", vertex[0]-1, "and Routes:", edges[0]) #TODO restar los los arcos del aeropuerto
    print("--- Airport-Routes Graph ---")
    print("Original number of Airports:", vertex[1], "and Routes:", edges[1], "\n") #TODO verificar si el aeropuerto esta en el grafo y si lo esta: restar los los arcos del aeropuerto 

    print("="*15, " Req No. 5 Answer ", "="*15)
    print("There are", lt.size(affected), "Airports affected by the removal of", airIata)
    if lt.size(affected) != 0:
        if lt.size(affected) > 6:
            print("The first & last 3 Airports affected are:")
            affected_air = controller.FirtsAndLast(controller.getFirst(affected, 3), controller.getLast(affected, 3))
            printAirports(affected_air)
        else:
            print("The affected Airports are:")
            printAirports(affected)
        
def Req6Bono(cont):
    pass

def Req7Bono(cont): #TODO a lo mejor juntarlo con los demas req para no volver a hacer todo el calculo
    airIata = input('Ingrese el IATA del aeropuerto fuera de servicio: ')
    affected = controller.OutOfService(cont, airIata)
    controller.Mapa(affected)

cont = None #catalog

"""
Menu principal
"""
def run():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            cont = controller.initAnalyzer()
            LoadData(cont)
            
        elif int(inputs[0]) == 2:
            Req1(cont)

        elif int(inputs[0]) == 3:
            Req2(cont)

        elif int(inputs[0]) == 4:
            Req3(cont)

        elif int(inputs[0]) == 5:
            Req4(cont)

        elif int(inputs[0]) == 6:
            Req5(cont)

        elif int(inputs[0]) == 7:
            Req6Bono(cont)
        
        elif int(inputs[0]) == 8:
            Req7Bono(cont)

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)
    sys.setrecursionlimit(2 ** 20)  
    thread = threading.Thread(target=run)
    thread.start()