from DbConnection import DbConnection
from py2neo import Node, Graph, Relationship

class Locomotora():

    def __init__(self, nombre, tipo):
            self.nombre = nombre
            self.tipo = tipo

    @staticmethod
    def createLocomotora(nombreL, tipoL):
        db_connection = DbConnection()
        if tipoL == 'altaVelocidad' or tipoL == 'catenaria' or tipoL == 'noCatenaria':
            locomotora = Node('Locomotora', nombre = nombreL, tipo = tipoL)
            nodo = Locomotora.getLocomotoraFromNombre(nombreL)
            if nodo is None:
                m = db_connection.graph.create(locomotora)

    @staticmethod
    def createLocomotoras():
        Locomotora.createLocomotora('TrenToWapo', 'altaVelocidad')
        Locomotora.createLocomotora('TrenNoTanWapo', 'catenaria')
        Locomotora.createLocomotora('TrenCutre', 'noCatenaria')

        Locomotora.createLocomotora('Ave', 'altaVelocidad')
        Locomotora.createLocomotora('Renfe', 'catenaria')
        Locomotora.createLocomotora('TractorGrande', 'noCatenaria')

    @staticmethod
    def getLocomotoraFromNombre(nombre):
        db_connection = DbConnection()
        n = db_connection.graph.find_one('Locomotora', 'nombre', nombre)
        return n

    @staticmethod
    def asociarLocomotoraAEstacion(locomotora, estacion):
        db_connection = DbConnection()
        db_connection.graph.create_unique(Relationship(locomotora, 'locomotoraEstaciona', estacion))

    @staticmethod
    def asociarLocomotoras(madrid):
        db_connection = DbConnection()

        locomotora1 = Locomotora.getLocomotoraFromNombre('TrenToWapo')
        locomotora2 = Locomotora.getLocomotoraFromNombre('TrenNoTanWapo')
        locomotora3 = Locomotora.getLocomotoraFromNombre('TrenCutre')
        locomotora4 = Locomotora.getLocomotoraFromNombre('Ave')
        locomotora5 = Locomotora.getLocomotoraFromNombre('Renfe')
        locomotora6 = Locomotora.getLocomotoraFromNombre('TractorGrande')


        Locomotora.asociarLocomotoraAEstacion(locomotora1, madrid)
        Locomotora.asociarLocomotoraAEstacion(locomotora2, madrid)
        Locomotora.asociarLocomotoraAEstacion(locomotora3, madrid)
        Locomotora.asociarLocomotoraAEstacion(locomotora4, madrid)
        Locomotora.asociarLocomotoraAEstacion(locomotora5, madrid)
        Locomotora.asociarLocomotoraAEstacion(locomotora6, madrid)

