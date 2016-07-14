from DbConnection import DbConnection
from py2neo import Node, Graph, Relationship
from Locomotora import Locomotora

class Envio():

    #el tren asociado se guardara en forma de relacion
    def __init__(self, nombre, cliente, tipo, fecha, volumen, peso, tiempo, coste, mes):
        self.nombre = nombre
        self.cliente = cliente
        self.tipo = tipo
        self.fecha = fecha
        self.volumen = volumen
        self.peso = peso
        self.tiempo = tiempo
        self.coste = coste
        self.mes = mes

    @staticmethod
    def createEnvio(nombre, cliente, tipo, fecha, volumen, peso, tiempo, coste, mes):
        db_connection = DbConnection()

        envio = Node('Envio', nombre = nombre, cliente = cliente,
                     tipo = tipo, fecha = fecha, volumen = volumen,
                     peso = peso, tiempo = tiempo, coste = coste, mes = mes)
        nodo = Envio.getEnvioFromNombre(nombre)
        if nodo is None:
            m = db_connection.graph.create(envio)

    @staticmethod
    def getEnvioFromNombre(nombre):
        db_connection = DbConnection()
        n = db_connection.graph.find_one('Envio', 'nombre', nombre)
        return n

    @staticmethod
    def createEnvios():
        Envio.createEnvio('envio1', 'opsitseva', 'economico', '01/01/2016', 10, 10, 100, 100, 'Enero')
        Envio.createEnvio('envio2', 'rosalastwords', 'intradia', '01/01/2016', 20, 20, 150, 150, 'Enero')
        Envio.createEnvio('envio3', 'anamasxw', 'primeraHora', '01/01/2016', 30, 30, 200, 200, 'Enero')
        Envio.createEnvio('envio4', 'carlotasquella', 'normal', '01/01/2016', 40, 40, 250, 250, 'Enero')
        Envio.createEnvio('envio5', 'goicoechea22', 'economico', '01/02/2016', 50, 50, 300, 300, 'Febrero')

        Envio.createEnvio('envio6', 'opsitseva', 'intradia', '01/01/2016', 10, 10, 100, 100, 'Enero')

    @staticmethod
    def asociarEnvioLocomotora(envio, locomotora):
        db_connection = DbConnection()
        db_connection.graph.create_unique(Relationship(envio, 'almacenado', locomotora))

    @staticmethod
    def asociarEnvios():
        envio1 = Envio.getEnvioFromNombre('envio1')
        envio2 = Envio.getEnvioFromNombre('envio2')
        envio3 = Envio.getEnvioFromNombre('envio3')
        envio4 = Envio.getEnvioFromNombre('envio4')
        envio5 = Envio.getEnvioFromNombre('envio5')

        locomotora = Locomotora.getLocomotoraFromNombre('TrenToWapo')

        Envio.asociarEnvioLocomotora(envio1, locomotora)
        Envio.asociarEnvioLocomotora(envio2, locomotora)
        Envio.asociarEnvioLocomotora(envio3, locomotora)
        Envio.asociarEnvioLocomotora(envio4, locomotora)
        Envio.asociarEnvioLocomotora(envio5, locomotora)