from app.models import db, Product, Category




def validate_product_data(data):
    """Validate the product JSON payload."""
    required_fields = ["name", "price", "stock"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"

    if not isinstance(data["price"], (int, float)) or data["price"] < 0:
        return False, "Price must be a positive number."

    if not isinstance(data["stock"], int) or data["stock"] < 0:
        return False, "Stock must be a non-negative integer."

    # Optional: validate category if provided
    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category:
            return False, "Invalid category ID."

    return True, None


class ProductService:
    """Handles all product-related database operations."""

    @staticmethod
    def create_product(data):
        """Create a new product."""
        category = None
        if "category_id" in data:
            category = Category.query.get(data["category_id"])
            if not category:
                return None, {"error": "Invalid category ID"}

        new_product = Product(
            name=data["name"],
            description=data.get("description", ""),
            price=data["price"],
            stock=data.get("stock", 0),
            category_id=data.get("category_id"),
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product, None

    @staticmethod
    def get_all_products():
        """Retrieve all products."""
        return Product.query.all()

    @staticmethod
    def get_product(product_id):
        """Retrieve a single product by ID."""
        return Product.query.get_or_404(product_id)

    @staticmethod
    def update_product(product_id, data):
        """Update a product."""
        product = Product.query.get_or_404(product_id)

        if "category_id" in data:
            category = Category.query.get(data["category_id"])
            if not category:
                return None, {"error": "Invalid category ID"}

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.stock = data.get("stock", product.stock)
        product.category_id = data.get("category_id", product.category_id)

        db.session.commit()
        return product, None

    @staticmethod
    def delete_product(product_id):
        """Delete a product."""
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return True

class DiscountedProductService(ProductService):
    """Extends base product logic with discount support."""
    
    @staticmethod
    def apply_discount(product, discount_percentage):
        product.price -= product.price * (discount_percentage / 100)
        db.session.commit()
        return product