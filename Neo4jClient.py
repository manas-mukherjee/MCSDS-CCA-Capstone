from neo4j import GraphDatabase

class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        # result = tx.run("CREATE (a:Greeting) "
                        # "SET a.message = $message "
                        # "RETURN a.message + ', from node ' + id(a)", message=message)

        result = tx.run("MATCH (author:Authors) RETURN author.name LIMIT 10")


        return result.single()[0]

    def add_person(self, name):
        with self._driver.session() as session:
            session.run("CREATE (a:Person {name: $name})", name=name)

client = HelloWorldExample("bolt://localhost:7687", "neo4j", "graph@2019")

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "graph@2019"))
with driver.session() as session:
    tx = session.begin_transaction()

    HelloWorldExample._create_and_return_greeting(tx, "This is cool")
# client.add_person("Manas")