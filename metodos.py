import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from graphviz import Digraph
from lector import *
from Automata import *

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
            gram = gramaticas[seleccion - 1]
            gram.imprimir()


def generarAutomataPila():
    global automata
    if len(gramaticas) == 0:
        print("No ha cargado ningun archivo o las gramaticas no fueron ingresadas")
    else:
        i = 1
        print("Seleccione la gramatica para generar el automata de pila")
        for gramatica in gramaticas:
            print(str(i) + ") Gramatica: " + gramatica.Nombre)
            i += 1

        seleccion = int(input())
        if 0 < seleccion <= len(gramaticas):
            automata = AutomataPila(gramaticas[seleccion - 1])
            generarAutomataGrafico(gramaticas[seleccion - 1])
        else:
            print("Error seleccione una gramatica")


def generarReporteGrafico():
    if automata is None:
        print("El automata no se ha creado aun")
    else:
        cadena = input("Ingrese la cadena a validar: ")
        if automata.analizarCadena(cadena):
            desplegarGraficasHTML(automata.imagenesGraphviz, automata.gramatica.Nombre, "Cadena Aceptada")
            print("Cadena Aceptada")
        else:
            desplegarGraficasHTML(automata.imagenesGraphviz, automata.gramatica.Nombre, "Cadena Rechazada")
            print("Cadena Rechazada")


def generarReporteTabla():
    if automata is None:
        print("El automata no se ha creado aun")
    else:
        cadena = input("Ingrese la cadena a validar: ")
        if automata.analizarCadena(cadena):
            desplegarTablaHTML(automata.reportesTabla, automata.gramatica.Nombre, "Cadena Aceptada")
            print("Cadena Aceptada")
        else:
            desplegarTablaHTML(automata.reportesTabla, automata.gramatica.Nombre, "Cadena Rechazada")
            print("Cadena Rechazada")


def generarAutomataGrafico(gramatica):
    try:
        f = Digraph('Automata de pila', filename='AP_' + gramatica.Nombre + '.gv', format='jpg')

        f.attr('node', shape='box')
        f.attr(rankdir='UD')
        inicio = """<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\n"""
        inicio += '<TR>\n'
        inicio += '<TD> Nombre: </TD>\n'
        inicio += '<TD> AP_' + gramatica.Nombre + '</TD>\n'
        inicio += '</TR>'
        pila = ','.join(gramatica.terminales+gramatica.no_Terminales+["#"])
        inicio += '<TR>\n'
        inicio += '<TD>Alfabeto de pila: </TD>\n'
        inicio += '<TD>{' + pila + '}</TD>\n'
        inicio += '</TR>'

        inicio += '<TR>\n'
        inicio += '<TD> Estados: </TD>\n'
        inicio += '<TD> {i,p,q,f}</TD>\n'
        inicio += '</TR>'

        inicio += '<TR>\n'
        inicio += '<TD> Estado inicial: </TD>\n'
        inicio += '<TD> {i}</TD>\n'
        inicio += '</TR>'

        inicio += '<TR>\n'
        inicio += '<TD> Estado de aceptacion: </TD>\n'
        inicio += '<TD> {f}</TD>\n'
        inicio += '</TR>'
        inicio += '</TABLE>>\n'

        f.node("datos", inicio)

        f.attr(rankdir='LR')
        f.attr('node', shape='circle')
        f.node('i')
        f.node('p')
        f.node('q')

        producNoTerminales = []
        producTerminales = []
        for produccion in gramatica.producciones:
            # entrada ; desapilar ; apilar1
            for derivacion in produccion.derivaciones:
                apilar = ""
                for simbolo in derivacion:
                    apilar = apilar + simbolo.valor

                texto = "λ," + produccion.nombre + ';' + apilar
                producNoTerminales.append(texto)

        for terminal in gramatica.terminales:
            texto = terminal + ',' + terminal + ';λ'
            producTerminales.append(texto)

        # prods1 = producNoTerminales+producTerminales
        prods1 = '\\n'.join(producNoTerminales)
        prods2 = '\\n'.join(producTerminales)
        f.edge('i', 'p', label='λ,λ;#')
        f.edge('p', 'q', label=('λ,λ;' + gramatica.inicial))
        f.edge('q:n', 'q:n', label=prods1)
        f.edge('q:s', 'q:s', label=prods2)
        f.attr('node', shape='doublecircle')
        f.node('f')
        f.edge('q', 'f', label='λ,#,λ')

        f.view()

    except Exception as e:
        print('Ha ocurido un error: ' + str(e))


def desplegarTablaHTML(reportes, nombre, resultado):
    try:
        f = open('reporteTabla.html', 'w')
        f.write("""<html>
            <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

                <nav class="navbar navbar-dark bg-dark">
                  <a class="navbar-brand">
                    <img src="usacIcono.png" width="100" height="100">
                  </a>
                  <a class="navbar-brand">
                  <h2><b> Wilmer Estuardo Vasquez Raxon - 2018000678 </b></h2>
                  </a>
                </nav>
                <style>
                table, th {
                  border: 1px solid black;
                  border-collapse: collapse;
                }
            </head>
            <body>""")
        f.write("<br><br>\n")
        f.write("""
            <div class="container" style="text-align: center;"><h4 > <b> AP_""" + nombre +
                """</b> </h4></div>
            <br>
            <div class="container" style="text-align: center;" > <ul class="list-group">""")
        f.write(""" <div class="container" style="text-align: left;"><h4><b> Tabla de transiciones </b></h4></div>\n""")
        f.write("""<div class="container" style="text-align: center;" > \n""")
        f.write("""<li class="list-group-item">""")
        f.write("<table style=\"width:100%\">\n")
        f.write("<tr>\n")
        f.write("<th><b> Iteracion </b></th>\n")
        f.write("<th><b> Pila  </b></th>\n")
        f.write("<th><b> Entrada </b></th>\n")
        f.write("<th><b> Trancision </b></th>\n")
        f.write("</tr>\n")
        for reporte in reportes:
            f.write("<tr>")
            f.write("<td> " + str(reporte.iteracion) + "</td>\n")
            f.write("<td> " + reporte.pila + "</td>\n")
            f.write("<td> " + reporte.entrada + "</td>\n")
            f.write("<td> " + reporte.transicion + "</td>\n")
            f.write("</tr>\n")
        f.write("</table>\n")
        f.write(""" <div class="container" style="text-align: left;"><h4><b>""" + resultado + """ </b></h4></div>\n""")
        f.write('\n</li> \n')
        f.write('\n</div> \n')

        f.write('\n</ul> </div> \n')
        fin = """</body>
                </html>"""
        f.write(fin)
        f.close()
        subprocess.Popen(['reporteTabla.html'], shell=True)

    except Exception as e:
        print("Algo ocurrio: " + str(e))


def desplegarGraficasHTML(imagenes, nombre, resultado):
    try:
        f = open('reporteGrafico.html', 'w')
        f.write("""<html>
            <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

                <nav class="navbar navbar-dark bg-dark">
                  <a class="navbar-brand">
                    <img src="usacIcono.png" width="100" height="100">
                  </a>
                  <a class="navbar-brand">
                  <h2><b> Wilmer Estuardo Vasquez Raxon - 2018000678 </b></h2>
                  </a>
                </nav>
            </head>
            <body>""")
        f.write("<br><br>\n")
        f.write("""
            <div class="container" style="text-align: center;"><h4 > <b> AP_""" + nombre +
                """</b> </h4></div>
            <br>
            <div class="container" style="text-align: center;" > <ul class="list-group">""")
        f.write(""" <div class="container" style="text-align: left;"><h4><b>Transiciones Realizadas</b></h4></div>\n""")
        f.write("""<div class="container" style="text-align: center;" > \n""")

        for imagen in imagenes:
            f.write("""<li class="list-group-item">""")
            f.write("<img src=\""+imagen+"\" width=\"750\" height=\"450\">")
            f.write('\n</li> \n')
        f.write(""" <div class="container" style="text-align: left;"><h4><b>""" + resultado + """ </b></h4></div>\n""")
        f.write('\n</li> \n')
        f.write('\n</div> \n')

        f.write('\n</ul> </div> \n')
        fin = """</body>
                </html>"""
        f.write(fin)
        f.close()
        subprocess.Popen(['reporteGrafico.html'], shell=True)

    except Exception as e:
        print("Algo ocurrio" + str(e))



