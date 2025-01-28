import json
import products
from cart import dao
from products import Product

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])

def get_cart(username: str) -> list:
    # Fetch the cart details from the database
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []

    # Parse contents and map product details efficiently
    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Safe JSON parsing
            items.extend(contents)  # Add all items to the list
        except json.JSONDecodeError:
            continue  # Skip invalid contents

    # Get product details for all items
    products_list = [products.get_product(item) for item in items]
    return products_list

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)

