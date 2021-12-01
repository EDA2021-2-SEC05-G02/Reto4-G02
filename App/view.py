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
    print("Bienvenido")
    print("1- Cargar información de los aeropuertos")
    print("2- (Req 1) Encontrar puntos de interconexión aérea")
    print("3- (Req 2) Encontrar clústeres de tráfico aéreo")
    print("4- (Req 3) Encontrar la ruta más corta entre ciudades")
    print("5- (Req 4) Utilizar las millas de viajero")
    print("6- (Req 5) Cuantificar el efecto de un aeropuerto cerrado")
    print("7- (Bono) Comparar con servicio WEB externo")
    print("8- (Bono) Visualizar gráficamente los requerimientos")
    print("0- Salir")

def printLastCity(city):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ['City', 'population', 'lat', 'lng']
   x.add_row([city['city_ascii'], city['population'], city['lat'], city['lng']])
   print(x)

def printFirstAirport(airport):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ["IATA", "Name", "City", "Country", "Latitude", "Longitude"]
   x.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country'], airport['Latitude'], airport['Longitude']])
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
   x.field_names = ['IATA', '# Interconnections', 'Airport (Name)', 'City', 'Country']
   for air in lt.iterator(airport):
       x.add_row([air['Airport'], air['Interconnections'], air['Name'], air['City'], air['Country']])
   print(x)



def LoadData(cont):
    print("Cargando información de los aeropuertos ....")
    loadData = controller.loadData(cont)
    
    print('El primer aeropuerto cargado del grafo no dirgido es')
    printFirstAirport(loadData)

    data = controller.FirstAirportandLastCity()
    print('El primer aeropuerto cargado del grafo dirgido es')
    printFirstAirport(data[0])
    print('La ultima ciudad cargada es')
    printLastCity(data[1])
    numedges = controller.totalConnectionsperGraph(cont)
    numvertex = controller.totalAirperGraph(cont)
    CitySize = controller.CitySize(cont)
    print('Total de aeropuertos del grafo dirigido: ' + str(numvertex[0]))
    print('Total de aeropuertos del grafo no dirigido: ' + str(numvertex[1]))
    print('Numero de rutas aereas del grafo dirigido: ' + str(numedges[0]))
    print('Numero de rutas aereas del grafo no dirigido: ' + str(numedges[1]))
    print('El total de ciudades es: ' + str(CitySize))

def Req1(cont):
    airports=controller.AirInterconection(cont)
    print('El numero de aeropuertos interconectados es de: ',lt.size(airports))
    top5 = controller.getFirst(airports, 5)
    printAirInterconection(top5)

def Req2(cont):
    air1 = input('Ingrese el IATA del aeropuerto 1: ').upper()
    air2 = input('Ingrese el IATA del aeropuerto 2: ').upper()
    airport = controller.AirCluster(cont, air1, air2)
    if airport[1]:
        print('Los aeropuertos con identificador(IATA) ' + air1 + ' y ' + air2 + ' estan en el mismo cluster.')
    else:
        print('Los aeropuertos con identificador(IATA) ' + air1 + ' y ' + air2 + ' no estan en el mismo cluster.')

    print('El total de clusteres presentes en la red de transporte aereo son: ' + str(airport[0]))

def Req3(cont):
    ori_city = input('Ingrese la ciudad de origen: ')
    ori_cities = controller.SearchCity(cont, ori_city.lower())
    if lt.size(ori_cities) > 1:
        print("Se encontraron", lt.size(ori_cities), "ciudades con el mismo nombre")
        printCitiesSameName(ori_cities)
        num_oricity = input("Seleccione el numero de la ciudad que quiere consultar: ")

    dest_city = input('\nIngrese la ciudad de destino: ')
    dest_cities = controller.SearchCity(cont, dest_city.lower())
    if lt.size(dest_cities) > 1:
        print("Se encontraron", lt.size(dest_cities), "ciudades con el mismo nombre")
        printCitiesSameName(dest_cities)
        num_destcity = input("Seleccione el numero de la ciudad que quiere consultar: ")
 
def Req4(cont):
    pass

def Req5(cont):
    airIata = input('Ingrese el IATA del aeropuerto fuera de servicio: ')
    affected = controller.OutOfService(cont, airIata)
    print("="*15, " Req No. 5 Inputs ", "="*15)
    print("Check how many airports are affected if the airport with IATA" ,airIata,  "stops working\n")
    print("="*15, " Req No. 5 Answer ", "="*15)
    print("There are" ,lt.size(affected), "airports affected if the airport with IATA" ,airIata, "stops working\n")
    if lt.size(affected) != 0:
        print("The affected airports are:")
        printAirports(affected)

def Req6Bono(cont):
    pass

def Req7Bono(cont):
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

    
