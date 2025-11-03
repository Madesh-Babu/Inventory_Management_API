from flask import Blueprint,request,jsonify
from ..models import db, Product

products_b_p = Blueprint("products", __name__)

@products_b_p.route("/", methods=["POST"])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        stock=data["stock"]
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added", "product": new_product.to_dict()}), 201


@products_b_p.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@products_b_p.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@products_b_p.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)

    db.session.commit()
    return jsonify({"message": "Product updated", "product": product.to_dict()})



@products_b_p.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})
