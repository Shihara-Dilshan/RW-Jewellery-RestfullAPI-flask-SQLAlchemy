from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;

database = SQLAlchemy(app)
ORM = Marshmallow(app)

#Models

##Customer Model
class Customer(database.Model):
    cus_id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(50))
    last_name = database.Column(database.String(50))
    address = database.Column(database.String(100))
    email = database.Column(database.String(100))
    nic = database.Column(database.String(10))
    telephone = database.Column(database.String(10))
    
    def __init__(self, first_name, last_name, address, email, nic, telephone):
    	self.first_name = first_name
    	self.last_name = last_name
    	self.address = address
    	self.email = email
    	self.nic = nic
    	self.telephone = telephone

##Customer Schema
class CustomerSchema(ORM.Schema):
    class Meta:
    	fields = ('cus_id', 'first_name', 'last_name', 'address', 'email', 'nic', 'telephone')

#Initialize Customer Schema
customer_schema = CustomerSchema()
customer_schema_all = CustomerSchema(many=True)

#customer API

##Register a new customer
@app.route('/register', methods=['POST'])
def add_customer():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    address = request.json['address']
    email = request.json['email']
    nic = request.json['nic']
    telephone = request.json['telephone']

    new_customer = Customer(first_name, last_name, address, email, nic, telephone)

    database.session.add(new_customer)
    database.session.commit()

    return customer_schema.jsonify(new_customer)

##Get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    all_users = Customer.query.all()
    result = customer_schema_all.dump(all_users)
    return jsonify(result)
    
##get a specific customer
@app.route('/customer/<id>', methods=['GET'])
def get_product(id):
    customer = Customer.query.get(id)
    return customer_schema.jsonify(customer)
    
##update a customer
@app.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)
    
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    address = request.json['address']
    email = request.json['email']
    nic = request.json['nic']
    telephone = request.json['telephone']
    
    customer.first_name = first_name
    customer.last_name = last_name
    customer.address = address
    customer.email = email
    customer.nic = nic
    customer.telephone = telephone

    database.session.commit()

    return customer_schema.jsonify(customer)

##delete a specific customer
@app.route('/customer/<id>', methods=['DELETE'])
def delete_product(id):
    customer = Customer.query.get(id)
    database.session.delete(customer)
    database.session.commit()
    
    return customer_schema.jsonify(customer)

#start the server       
if __name__ == '__main__':
    app.run(debug=True)
