from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.categories.service import CategoryService
from app.utils.roles_required import role_required

categories_b_p = Blueprint("categories", __name__)

@categories_b_p.route("/", methods=["POST"])
@jwt_required()
@role_required("admin","manager")
def create_category():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    category, err = CategoryService.create_category(data["name"])
    if err:
        return jsonify(err), 400

    return jsonify({
        "message": "Category created successfully",
        "category": {"id": category.id, "name": category.name}
    }), 201


@categories_b_p.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    categories = CategoryService.get_all_categories()
    return jsonify([{"id": c.id, "name": c.name} for c in categories]), 200


@categories_b_p.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    category = CategoryService.get_category(category_id)
    return jsonify({"id": category.id, "name": category.name}), 200


@categories_b_p.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
@role_required("admin","manager")
def update_category(category_id):
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "New category name is required"}), 400

    updated_category, err = CategoryService.update_category(category_id, data["name"])
    if err:
        return jsonify(err), 400

    return jsonify({
        "message": "Category updated successfully",
        "category": {"id": updated_category.id, "name": updated_category.name}
    }), 200


@categories_b_p.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_category(category_id):
    CategoryService.delete_category(category_id)
    return jsonify({"message": "Category deleted successfully"}), 200
