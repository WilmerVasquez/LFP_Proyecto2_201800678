from tkinter import Tk
from tkinter.filedialog import askopenfilename
from lector import *


gramaticas = []


def cargarArchivo():
    root = Tk()
    NombreArchivo = askopenfilename()
    root.withdraw()
    global gramaticas
    gramaticas = procesar_Gramatica(NombreArchivo)


def mostrarInfoGramatica():
    if len(gramaticas) == 0:
        print("No ha cargado ningun archivo o las gramaticas no fueron ingresadas")
    else:
        i = 1
        print("Seleccione la gramatica a mostrar")
        for gramatica in gramaticas:
            print(str(i) + ") Gramatica: " + gramatica.Nombre)
            i += 1

        seleccion = int(input("ingrese el numero: "))
        if 0 < seleccion <= len(gramaticas):
            gram = gramaticas[seleccion-1]
            gram.imprimir()



