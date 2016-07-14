from py2neo import Graph, Node, Relationship, authenticate

class DbConnection():
    def __init__(self):
        authenticate('localhost:7474', 'neo4j', 'neo4j')
        self.graph = Graph('http://localhost:7474/db/data/')

    @staticmethod
    def init():
        a = DbConnection()

        a.graph.schema.drop_uniqueness_constraint('Estacion', 'nombre')
        a.graph.schema.drop_uniqueness_constraint('Locomotora', 'nombre')

        a.graph.schema.create_uniqueness_constraint('Estacion', 'nombre')
        a.graph.schema.create_uniqueness_constraint('Locomotora', 'nombre')

    @staticmethod
    def deleteAllRelationships():
        db_connection = DbConnection()
        db_connection.graph.cypher.execute("match () - [r] - () delete r")

    @staticmethod
    def deleteAllNodes():
        db_connection = DbConnection()
        db_connection.graph.cypher.execute("match n delete n")

    @staticmethod
    def deleteAllGraph():
        DbConnection.deleteAllRelationships()
        DbConnection.deleteAllNodes()


if __name__ == '__main__':

    alice = Node('Person', name='Alice')
    db_connection = DbConnection()
    a = db_connection.graph.cypher.execute('match (n:Person) return n')
    print a

