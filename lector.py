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
                no_Terminales = caracteristicas[0]
                terminales = caracteristicas[1]
                inicial = caracteristicas[2]
                # Objeto Gramatica
                new_Gramatica = Gramatica(Nombre, no_Terminales, terminales, inicial)
                for j in range(2, len(gramatica)):
                    produccion = gramatica[j].split('->')
                    derivacion = produccion[1].split(' ')
                    if len(derivacion) > 2:
                        gramatica_Correcta = True
                    simbolosDerivacion = []
                    for simbolo in derivacion:
                        if simbolo in no_Terminales:
                            simbolo = Derivacion(tipo="No Terminal", valor=simbolo)
                            simbolosDerivacion.append(simbolo)
                        elif simbolo in terminales:
                            simbolo = Derivacion(tipo="Terminal", valor=simbolo)
                            simbolosDerivacion.append(simbolo)

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
