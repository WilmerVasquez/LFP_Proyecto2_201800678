from objetos import *


def procesar_Gramatica(ruta):
    global vector_Gramaticas
    try:
        documento = open(ruta, 'r')
        gramaticas = documento.read().strip('\n').split('*')
        # Vector de Gramaticas
        vector_Gramaticas = []
        for gramatica in gramaticas:
            gramatica_Correcta = False
            if gramatica == '':
                continue
            else:
                gramatica = gramatica.split('\n')
                gramatica = '%'.join(gramatica)
                gramatica = gramatica.strip('%').split('%')
                Nombre = gramatica[0]
                caracteristicas = gramatica[1].strip(' ').replace(' ', '').split(';')
                # print(caracteristicas)
                no_Terminales = caracteristicas[0].split(',')
                terminales = caracteristicas[1].split(',')
                # print(terminales)
                inicial = caracteristicas[2]
                # Objeto Gramatica

                new_Gramatica = Gramatica(Nombre, no_Terminales, terminales, inicial)
                producciones = gramatica[2:]
                for prod in producciones:
                    # print(prod)
                    produccion = prod.split('->')
                    ladoIzquierdo = produccion[0].strip(' ').replace(' ', '')
                    derivacion = list(produccion[1].strip(' ').replace(' ', ''))
                    if len(ladoIzquierdo) == 1:
                        if ladoIzquierdo in terminales:
                            break
                    elif len(ladoIzquierdo) > 1:
                        break
                    if len(derivacion) > 2:
                        gramatica_Correcta = True
                    simbolosDerivacion = []
                    for simbolo in derivacion:
                        if simbolo in no_Terminales:
                            simbol = Simbolo(tipo="No Terminal", valor=simbolo)
                            simbolosDerivacion.append(simbol)
                        elif simbolo in terminales:
                            simbol = Simbolo(tipo="Terminal", valor=simbolo)
                            simbolosDerivacion.append(simbol)

                    new_Gramatica.addProduccion(ladoIzquierdo, simbolosDerivacion)

            if gramatica_Correcta:
                vector_Gramaticas.append(new_Gramatica)
            else:
                print('Gramatica: ' + Nombre + ' no es libre del contexto')
        print('Cargado con exito')
    except FileNotFoundError:
        print('No se encontro el archivo, revise la ruta')
    except Exception as e:
        print('Ha ocurrido un error: ' + str(e))
    finally:
        return vector_Gramaticas


def obtenerPosGramatica():
    print("nel")
