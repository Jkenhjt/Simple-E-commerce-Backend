import pytest
import requests


session = requests.Session()


def test_register():
    response = session.post(
        "http://fastapi:8000/register",
        json={"username": "Adminuser", "password": "pass"},
    )

    assert response.status_code == 200


def test_register_to_same_data():
    response = session.post(
        "http://fastapi:8000/register",
        json={"username": "Adminuser", "password": "pass"},
    )

    assert response.status_code == 400


def test_login():
    response = session.post(
        "http://fastapi:8000/login", json={"username": "Adminuser", "password": "pass"}
    )

    assert response.status_code == 200
    assert response.cookies.get("session") != None
    assert response.cookies.get("session") != ""


def test_login_to_another_pass():
    response = session.post(
        "http://fastapi:8000/login", json={"username": "Adminuser", "password": "pass1"}
    )

    assert response.status_code == 404


def test_login_to_another_data():
    response = session.post(
        "http://fastapi:8000/login",
        json={"username": "Adminuser1", "password": "pass1"},
    )

    assert response.status_code == 404


def test_index():
    response = session.get("http://fastapi:8000/")

    assert response.status_code == 200


def test_add_product():  # Only if admin
    response = session.post(
        "http://fastapi:8000/admin/add_product",
        json={
            "name": "tea",
            "description": "very good tea",
            "price": 12.34,
            "quantity": 2,
            "category": "drink",
            "imageName": "2.png",
        },
    )

    assert response.status_code == 200

    response = session.post(
        "http://fastapi:8000/admin/add_product",
        json={
            "name": "tea",
            "description": "very good tea",
            "price": 12.34,
            "quantity": 2,
            "category": "drink",
            "imageName": "2.png",
        },
    )

    response = session.post(
        "http://fastapi:8000/admin/add_product",
        json={
            "name": "tea",
            "description": "very good tea",
            "price": 12.34,
            "quantity": 2,
            "category": "drink",
            "imageName": "2.png",
        },
    )

    response = session.post(
        "http://fastapi:8000/admin/add_product",
        json={
            "name": "tea",
            "description": "very good tea",
            "price": 12.34,
            "quantity": 2,
            "category": "drink",
            "imageName": "2.png",
        },
    )


def test_add_product2():
    response = requests.post(
        "http://fastapi:8000/admin/add_product",
        json={
            "name": "tea",
            "description": "very good tea",
            "price": 12.34,
            "quantity": 2,
            "category": "drink",
            "imageName": "2.png",
        },
    )

    assert response.status_code == 401


def test_add_product_not_need_type_data():
    response = session.post(
        "http://fastapi:8000/admin/add_product",
        json={"name": 123, "description": 123, "price": 123},
    )

    assert response.status_code == 422


def test_add_product_mismatch_some_data():
    response = session.post(
        "http://fastapi:8000/admin/add_product", json={"name": 123, "price": 123}
    )

    assert response.status_code == 422


def test_get_products():
    response = session.get(
        "http://fastapi:8000/products?limit=10000&offset=0&category=drink"
    )

    assert response.status_code == 200
    assert response.json() != None


def test_get_products2():
    response = requests.get(
        "http://fastapi:8000/products?limit=10000&offset=0&category=drink"
    )

    assert response.status_code == 401


def test_get_products3():
    response = session.get(
        "http://fastapi:8000/products?limit=9999999999999999&offset=0&category=drink"
    )

    assert response.status_code == 400


def test_get_products4():
    response = session.get(
        "http://fastapi:8000/products?limit=10000&offset=9999999999999999&category=drink"
    )

    assert response.status_code == 400


def test_get_products5():
    response = session.get(
        "http://fastapi:8000/products?limit=10000&offset=0&category=drinknjndoaijd"
    )

    assert response.status_code == 200


def test_get_product():
    response = session.get("http://fastapi:8000/product?id=2")

    assert response.status_code == 200
    assert response.json()["name"] == "tea"
    assert float(response.json()["price"]) == 12.34


def test_get_product2():
    response = requests.get("http://fastapi:8000/product?id=2")

    assert response.status_code == 200
    assert response.json()["name"] == "tea"
    assert float(response.json()["price"]) == 12.34

    response = requests.get("http://fastapi:8000/image?imageName=2.png")

    assert response.status_code == 200


def test_get_product3():
    response = session.get("http://fastapi:8000/product?id=2222222222")

    assert response.status_code == 400


def test_get_product4():
    response = session.get("http://fastapi:8000/product?id=-1")

    assert response.status_code == 404


def test_update_product():  # Only if admin
    response = session.post(
        "http://fastapi:8000/admin/update_product/1",
        json={
            "name": "tea",
            "description": "very good tea",
            "price": 12.34,
            "quantity": 2,
            "category": "drink",
            "imageName": "2.png",
        },
    )

    assert response.status_code == 200


def test_update_product2():
    response = requests.post(
        "http://fastapi:8000/admin/update_product/1",
        json={
            "name": "tea",
            "description": "very good tea",
            "price": 12.34,
            "quantity": 2,
            "category": "drink",
            "imageName": "2.png",
        },
    )

    assert response.status_code == 401


def test_update_product_not_need_type_data():
    response = session.post(
        "http://fastapi:8000/admin/update_product/1",
        json={"name": 123, "description": 123, "price": 123},
    )

    assert response.status_code == 422


def test_update_product_mismatch_some_data():
    response = session.post(
        "http://fastapi:8000/admin/update_product/1", json={"name": 123, "price": 123}
    )

    assert response.status_code == 422


def test_delete_product():  # Only if admin
    response = session.delete(
        "http://fastapi:8000/admin/delete_product", json={"id": 1}
    )

    assert response.status_code == 200


def test_delete_product2():
    response = requests.delete(
        "http://fastapi:8000/admin/delete_product", json={"id": 2}
    )

    assert response.status_code == 401


def test_delete_product3():
    response = session.delete(
        "http://fastapi:8000/admin/delete_product", json={"id": 999}
    )

    assert response.status_code == 200


def test_cart_add_product():
    response = session.post("http://fastapi:8000/cart?productID=2")

    assert response.status_code == 200


def test_cart_add_product2():
    response = requests.post("http://fastapi:8000/cart?productID=2")

    assert response.status_code == 401


def test_cart_add_product3():
    response = session.post("http://fastapi:8000/cart?productID=9999")

    assert response.status_code == 404


def test_cart_add_product4():
    response = session.post("http://fastapi:8000/cart?productID=-1")

    assert response.status_code == 404


def test_cart_delete_product():
    response = session.delete("http://fastapi:8000/cart?productID=2")

    assert response.status_code == 200


def test_cart_delete_product2():
    response = requests.delete("http://fastapi:8000/cart?productID=2")

    assert response.status_code == 401


def test_cart_delete_product3():
    response = session.delete("http://fastapi:8000/cart?productID=9999")

    assert response.status_code == 200


def test_cart_delete_product4():
    response = session.delete("http://fastapi:8000/cart?productID=-1")

    assert response.status_code == 200


def test_cart_get():
    response = session.get("http://fastapi:8000/cart")

    assert response.status_code == 200


def test_cart_get2():
    response = requests.get("http://fastapi:8000/cart")

    assert response.status_code == 401


def test_payment():
    response = session.post(
        "http://fastapi:8000/payment",
        json={"cardNumber": "1111222233334444", "cardDate": "99/99", "cardCVV": "1234"},
    )

    assert response.status_code == 200
