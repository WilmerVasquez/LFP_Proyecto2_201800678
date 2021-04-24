

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
            self.producciones.append(new_produccion)

    def verificarProduccion(self, nombre):
        for produccion in self.producciones:
            if produccion.nombre == nombre:
                return True
        return False

    def verificarNoTerminalProduce(self, noT, term):
        for produccion in self.producciones:
            if produccion.nombre == noT:
                return produccion.verificarTerminal(term)
        return False

    def obtenerProduccion(self, nombre):
        for produccion in self.producciones:
            if produccion.nombre == nombre:
                return produccion
        return None

    def imprimir(self):
        print('Nombre de la gramatica tipo 2: ' + self.Nombre)
        print('No terminales = {' + ','.join(self.no_Terminales) + '}')
        print('Terminales = {' + ','.join(self.terminales) + '}')
        print('No terminal inicial = ' + self.inicial)
        print('Producciones:')
        for produccion in self.producciones:
            produccion.imprimir()

    def obtenerProduccionPorTerminal(self, terminal):
        for produccion in self.producciones:
            if produccion.verificarTerminal(terminal):
                return produccion
        return None


class Produccion():
    def __init__(self, nombre=None):
        self.nombre = nombre
        self.derivaciones = []

    def verificarTerminal(self, terminal):
        for derivacion in self.derivaciones:
            for simbolo in derivacion:
                if simbolo.valor == terminal:
                    return True
        return False

    def obtenerDerivacion(self, terminal):
        for derivacion in self.derivaciones:
            for simbolo in derivacion:
                if simbolo.valor == terminal:
                    return derivacion
        return None

    def obtenerNoTerminales(self):
        noTerminales = []
        for derivacion in self.derivaciones:
            for simbolo in derivacion:
                if simbolo.tipo == "No Terminal":
                    noTerminales.append(simbolo.valor)
        return noTerminales

    def addDerivacion(self, derivacion):
        self.derivaciones.append(derivacion)

    def imprimir(self):
        if len(self.derivaciones) > 1:
            # valores = self.obtenerValores(0)
            print(str(self.nombre) + '->\t' + ' '.join(self.obtenerValores(0)), end='\n')
            for i in range(1, len(self.derivaciones)):
                print('\t|' + ' '.join(self.obtenerValores(i)), end='\n')
            print('')
        elif len(self.derivaciones) == 1:
            print(str(self.nombre) + '->\t' + ' '.join(self.obtenerValores(0)), end='\n')

    def obtenerValores(self, indice):
        valores = []
        simbolos = self.derivaciones[indice]
        for simbolo in simbolos:
            valores.append(simbolo.valor)
        return valores


class Simbolo():
    def __init__(self, tipo=None, valor=None):
        self.tipo = tipo
        self.valor = valor


