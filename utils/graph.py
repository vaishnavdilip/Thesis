"""
This file contains functions that can be used throughout the project.
"""

from neo4j import GraphDatabase, basic_auth

class Graph:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = self.create_driver()

    def create_driver(self):
        driver = GraphDatabase.driver(self.uri,auth=basic_auth(self.username, self.password))
        return driver

    def write_query(self, cypher_query):
        with self.driver.session(database="neo4j") as session:
            results = session.execute_read(
                lambda tx: tx.run(cypher_query).data())
        self.driver.close()

        return results
    
    def create_person_work(tx, name):
        return tx.run("CREATE (p:Person {name: $name}) RETURN p", name=name).single()

    def create_person(name):
        # Create a Session for the `people` database
        session = driver.session(database="people")

        # Create a node within a write transaction
        record = session.execute_write(create_person_work, name=name)

        # Get the `p` value from the first record
        person = record["p"]

        # Close the session
        session.close()

        # Return the property from the node
        return person["name"]

