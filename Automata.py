import numpy as np
from objetos import *
from metodos import *


def generarString(vector):
    string = ""
    for simbolo in vector:
        string = string + simbolo.valor
    return string


def generarAutomataGraficoDinamico(gramatica, estado, trancision, noTransicion, pila, entrada):
    try:
        nombre = str(noTransicion) + '_AP_' + gramatica.Nombre
        # nombre = str(noTransicion) + '_AP_' + gramatica.Nombre + '.gv' + '.jpg'
        f = Digraph('Automata de pila', filename=nombre + '.gv', format='jpg')

        f.attr('node', shape='box')
        f.attr(rankdir='UD')
        inicio = """<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\n"""
        inicio += '<TR>\n'
        inicio += '<TD> Iteracion: </TD>\n'
        inicio += '<TD>' + str(noTransicion) + '</TD>\n'
        inicio += '</TR>'

        inicio += '<TR>\n'
        inicio += '<TD> Pila: </TD>\n'
        inicio += '<TD>' + pila + '</TD>\n'
        inicio += '</TR>'

        inicio += '<TR>\n'
        inicio += '<TD> Entrada: </TD>\n'
        inicio += '<TD> ' + entrada + '</TD>\n'
        inicio += '</TR>'
        inicio += '</TABLE>>\n'

        f.node("datos", inicio)

        f.attr(rankdir='LR')

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

        f.attr('node', shape='circle')
        if estado == "i":
            f.node('i', fillcolor="gold")
            f.attr(rankdir='UD')
            f.node('Transicion: ' + trancision, fillcolor="red")
            # f.edge('q', 't')
            # f.edge('i', 'Transicion: ' + trancision)
        elif estado == "p":
            f.node('p', fillcolor="gold")
            f.attr(rankdir='UD')
            f.node('Transicion: ' + trancision, fillcolor="red")
            # f.edge('q', 't')
            # f.edge('p', 'Transicion: ' + trancision)
        elif estado == "q":
            f.node('q', fillcolor="gold")
            f.attr(rankdir='UD')
            f.node('t', 'Transicion: ' + trancision, fillcolor="red")
            # f.edge('q', 't')
            # f.edge('q', 'Transicion: ' + trancision)
        elif estado == "f":
            f.attr('node', shape='doublecircle')
            f.node('f', fillcolor="gold")
            if len(pila) == 0:
                f.attr(rankdir='UD')
                f.attr('node', shape='box')
                f.node('resultado', 'Cadena Aceptada', fillcolor="red")
            else:
                f.attr(rankdir='UD')
                f.attr('node', shape='box')
                f.node('resultado', 'Cadena Rechazada', fillcolor="red")

        f.attr('node', shape='circle')
        f.attr(rankdir='LR')
        f.edge('i', 'p', label='λ,λ;#')
        f.edge('p', 'q', label=('λ,λ;' + gramatica.inicial))

        f.edge('q:n', 'q:n', label=prods1)
        f.edge('q:s', 'q:s', label=prods2)
        f.edge('q', 'f', label='λ,#,λ')
        f.render()
        return nombre + '.gv' + '.jpg'
    except Exception as e:
        print('Ha ocurido un error: ' + str(e))


class AutomataPila():
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.reportesTabla = []
        self.imagenesGraphviz = []

    def analizarCadena(self, input):
        i = 0
        input_length = len(input)
        stack = []
        state = 'i'
        no_Transicion = 0
        reportes = []
        imagenes = []
        while i <= input_length:
            # i no avanza, significa que no leemos nada de la cadena de entrada
            if state == "i":
                stack_element_i = Simbolo(tipo="No Terminal", valor="#")
                stack.append(stack_element_i)
                imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                               state,
                                                               "λ,λ;#",
                                                               no_Transicion,
                                                               generarString(stack),
                                                               input[i]))

                reportes.append(Reporte(no_Transicion, "", input[i], "i,$,$;p,#"))
                no_Transicion += 1
                state = 'p'
            elif state == 'p':
                stack_element_p = Simbolo(tipo="No Terminal", valor=self.gramatica.inicial)
                stack.append(stack_element_p)
                imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                               state,
                                                               "λ,λ;#",
                                                               no_Transicion,
                                                               generarString(stack),
                                                               input[i]))
                reportes.append(Reporte(no_Transicion, "#", input[i], "p,$,$;q,S"))
                no_Transicion += 1
                state = 'q'
            elif state == 'q':
                # for current_production in self.gramatica.producciones:
                should_restart = True
                while should_restart:
                    should_restart = False
                    for j in range(0, len(self.gramatica.producciones)):
                        current_production = self.gramatica.producciones[j]
                        stack_top = stack[len(stack) - 1]
                        # print(" Tipo: " + stack_top.tipo + " Valor: " + stack_top.valor)
                        if stack_top.tipo == "No Terminal" and stack_top.valor == current_production.nombre:
                            if len(current_production.derivaciones) == 1:

                                # pila en este momento (para el caso de S): [ # ]
                                derivaciones = current_production.derivaciones[0]
                                derivacionesInvertidas = np.flip(derivaciones)

                                imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                                               state,
                                                                               "λ," + stack_top.valor + ";q," +
                                                                               generarString(derivaciones),
                                                                               no_Transicion,
                                                                               generarString(stack),
                                                                               input[i]))
                                reportes.append(Reporte(no_Transicion,
                                                        generarString(stack),
                                                        input[i],
                                                        "q,$," + stack_top.valor + ";q," + generarString(derivaciones)))
                                no_Transicion += 1

                                stack.pop()
                                for der in derivacionesInvertidas:
                                    stack.append(der)
                                should_restart = True
                                break
                            else:
                                currentChar = input[i]
                                derivacion = []
                                for derivacionActual in current_production.derivaciones:
                                    if derivacionActual[0].valor == currentChar:
                                        derivacion = np.flip(derivacionActual, 0)

                                if len(derivacion) == 0:
                                    noTerminales = current_production.obtenerNoTerminales()

                                    if current_production.verificarTerminal(currentChar):
                                        derivacion = np.flip(current_production.obtenerDerivacion(currentChar), 0)
                                    else:
                                        for noterm in noTerminales:
                                            if self.gramatica.verificarNoTerminalProduce(noterm, currentChar):
                                                prod = self.gramatica.obtenerProduccion(noterm)
                                                derivacion = np.flip(prod.obtenerDerivacion(currentChar), 0)
                                                break
                                            elif self.gramatica.verificarNoTerminalProduce(noterm, "$"):
                                                prod = self.gramatica.obtenerProduccion(noterm)
                                                derivacion = np.flip(prod.obtenerDerivacion("$"), 0)
                                                break

                                derivaciones = np.flip(derivacion)
                                imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                                               state,
                                                                               "λ," + stack_top.valor + ";q," + generarString(
                                                                                   derivaciones),
                                                                               no_Transicion, generarString(stack),
                                                                               input[i]))
                                reportes.append(Reporte(no_Transicion,
                                                        generarString(stack),
                                                        input[i],
                                                        "q,$," + stack_top.valor + ";q," + generarString(derivaciones)))
                                no_Transicion += 1

                                stack.pop()
                                for der in derivacion:
                                    # simbolos del automata arreglar
                                    if der.valor != "$":
                                        stack.append(der)

                                should_restart = True
                                break
                            # ejemplo de como quedaria la pila en este momento: [z N z  # ]
                        elif stack_top.tipo == "Terminal" and stack_top.valor == input[i]:
                            imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                                           state,
                                                                           "λ," + stack_top.valor + ";q," + input[i],
                                                                           no_Transicion, generarString(stack),
                                                                           input[i]))
                            reportes.append(Reporte(no_Transicion,
                                                    generarString(stack),
                                                    input[i],
                                                    "q,$," + stack_top.valor + ";q," + input[i]))
                            no_Transicion += 1
                            i += 1
                            stack.pop()
                            should_restart = True
                            break
                            # ejemplo de como quedaria la pila en este momento: [N z  # ]
                        # input = "zazabzbz"
                        elif stack_top.tipo == "Terminal" and stack_top.valor != input[i]:
                            print("Error, la cadena de entrada no se adapta al automata con pila")
                            state = "f"
                            imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                                           state,
                                                                           "Error, la entrada no se adapta al "
                                                                           "automata con pila",
                                                                           no_Transicion, generarString(stack),
                                                                           input[i]))
                            reportes.append(Reporte(no_Transicion,
                                                    generarString(stack),
                                                    input[i],
                                                    "Error, la entrada no se adapta al automata con pila"))
                            no_Transicion += 1

                            should_restart = False
                            break
                            # Error, la cadena de entrada no se adapta al automata con pila

                        elif stack_top.tipo == "No Terminal" and stack_top.valor == "#":
                            imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                                           state,
                                                                           "λ," + stack_top.valor + ";q," + input[-1],
                                                                           no_Transicion, generarString(stack),
                                                                           input[-1]))
                            reportes.append(Reporte(no_Transicion,
                                                    generarString(stack),
                                                    "$",
                                                    "q,$,#;f,"))
                            no_Transicion += 1
                            stack.pop()
                            state = "f"
                            should_restart = False
                            break
                        else:
                            should_restart = True

            elif state == "f":
                if i == input_length and len(stack) == 0:
                    print("longitud de la cadena: " + str(i))
                    print("longitud de la pila: " + str(len(stack)))
                    for elemento in stack:
                        print("Tipo: " + elemento.tipo + " | Valor: " + elemento.valor)

                    imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                                   state,
                                                                   "λ,#;λ",
                                                                   no_Transicion,
                                                                   generarString(stack),
                                                                   ""))
                    reportes.append(Reporte(no_Transicion,
                                            "",
                                            "",
                                            "f"))
                    self.reportesTabla = reportes
                    self.imagenesGraphviz = imagenes
                    return True
                else:
                    print("longitud de la cadena: " + str(i))
                    print("longitud de la pila: " + str(len(stack)))
                    for elemento in stack:
                        print("Tipo: " + elemento.tipo + " | Valor: " + elemento.valor)
                    imagenes.append(generarAutomataGraficoDinamico(self.gramatica,
                                                                   state,
                                                                   "λ,#;λ",
                                                                   no_Transicion,
                                                                   generarString(stack),
                                                                   input[i]))
                    reportes.append(Reporte(no_Transicion,
                                            generarString(stack),
                                            input[i],
                                            "f,$,$;q,$" + input[i]))
                    self.reportesTabla = reportes
                    self.imagenesGraphviz = imagenes
                    return False
