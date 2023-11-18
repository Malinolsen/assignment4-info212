from Car_Rental_project.driver import _get_connection, node_to_json

# from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
# import json 

# URI = "neo4j+s://f10a56c5.databases.neo4j.io"
# AUTH = ("neo4j", "NQMqDPzJAaARcU_-0lCoAQ2bB5efvttgj71eDu8fMYA")

# def _get_connection() -> Driver:
#     driver = GraphDatabase.driver(URI, auth=AUTH)
#     driver.verify_connectivity()

#     return driver

# def node_to_json(node):
#      node_properties = dict(node.items())
#      return node_properties

# Class and functions for Employee entities
class Employee:
    def __init__(self, name, branch, address):
        self.name = name
        self.branch = branch
        self.address = address


def create_Employee(name, branch, address):
    with _get_connection().session() as session:
        employees = session.run("CREATE (e:Employee {name:$name, branch:$branch, address:$address})", name=name,
                                branch=branch, address=address)

        nodes_json = [node_to_json(record['e']) for record in employees]
        print(nodes_json)
        return nodes_json


def update_Employee(name, branch, address):
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee{reg:$reg})set e.name:$name, e.branch:$branch, e.address:$address})",
                                name=name, branch=branch, address=address)
        nodes_json = [node_to_json(record['e']) for record in employees]
        print(nodes_json)
        return nodes_json


def read_Employee():
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) Return e;")
        nodes_json = [node_to_json(record["e"]) for record in employees]
        print(nodes_json)
        return nodes_json


def delete_Employee(reg):
    _get_connection().execute_query("MATCH (e:Employee{reg:$reg}}) DETACH DELETE e;", reg=reg)
