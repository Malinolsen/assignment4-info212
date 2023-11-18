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

class Car:
    def __init__(self, make, model, year, address, car_ID, status):
        self.make = make
        self.model = model
        self.year = year
        self.address = address
        self.car_ID = car_ID
        self.status = status


def create_Car(make, model, year, address, car_ID, status):
    with _get_connection().session() as session:
        cars = session.run(
            "CREATE (a:Car {make: $make, model:$model, year:$year, address:$address, car_ID:$car_ID, status:$status})",
            make=make, model=model, year=year, address=address, car_ID=car_ID, status=status)

        nodes_json = [node_to_json(record['a']) for record in cars]
        print(nodes_json)
        return nodes_json


def update_Car(make, model, year, address, car_ID, status):
    with _get_connection().session() as session:
        cars = session.run(
            "MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year=$year, a.address=$address, a.car_ID=$car_ID, a.status=$status RETURN a;",
            make=make, model=model, year=year, address=address, car_ID=car_ID, status=status)
        # print(cars)
        nodes_json = [node_to_json(record['a']) for record in cars]
        # print(nodes_json)
        return nodes_json


def delete_Car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg:$reg} DETACH DELETE a;", reg=reg)
    


def Read_Cars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) Return a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json


def check_car_status(car_ID):
    with _get_connection().session() as session:
        car_status_available = session.run("MATCH(a:Car {car_ID:$car_ID, status: 'available'})set a.status='Booked' RETURN a",
                                 car_ID=car_ID)
        return car_status_available.single()

def update_available_status(car_ID):
    with _get_connection().session() as session:
        booked_status = session.run("MATCH(a:Car {car_ID:$car_ID, status: 'booked'})set a.status='available' RETURN a",
                                 car_ID=car_ID)
        return booked_status.single()


def rented_car_status(customer_ID, car_ID):
    with _get_connection().session() as session:
        check_booked=session.run("MATCH(p:Customer {customer_ID:$customer_ID})-->(a:Car {car_ID:$car_ID, status: 'Booked'}) RETURN a", customer_ID=customer_ID, car_ID= car_ID)
        if check_booked:
            car_status_booked= session.run("MATCH(a:Car {car_ID:$car_ID, status: 'booked'})set a.status='rented' RETURN a",
                                 car_ID=car_ID)
            return car_status_booked.single()

def booked_status(customer_ID, car_ID):
    with _get_connection().session() as session: 
        car_status = session.run("MATCH(p:Customer {customer_ID:$customer_ID})-->(a:Car {car_ID:$car_ID, status: 'Booked'}) RETURN a", customer_ID=customer_ID, car_ID=car_ID)
        if car_status:
            return car_status.single()

def return_car(customer_ID, car_ID, car_status):
    with _get_connection().session() as session: 
        # check_booked_car=booked_status(customer_ID, car_ID)

        # if check_booked_car:
        car_returned = session.run("MATCH(a:Car {car_ID:$car_ID, status: 'Booked'})SET a.status= $car_status RETURN a",
                                 car_ID=car_ID, car_status=car_status)
        return car_returned.single()

