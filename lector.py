from objetos import *


def procesar_Gramatica(ruta):
    try:
        documento = open(ruta, 'r')
        gramaticas = documento.read().split('*')
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
                caracteristicas = gramatica[1].split(';')
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
                    derivacion = produccion[1].split(' ')
                    if len(derivacion) > 2:
                        gramatica_Correcta = True
                    simbolosDerivacion = []
                    for simbolo in derivacion:
                        if simbolo in no_Terminales:
                            simbol = Derivacion(tipo="No Terminal", valor=simbolo)
                            simbolosDerivacion.append(simbol)
                        elif simbolo in terminales:
                            simbol = Derivacion(tipo="Terminal", valor=simbolo)
                            simbolosDerivacion.append(simbol)

                    new_Gramatica.addProduccion(produccion[0], simbolosDerivacion)

            if gramatica_Correcta:
                vector_Gramaticas.append(new_Gramatica)
            else:
                print('Gramatica: ' + Nombre + ' no es libre del contexto')
        print('Cargado con exito')
        return vector_Gramaticas
    except FileNotFoundError:
        print('No se encontro el archivo, revise la ruta')
    except Exception as e:
        print('Ha ocurrido un error' + str(e))


def obtenerPosGramatica():
    print("nel")
