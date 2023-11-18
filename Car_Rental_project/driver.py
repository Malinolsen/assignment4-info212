from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json 

URI = "neo4j+s://f10a56c5.databases.neo4j.io"
AUTH = ("neo4j", "NQMqDPzJAaARcU_-0lCoAQ2bB5efvttgj71eDu8fMYA")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def node_to_json(node):
     node_properties = dict(node.items())
     return node_properties