from flask import Blueprint, jsonify, request
from app.models import db, Category
from flask_jwt_extended import jwt_required

categories_b_p = Blueprint("categories", __name__)

@categories_b_p.route("/", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    if Category.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Category already exists"}), 400

    new_category = Category(
        name=data["name"],
        description=data.get("description", "")
    )
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category created", "category": new_category.to_dict()}), 201


@categories_b_p.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200


@categories_b_p.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict()), 200


@categories_b_p.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()

    category.name = data.get("name", category.name)
    category.description = data.get("description", category.description)
    db.session.commit()

    return jsonify({"message": "Category updated", "category": category.to_dict()}), 200


@categories_b_p.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200
