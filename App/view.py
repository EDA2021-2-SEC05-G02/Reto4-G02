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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de los aeropuertos")
    print("3- (Req 1) Encontrar puntos de interconexión aérea")
    print("4- (Req 2) Encontrar clústeres de tráfico aéreo")
    print("5- (Req 3) Encontrar la ruta más corta entre ciudades")
    print("6- (Req 4) Utilizar las millas de viajero")
    print("7- (Req 5) Cuantificar el efecto de un aeropuerto cerrado")
    print("8- (Bono) Comparar con servicio WEB externo")
    print("9- Salir")

catalog = None

def LoadData(cont):
    print("Cargando información de los aeropuertos ....")
    controller.loadData(cont)
    numedges = controller.totalConnectionsperGraph(cont)
    numvertex = controller.totalAirperGraph(cont)
    CitySize = controller.CitySize(cont)
    print('Total de aeropuertos del grafo dirigido: ' + str(numvertex[0]))
    print('Total de aeropuertos del grafo no dirigido: ' + str(numvertex[1]))
    print('Numero de rutas aereas del grafo dirigido: ' + str(numedges[0]))
    print('Numero de rutas aereas del grafo no dirigido: ' + str(numedges[1]))
    print('El total de ciudades es: ' + str(CitySize))



def Requerimiento1(cont):
    print('El número de aeropuertos interconectados es: ' +
          str(controller.connectedComponents(cont)))


"""
Menu principal
"""
def run():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            cont = controller.initAnalyzer()

        elif int(inputs[0]) == 2:
            LoadData(cont)
    
        elif int(inputs[0]) == 3:
            Requerimiento1(cont)

        elif int(inputs[0]) == 4:
            pass

        elif int(inputs[0]) == 5:
            pass

        elif int(inputs[0]) == 6:
            pass

        elif int(inputs[0]) == 7:
            pass

        elif int(inputs[0]) == 8:
            pass

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)
    sys.setrecursionlimit(2 ** 20)  
    thread = threading.Thread(target=run)
    thread.start()

    
