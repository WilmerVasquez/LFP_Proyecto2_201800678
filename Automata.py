from objetos import *

class AutomataPila():
    def __init__(self, gramatica):
        self.gramatica = gramatica

    def analizarCadena(self, input):

        i = 0
        input_length = len(input)
        stack = []
        state = 'i'

        while i < input_length:
            # i no avanza, significa que no leemos nada de la cadena de entrada
            if state == "i":
                stack_element_i = Simbolo("No Terminal", "#")
                stack.append(stack_element_i)
                state = 'p'
            elif state == 'p':
                stack_element_p = Simbolo("No Terminal", 'S')
                stack.append(stack_element_p)
                state = 'q'
            elif state == 'q':
                for j in range(self.gramatica.producciones.length):
                    current_production = self.gramatica.producciones[j]
                    stack_top = stack[0]
                    if stack_top.tipo == "No Terminal" and stack_top.valor == current_production.name:
                        if len(current_production.derivaciones) == 1:
                            stack.pop()
                            # pila en este momento (para el caso de S): [ # ]
                        for k in range(len(current_production.derivaciones), 0):
                            simbol = current_production.derivaciones[k]
                            stack.append(simbol)

                            # pila quedaria(para el caso de S): [z M N z  # ]
                        else:
                            derivacion = None
                            currentChar = input.charAt(i)
                            for k in range(len(current_production.derivaciones)):
                                derivacionActual = current_production.derivaciones[k]
                                if derivacionActual[0].valor == currentChar:
                                    derivacion = derivacionActual
                            stack.pop()
                            for k in range(len(derivacion), 0):
                                # simbolos del automata arreglar
                                aux = derivacion[k]
                                stack.append(aux)

                            # ejemplo de como quedaria la pila en este momento: [z N z  # ]

                    elif stack_top.tipo == "Terminal" and stack_top.valor == input.charAt(i):
                        i += 1
                        stack.pop()
                        # ejemplo de como quedaria la pila en este momento: [N z  # ]

                    elif stack_top.tipo == "Terminal" and stack_top.valor != input.charAt(i):
                        print("Error, la cadena de entrada no se adapta al automata con pila")
                        # Error, la cadena de entrada no se adapta al automata con pila

                    elif stack_top.tipo == "No Terminal" and stack_top.valor == "#":
                        stack.pop()
                    # pila nos queda: []
                        state = "f"

                    elif state == "f":
                        if i == input_length:
                            print("Cadena Aceptada")
                            # aceptamos
                        else:
                            print("Cadena Rechazada")
                            # error, no se adapta

