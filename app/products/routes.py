from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Product
from ..database import get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", status_code=201)
def add_product(data: dict, db: Session = Depends(get_db)):
    new_product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        stock=data["stock"]
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added", "product": new_product.to_dict()}


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [p.to_dict() for p in products]


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.to_dict()


@router.put("/{product_id}")
def update_product(product_id: int, data: dict, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)

    db.commit()
    db.refresh(product)
    return {"message": "Product updated", "product": product.to_dict()}


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
