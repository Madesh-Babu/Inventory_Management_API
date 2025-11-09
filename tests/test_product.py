def test_add_product(client):
    res = client.post("/products/", json={
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1200.50,
        "stock": 10
    })
    assert res.status_code == 201
    assert res.json()["product"]["name"] == "Laptop"


def test_get_all_products(client):
    client.post("/products/", json={
        "name": "Mouse",
        "description": "Wireless",
        "price": 25,
        "stock": 50
    })
    res = client.get("/products/")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_single_product(client):
    res = client.post("/products/", json={
        "name": "Keyboard",
        "description": "Mechanical",
        "price": 75,
        "stock": 15
    })
    pid = res.json()["product"]["id"]
    res = client.get(f"/products/{pid}")
    assert res.status_code == 200
    assert res.json()["name"] == "Keyboard"


def test_update_product(client):
    res = client.post("/products/", json={
        "name": "Monitor",
        "description": "LED",
        "price": 300,
        "stock": 20
    })
    pid = res.json()["product"]["id"]
    res = client.put(f"/products/{pid}", json={"price": 350})
    assert res.status_code == 200
    assert res.json()["product"]["price"] == 350


def test_delete_product(client):
    res = client.post("/products/", json={
        "name": "Tablet",
        "description": "10 inch",
        "price": 500,
        "stock": 5
    })
    pid = res.json()["product"]["id"]
    res = client.delete(f"/products/{pid}")
    assert res.status_code == 200
    assert res.json()["message"] == "Product deleted"
