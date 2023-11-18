# from server import app
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
# from driver import *
from Car_Rental_project.models.car import *
from Car_Rental_project.models.customer import *
from Car_Rental_project.models.employee import *


app= Flask(__name__)

@app.route('/')
def front_page():
    return render_template('index.html')

#Cars
@app.route('/update_car',methods=['GET', 'PUT'])
def update_car_info():
    if request.method == 'PUT':
        record = json.loads(request.data)
        print(record)
        return update_Car(record['make'],record['model'],record['year'],record['address'],record['car_ID'],record['status']) 
    return jsonify({"message":"You can update the car information here."})

@app.route('/create_car', methods=['POST'])
def create_car_info():

    if request.method =='POST':
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        address = request.form.get('address')
        car_id = request.form.get('car_ID')
        status = request.form.get('status')

        return create_Car(make, model, year, address, car_id, status)
        # return jsonify({"message":"Car instance has successfully been created."})

@app.route('/read_car',methods=['GET'])
def query_records_car():
    return Read_Cars()

@app.route('/delete_car', methods=['GET', 'DELETE'])
def delete_car_info():
    if request.method =='DELETE':
        record = json.loads(request.data)
        car_deleted = delete_Car(record['car_id']) 
        if car_deleted:
            return jsonify({"message":"The car is deleted."})
        else:
            return jsonify({"message":"There is no car to delete."})
    
    return jsonify({"message":"You can delete a car instance here."})
        

#Customer
@app.route('/update_customer',methods=['GET', 'PUT'])
def update_customer_info():
    if request.method == 'PUT':
        record = json.loads(request.data)
        print(record)
        return update_Customer(record['name'],record['age'],record['customer_ID'],record['address'])
    
    return jsonify({"message":"You can update customer information here."})

@app.route('/create_customer', methods=['POST'])
def create_customer_info():
    if request.method =='POST':
        name = request.form.get('name')
        age = request.form.get('age')
        customer_ID= request.form.get('customer_ID')
        address = request.form.get('address')
        
        return create_Customer(name,age,customer_ID,address)

@app.route('/read_customer',methods=['GET'])
def query_records_customer():
    return read_Customer()

@app.route('/delete_customer', methods=['GET', 'DELETE'])
def delete_customer_info():
    if request.method == 'DELETE':
        record = json.loads(request.data)
        print(record)
        delete_Customer(record['reg'])
        return read_Customer()
    return jsonify({"message":"You can delete a customer instance."})

#Employee
@app.route('/update_employee',methods=['GET', 'PUT'])
def update_employee_info():
    if request.method=='PUT':
        record = json.loads(request.data)
        print(record)
        return update_Employee(record['name'],record['branch'],record['address'])
    
    return jsonify({"message":"You can update employee information here."})

@app.route('/create_employee', methods=['POST'])
def create_employee_info():
    if request.method =='POST':
        name = request.form.get('name')
        branch = request.form.get('branch')
        address= request.form.get('address')
        
        return create_Employee(name,branch,address)

@app.route('/read_employee',methods=['GET'])
def query_records_employee():
    return read_Employee()

@app.route('/delete_employee', methods=['GET', 'DELETE'])
def delete_employee_info():
    if request.method=='DELETE':
        record = json.loads(request.data)
        print(record)
        delete_Employee(record['reg'])
        return read_Employee()
    return jsonify({"message":"Customer instance can be deleted here"})


#Order car
@app.route('/order_car', methods=['GET', 'POST'])
def order_car():
    if request.method == 'POST':
        customer_id = request.form.get('customer_ID')
        car_id = request.form.get('car_ID')
        
        booked_cars = check_customerBookings(customer_id)
        if booked_cars:
            return jsonify({"message": "Customer has already booked a car"}), 200
        
        car_status = check_car_status(car_id)
        if not car_status:
            return jsonify({"message":"Car is not available"})
        
        create_booking(customer_id, car_id)
        if create_booking:
            return jsonify({"message":"Car successfully booked."})
    
    # return render_template('orderCar.html')


#Cancel car order
@app.route('/cancel_car_order', methods=['POST'])
def cancel_car_order():
    if request.method == 'POST':
        customer_id = request.form.get('customer_ID')
        car_id = request.form.get('car_ID')
        
        car = check_customerBookings(customer_id)
        
        if not car:
            return jsonify({"message": "Customer has not booked this car."})
        
        update_available_status(car_id)
        return jsonify({"message": "Car order is successfully cancelled."})
        
#Rent car 
@app.route('/rent_car', methods=['POST'])
def rent_car():
    if request.method == 'POST':
        customer_id = request.form.get('customer_ID')
        car_id = request.form.get('car_ID')
        car_rent = rented_car_status(customer_id, car_id)
            
        if car_rent:
            return jsonify({"message":"Customer is now renting the car"})
        else:
            return jsonify({"message":"Customer has not booked the car"})


#Return car 
@app.route('/return_car', methods=['POST'])
def return_car():
    if request.method == 'POST':
        customer_id = request.form.get('customer_ID')
        car_id = request.form.get('car_ID')
        car_status = request.form.get('car_status')
        
        if car_status not in ['available', 'damaged']:
            return jsonify({"message": "Customer provided invalid car status. It must be either available or damaged"})
        
        returned_car = return_car(customer_id, car_id, car_status)
        if not returned_car: 
            return jsonify({"message": "Customer has not booked the car"})
        else:
            return jsonify({"message": f"Car status updated to {car_status}"})


if __name__== '__main__':
    app.run(True)
