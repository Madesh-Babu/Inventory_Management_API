from flask import Blueprint,request,jsonify
from app.models import db, Product,Category
from flask_jwt_extended import jwt_required
from app.products.service import ProductService,DiscountedProductService
from app.utils.roles_required import role_required


products_b_p = Blueprint("products", __name__)

@products_b_p.route("/", methods=["POST"])
@jwt_required()
@role_required("admin","manager")
def add_product():
    data = request.get_json()

    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Missing name or price"}), 400
    
    category =None
    if "categore_id" in data:
        category =Category.query.get(data["category_id"])
        if not category:
            return jsonify({"error":"Invalid category ID"}), 400

    new_product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        stock=data["stock"],
        category_id = data.get("category_id")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added", "product": new_product.to_dict()}), 201


@products_b_p.route("/", methods=["GET"])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@products_b_p.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    if not product:
        return jsonify({'error':"Product not found"}),404
    return jsonify(product.to_dict())


@products_b_p.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
@role_required("admin","manager")
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)

    db.session.commit()
    return jsonify({"message": "Product updated", "product": product.to_dict()}),200



@products_b_p.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}),200


@products_b_p.route("/<int:product_id>/discount", methods=["PATCH"])
def discount_product(product_id):
    product = DiscountedProductService.get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    discount = data.get("discount", 0)
    updated = DiscountedProductService.apply_discount(product, discount)
    return jsonify({
        "message": f"Applied {discount}% discount",
        "new_price": updated.price
    })