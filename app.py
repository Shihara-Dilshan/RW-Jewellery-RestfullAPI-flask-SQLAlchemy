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
    	fields = ('first_name', 'last_name', 'address', 'email', 'nic', 'telephone')

#Initialize Customer Schema
customer_schema = CustomerSchema()

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
    return customer_schema.jsonify(all_users)


#start the server       
if __name__ == '__main__':
    app.run(debug=True)
