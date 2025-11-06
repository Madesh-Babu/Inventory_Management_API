from app.models import db, Category


class CategoryService:
    """Handles all category-related operations."""

    @staticmethod
    def create_category(name):
        if Category.query.filter_by(name=name).first():
            return None, {"error": "Category already exists"}

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category, None

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category(category_id):
        return Category.query.get_or_404(category_id)

    @staticmethod
    def update_category(category_id, new_name):
        category = Category.query.get(category_id)
        if not category:
            return None, {"error": "Category not found"}

        if Category.query.filter(Category.name == new_name, Category.id != category_id).first():
            return None, {"error": "Category name already in use"}

        category.name = new_name
        db.session.commit()
        return category, None

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return True
