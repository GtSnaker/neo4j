from DbConnection import DbConnection
from py2neo import Node, Graph, Relationship
from Locomotora import Locomotora
from Envio import Envio

class Estacion():

    def __init__(self, nombre):
        self.nombre = nombre

    @staticmethod
    def createEstacion(nombre):
        db_connection = DbConnection()
        m = db_connection.graph.merge_one('Estacion', 'nombre', nombre)

    @staticmethod
    def crearEstaciones():
        Estacion.createEstacion('Galicia')
        Estacion.createEstacion('Asturias')
        Estacion.createEstacion('Cantabria')
        Estacion.createEstacion('Euskadi')
        Estacion.createEstacion('Navarra')
        Estacion.createEstacion('Aragon')
        Estacion.createEstacion('Catalunya')
        Estacion.createEstacion('Valencia')
        Estacion.createEstacion('Murcia')
        Estacion.createEstacion('LaMancha')
        Estacion.createEstacion('Andalucia')
        Estacion.createEstacion('Extremadura')
        Estacion.createEstacion('Leon')
        Estacion.createEstacion('Madrid')
        Estacion.createEstacion('Canarias')
        Estacion.createEstacion('Baleares')

    @staticmethod
    def crearTramo(alice, bob, tipo, attrs = None):
        db_connection = DbConnection()
        if attrs is not None:
            db_connection.graph.create_unique(Relationship.cast(alice, tipo, bob, attrs))
        else:
            db_connection.graph.create_unique(Relationship(alice, tipo, bob))

    @staticmethod
    def getEstacionFromNombre(nombre):
        db_connection = DbConnection()
        return db_connection.graph.find_one('Estacion', 'nombre', nombre)

    @staticmethod
    def crearTramos():
        db_connection = DbConnection()
        galicia = Estacion.getEstacionFromNombre('Galicia')
        asturias = Estacion.getEstacionFromNombre('Asturias')
        cantabria = Estacion.getEstacionFromNombre('Cantabria')
        euskadi = Estacion.getEstacionFromNombre('Euskadi')
        navarra = Estacion.getEstacionFromNombre('Navarra')
        aragon = Estacion.getEstacionFromNombre('Aragon')
        catalunya = Estacion.getEstacionFromNombre('Catalunya')
        valencia = Estacion.getEstacionFromNombre('Valencia')
        murcia = Estacion.getEstacionFromNombre('Murcia')
        lamancha = Estacion.getEstacionFromNombre('LaMancha')
        andalucia = Estacion.getEstacionFromNombre('Andalucia')
        extremadura = Estacion.getEstacionFromNombre('Extremadura')
        leon = Estacion.getEstacionFromNombre('Leon')
        madrid = Estacion.getEstacionFromNombre('Madrid')
        canarias = Estacion.getEstacionFromNombre('Canarias')
        baleares = Estacion.getEstacionFromNombre('Baleares')

        a = Estacion.crearTramo
        i = {'tipo': 'catenaria', 'tiempo': 3, 'distancia': 100, 'precio': 3.5}
        j = {'tipo': 'altaVelocidad', 'tiempo': 1, 'distancia': 400, 'precio': 2.5}
        k = {'tipo': 'noCatenaria', 'tiempo': 5, 'distancia': 250, 'precio': 0.8}
        l = {'tipo': 'altaVelocidad', 'tiempo': 1, 'distancia': 500, 'precio': 1.8}

        a(madrid, galicia, 'via', j)
        a(madrid, catalunya, 'via', j)
        a(madrid, asturias, 'via', j)
        a(madrid, cantabria, 'via', j)
        a(madrid, euskadi, 'via', j)
        a(madrid, navarra, 'via', j)
        a(madrid, aragon, 'via', j)
        a(madrid, valencia, 'via', j)
        a(madrid, murcia, 'via', j)

        #union madrid laMancha
        a(madrid, lamancha, 'via', j)
        #comentar abajo para diferente calculo
        a(madrid, lamancha, 'via', l)

        a(madrid, andalucia, 'via', j)
        a(madrid, extremadura, 'via', j)
        a(madrid, leon, 'via', j)
        a(madrid, canarias, 'via', j)
        a(madrid, baleares, 'via', j)

        a(catalunya, valencia, 'via', j)
        a(catalunya, aragon, 'via', j)

        a(valencia, lamancha, 'via', j)
        a(valencia, murcia, 'via', j)

        a(madrid, leon, 'via', k)
        a(madrid, canarias, 'via', k)
        a(madrid, baleares, 'via', k)

        a(madrid, aragon, 'via', j)
        a(madrid, valencia, 'via', k)
        a(madrid, murcia, 'via', i)

        a(madrid, galicia, 'via', i)
        a(madrid, catalunya, 'via', i)
        a(madrid, asturias, 'via', i)


    @staticmethod
    def getVias(nombre):
        db_connection = DbConnection()
        vias = db_connection.graph.cypher.execute(
            "match (n:Estacion {nombre:'" + nombre + "'})-[r:via]->() return r")
        print vias

    @staticmethod
    def getRutaOptima(salida, llegada, tipoServicio):
        db_connection = DbConnection()
        ruta = None
        if tipoServicio == 'economico':
            ruta = db_connection.graph.cypher.execute(
                "match p = (n:Estacion)-[*]->(m:Estacion) where n.nombre = {a} and m.nombre = {b} "
                "with p as camino, reduce(precioTotal = 0, r in relationships(p) | precioTotal + (r.precio * r.distancia)) as coste "
                "return camino, coste "
                "order by coste asc "
                "limit 1 "
                , a = salida, b = llegada)
        else:
            tiempoMaximo = 24
            if tipoServicio == 'intradia':
                tiempoMaximo = 6
            elif tipoServicio == 'primeraHora':
                tiempoMaximo = 12
            elif tipoServicio == 'normal':
                tiempoMaximo = 24
            ruta = db_connection.graph.cypher.execute(
                "match p = (n:Estacion)-[*]->(m:Estacion) where n.nombre = {a} and m.nombre = {b} "
                "with p as camino, reduce(tiempoMinimo = 0, r in relationships(p) | tiempoMinimo + r.tiempo) as tiempoMin "
                "where tiempoMin <= {c} "
                "return camino, tiempoMin "
                "order by tiempoMin asc "
                "limit 1 "
                , a = salida, b = llegada, c = tiempoMaximo)
        return ruta

    @staticmethod
    def getRuta(salida, llegada, tipoServicio, locomotora):
        db_connection = DbConnection()
        rutas = None
        if tipoServicio == 'economico':
            rutas = db_connection.graph.cypher.execute(
                "match p = (n:Estacion)-[*]->(m:Estacion) where n.nombre = {a} and m.nombre = {b} "
                "with p as camino, reduce(precioTotal = 0, r in relationships(p) | precioTotal + (r.precio * r.distancia)) as coste "
                "return camino, coste "
                "order by coste asc "
                , a = salida, b = llegada)
        else:
            rutas = db_connection.graph.cypher.execute(
                "match p = (n:Estacion)-[*]->(m:Estacion) where n.nombre = {a} and m.nombre = {b} "
                "with p as camino, reduce(distancia = 0, r in relationships(p) | distancia + r.distancia) as distanciaMin "
                "return camino, distanciaMin "
                "order by distanciaMin asc "
                , a = salida, b = llegada)

        return Estacion.getRutaValidaParaLocomotora(rutas, locomotora)

    @staticmethod
    #recibe type RecordList
    def getRutaValidaParaLocomotora(rutas, locomotora):
        for ruta in rutas:
            if Estacion.isRutaValidaParaLocomotora(ruta, locomotora):
                return ruta
        return None

    @staticmethod
    #recibe type Record
    def isRutaValidaParaLocomotora(ruta, locomotora):
        #camino type: Path
        camino = ruta[0]
        i = 0
        valido = True
        while(i < camino.size):
            #tmp type: Relationship
            tmp = camino[i]
            i += 1
            if locomotora.properties['tipo'] != tmp.properties['tipo']:
                valido = False
        return valido

    @staticmethod
    def getLocomotoraNombreEnvio(envio):
        db_connection = DbConnection()
        nombre = envio.properties['nombre']
        locomotora = db_connection.graph.cypher.execute(
            "match (n:Envio)-[*1]->(m:Locomotora) where n.nombre = {a} "
            "return m.nombre "
            , a = nombre)
        return locomotora[0][0]
    @staticmethod
    def getSituacionEnvio(envio):
        db_connection = DbConnection()
        nombre = envio.properties['nombre']
        situacion = db_connection.graph.cypher.execute(
            "match (n:Envio)-[*1]->(m:Locomotora)-[]->(e:Estacion) where n.nombre = {a} "
            "return e.nombre "
            , a = nombre)
        return situacion[0][0]

    @staticmethod
    def getTiempoRestanteEnvio(envio, destino):
        db_connection = DbConnection()
        nombre = envio.properties['nombre']
        tipo = envio.properties['tipo']
        origen = Estacion.getSituacionEnvio(envio)
        nombreLocomotora = Estacion.getLocomotoraNombreEnvio(envio)
        locomotora = Locomotora.getLocomotoraFromNombre(nombreLocomotora)

        ruta = Estacion.getRuta(origen, destino, tipo, locomotora)
        tipo_ruta = ruta[0][0].properties['tipo']
        distancia = ruta[0][0].properties['distancia']
        velocidad = None
        if tipo_ruta == 'altaVelocidad':
            #30 minutos en hacer 100 km, la velocidad son 200km/h
            velocidad = 200
        elif tipo_ruta == 'catenaria':
            #50 minutos en hacer 100 km, la velocidad son 120km/h
            velocidad = 120
        elif tipo_ruta == 'noCatenaria':
            #70 minutos en hacer 100 km, la velocidad son 85km/h
            velocidad = 85

        tiempo = distancia / velocidad

        return tiempo

    @staticmethod
    def getResumenEnvioDiaCliente(cliente, fecha):
         db_connection = DbConnection()
         envio = db_connection.graph.cypher.execute(
            "match (n:Envio) "
            "where n.fecha = {a} and n.cliente = {b} return n "
            ,a = fecha, b = cliente)
         return envio

    @staticmethod
    def getResumenMes(mes):
        db_connection = DbConnection()
        media = db_connection.graph.cypher.execute(
            "match (n:Envio) where n.mes= {a} "
            "return avg(n.peso) as mediaPeso, avg(n.volumen) as mediaVolumen, count(n) as cuenta "
            , a = mes)
        return media

    @staticmethod
    def getResumenOcupacion(tipo):
        db_connection = DbConnection()
        media = db_connection.graph.cypher.execute(
            "match (n:Locomotora)-[r]-(e:Estacion) where n.tipo = {a} "
            "return count(r) as numero", a = tipo)
        return media

if __name__ == '__main__':
    DbConnection.deleteAllGraph()
    DbConnection.init()

    Estacion.crearEstaciones()
    Estacion.crearTramos()

    #Estacion.getVias("Madrid")
    madrid = Estacion.getEstacionFromNombre('Madrid')
    Locomotora.createLocomotoras()
    Locomotora.asociarLocomotoras(madrid)

    Envio.createEnvios()
    Envio.asociarEnvios()

    print "Camino economico Madrid - LaMancha:"
    print Estacion.getRutaOptima('Madrid', 'LaMancha', 'economico')

    print "_______"

    print "Camino intradia (menos de 6 horas) Madrid - LaMancha:"
    print Estacion.getRuta('Madrid', 'LaMancha', 'intradia', Locomotora.getLocomotoraFromNombre('TrenToWapo'))

    print "_______"

    envio1 = Envio.getEnvioFromNombre('envio1')
    print "Situacion del envio1:"
    print Estacion.getSituacionEnvio(envio1)

    print "_______"

    print "Tiempo restante del envio1:"
    print Estacion.getTiempoRestanteEnvio(envio1, 'Murcia')

    print "_______"

    print "Envio de opsitseva el 01/01/2016"
    print Estacion.getResumenEnvioDiaCliente('opsitseva', '01/01/2016')

    print "_______"

    print "Envios del mes Enero"
    print Estacion.getResumenMes('Enero')

    print "_______"

    print "Envios de locomotora de altaVelocidad"
    print Estacion.getResumenOcupacion('altaVelocidad')


