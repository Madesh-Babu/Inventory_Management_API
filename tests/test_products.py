import pytest
from app import create_app, db
from app.config import TestConfig

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client


def test_add_product(client):
    res = client.post("/products/", json={
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1200.50,
        "stock": 10
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["product"]["name"] == "Laptop"


def test_get_all_products(client):
    client.post("/products/", json={
        "name": "Mouse",
        "description": "Wireless",
        "price": 25,
        "stock": 50
    })
    res = client.get("/products/")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_get_single_product(client):
    res = client.post("/products/", json={
        "name": "Keyboard",
        "description": "Mechanical",
        "price": 75,
        "stock": 15
    })
    pid = res.get_json()["product"]["id"]
    res = client.get(f"/products/{pid}")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Keyboard"


def test_update_product(client):
    res = client.post("/products/", json={
        "name": "Monitor",
        "description": "LED",
        "price": 300,
        "stock": 20
    })
    pid = res.get_json()["product"]["id"]
    res = client.put(f"/products/{pid}", json={"price": 350})
    assert res.status_code == 200
    assert res.get_json()["product"]["price"] == 350


def test_delete_product(client):
    res = client.post("/products/", json={
        "name": "Tablet",
        "description": "10 inch",
        "price": 500,
        "stock": 5
    })
    pid = res.get_json()["product"]["id"]
    res = client.delete(f"/products/{pid}")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Product deleted"
