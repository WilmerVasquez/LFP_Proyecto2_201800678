

class Gramatica():
    def __init__(self, Nombre, no_Terminales, terminales, inicial):
        self.Nombre = Nombre
        self.no_Terminales = no_Terminales
        self.terminales = terminales
        self.inicial = inicial
        self.producciones = []

    def addProduccion(self, nombre, derivacion):
        if self.verificarProduccion(nombre):
            prod = self.obtenerProduccion(nombre)
            prod.addDerivacion(derivacion)
        else:
            new_produccion = Produccion(nombre=nombre)
            new_produccion.addDerivacion(derivacion)

    def verificarProduccion(self, nombre):
        var = False
        for produccion in self.producciones:
            if produccion.nombre == nombre:
                var = True
        return var

    def obtenerProduccion(self, nombre):
        for produccion in self.producciones:
            if produccion.nombre == nombre:
                return produccion

    def imprimir(self):
        print('Nombre de la gramatica tipo 2: ' + self.Nombre)
        print('No terminales = {' + ','.join(self.no_Terminales) + '}')
        print('Terminales = {' + ','.join(self.no_Terminales) + '}')
        print('No terminal inicial = ' + self.inicial)
        print('Producciones:')
        for produccion in self.producciones:
            produccion.imprimir()


class Produccion():
    def __init__(self, nombre=None):
        self.nombre = nombre
        self.derivaciones = []

    def addDerivacion(self, derivacion):
        self.derivaciones.append(derivacion)

    def imprimir(self):
        if len(self.derivaciones) > 1:
            print(self.nombre + '->'+self.derivaciones[0], end='')
            for i in range(1, len(self.derivaciones)):
                print('\t|'+self.derivaciones[i], end='')
            print('')


class Derivacion():
    def __init__(self, tipo=None, valor=None):
        self.tipo = tipo
        self.valor = valor

