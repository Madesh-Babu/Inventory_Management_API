from fastapi import FastAPI
from .database import Base, engine
from .products.routes import router as product_router
from .models import Product

Base.metadata.create_all(bind=engine)

def create_app():
    app = FastAPI(title="Inventory Management API")
    app.include_router(product_router)
    return app
