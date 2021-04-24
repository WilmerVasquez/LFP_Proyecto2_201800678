import numpy as np

from objetos import *


class AutomataPila():
    def __init__(self, gramatica):
        self.gramatica = gramatica

    def analizarCadena(self, input):
        cadenaAceptada = False
        i = 0
        input_length = len(input)
        stack = []
        state = 'i'

        while i <= input_length:
            # i no avanza, significa que no leemos nada de la cadena de entrada
            if state == "i":
                stack_element_i = Simbolo(tipo="No Terminal", valor="#")
                stack.append(stack_element_i)
                state = 'p'
            elif state == 'p':
                stack_element_p = Simbolo(tipo="No Terminal", valor=self.gramatica.inicial)
                stack.append(stack_element_p)
                state = 'q'
            elif state == 'q':
                # for current_production in self.gramatica.producciones:
                should_restart = True
                while should_restart:
                    should_restart = False
                    for j in range(0, len(self.gramatica.producciones)):
                        current_production = self.gramatica.producciones[j]
                        stack_top = stack[len(stack)-1]
                        # print(" Tipo: " + stack_top.tipo + " Valor: " + stack_top.valor)
                        if stack_top.tipo == "No Terminal" and stack_top.valor == current_production.nombre:
                            if len(current_production.derivaciones) == 1:
                                stack.pop()
                                # pila en este momento (para el caso de S): [ # ]
                                derivacionesInvertidas = np.flip(current_production.derivaciones, 0)
                                for der in derivacionesInvertidas:
                                    stack.append(der[0])
                                should_restart = True
                                break
                                # pila quedaria(para el caso de S): [a A a  # ]
                            else:
                                currentChar = input[i]
                                derivacion = []
                                for derivacionActual in current_production.derivaciones:
                                    if derivacionActual[0].valor == currentChar:
                                        derivacion = np.flip(derivacionActual, 0)
                                # elif
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
                                stack.pop()
                                for der in derivacion:
                                    # simbolos del automata arreglar
                                    if der.valor != "$":
                                        stack.append(der)

                                # stack.pop()
                                # for der in derivacion:
                                #     # simbolos del automata arreglar
                                #     stack.append(der)
                                should_restart = True
                                break
                            # ejemplo de como quedaria la pila en este momento: [z N z  # ]
                        elif stack_top.tipo == "Terminal" and stack_top.valor == input[i]:
                            i += 1
                            stack.pop()
                            should_restart = True
                            break
                            # ejemplo de como quedaria la pila en este momento: [N z  # ]
                        # input = "zazabzbz"
                        elif stack_top.tipo == "Terminal" and stack_top.valor != input[i]:
                            print("Error, la cadena de entrada no se adapta al automata con pila")
                            state = "f"
                            should_restart = False
                            break
                            # Error, la cadena de entrada no se adapta al automata con pila

                        elif stack_top.tipo == "No Terminal" and stack_top.valor == "#":
                            stack.pop()
                            # pila nos queda: []
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
                        print("Tipo: "+elemento.tipo+" | Valor: "+elemento.valor)
                    return True
                    # aceptamos
                else:
                    print("longitud de la cadena: " + str(i))
                    print("longitud de la pila: " + str(len(stack)))
                    for elemento in stack:
                        print("Tipo: "+elemento.tipo+" | Valor: "+elemento.valor)
                    return False
                    # error, no se adapta

