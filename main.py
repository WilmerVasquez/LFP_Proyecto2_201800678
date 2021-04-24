import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from metodos import *
from Automata import *

if __name__ == '__main__':
    segundos = 5
    print('----------Proyecto 2---------')
    print('Wilmer Estuardo Vasquez Raxon')
    print('201800678')
    # while segundos != 0:
    #     print(segundos)
    #     time.sleep(1)
    #     segundos = segundos - 1
    opcion = 0
    print('¡Bienvenido!')
    while opcion != 6:
        print('---------------Menu---------------')
        print('1. Cargar archivo')
        print('2. Mostrar informacion general de la gramatica')
        print('3. Generar automata de pila eqivalente')
        print('4. Reporte de recorrido')
        print('5. Reporte en tabla')
        print('6. Salir')
        opcion = int(input())
        if opcion == 1:
            cargarArchivo()
        elif opcion == 2:
            mostrarInfoGramatica()
        elif opcion == 3:
            generarAutomataPila()
        elif opcion == 4:
            generarReporteGrafico()

