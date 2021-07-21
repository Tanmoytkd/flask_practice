from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['PSQL_DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.post('/product')
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    if 'id' in request.json:
        new_product.id = request.json['id']

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.get('/product')
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.get('/product/<id>')
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


@app.put('/product/<id>')
def update_product(id):
    product = Product.query.get(id)

    product.name = request.json['name'] if 'name' in request.json else product.name
    product.description = request.json['description'] if 'description' in request.json else product.description
    product.price = request.json['price'] if 'price' in request.json else product.price
    product.qty = request.json['qty'] if 'qty' in request.json else product.qty

    db.session.commit()

    return product_schema.jsonify(product)


@app.delete('/product/<id>')
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)

@app.route('/', methods=["GET", "POST"])
def get_root():
    return jsonify({"state": "Root"})


@app.route('/home', methods=["GET", "POST"])
def get_home():
    return jsonify({"state": "Home"})


if __name__ == '__main__':
    app.run(debug=True)
