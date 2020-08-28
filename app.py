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

class Supplier(database.Model):
    supp_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True)
    address = database.Column(database.String(100), unique=True)
    category = database.Column(database.String(10))
    
    def __init__(self, name, address, category):
    	self.name = name
    	self.address = address
    	self.category = category
	
class SupplierSchema(ORM.Schema):
    class Meta:
    	fields = ('supp_id', 'name', 'address', 'category')
    	
supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many = True)

@app.route('/', methods=['GET'])
def get():
    return jsonify({"name" : "rw Jewery"})
    
if __name__ == '__main__':
    app.run(debug=True)
