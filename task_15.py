''' Task 15 | Integrated Order Fulfillment System
Concepts: OOP, composition, files, exceptions, algorithms
Problem: Design Product, Cart, Order, and Inventory classes. Read a product catalog from JSON, build carts, apply percentage discounts, compute totals, and place orders with stock updates. Persist orders to JSON.
Requirements: Reject invalid quantities and out-of-stock purchases. Validate all items before changing inventory; roll back if order persistence fails. Generate unique order IDs. Include at least three unit tests using unittest.
Sample / expected behavior: Catalog: P1 price=100 stock=5; cart P1 x2 with 10% discount -> total 180, stock becomes 3 after successful order.'''




import json
import os
import uuid
import unittest
import tempfile

from dataclasses import dataclass
from unittest.mock import patch



@dataclass
class Product:
    product_id: str
    name: str
    price: float
    stock: int

    def __post_init__(self):
        if not self.product_id.strip():
            raise ValueError("Product ID cannot be empty")

        if not self.name.strip():
            raise ValueError("Product name cannot be empty")

        if self.price <= 0:
            raise ValueError("Price must be greater than zero")

        if self.stock < 0:
            raise ValueError("Stock cannot be negative")

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }




class Cart:

    def __init__(self, discount_percent=0):
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100")

        self.items = {}
        self.discount_percent = discount_percent

    def add_product(self, product, quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be a whole number")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        self.items[product.product_id] = (
            self.items.get(product.product_id, 0) + quantity
        )

    def calculate_subtotal(self, inventory):
        subtotal = 0

        for product_id, quantity in self.items.items():
            if product_id not in inventory.products:
                raise ValueError("Product does not exist")

            product = inventory.products[product_id]
            subtotal += product.price * quantity

        return subtotal

    def calculate_total(self, inventory):
        subtotal = self.calculate_subtotal(inventory)
        discount = subtotal * self.discount_percent / 100

        return subtotal - discount




class Order:

    def __init__(self, order_id, items, subtotal, discount, total):
        self.order_id = order_id
        self.items = items
        self.subtotal = subtotal
        self.discount = discount
        self.total = total

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "items": self.items,
            "subtotal": round(self.subtotal, 2),
            "discount": round(self.discount, 2),
            "total": round(self.total, 2)
        }




class Inventory:

    def __init__(self, products):
        self.products = {
            product.product_id: product
            for product in products
        }

        if len(self.products) != len(products):
            raise ValueError("Duplicate product IDs found")

    def display_products(self):
        print("\nAVAILABLE PRODUCTS")
        print("-" * 45)

        for product in self.products.values():
            print(
                f"ID: {product.product_id} | "
                f"Name: {product.name} | "
                f"Price: {product.price} | "
                f"Stock: {product.stock}"
            )

    def place_order(self, cart, orders_file):
        if not cart.items:
            raise ValueError("Cart is empty")

       

        for product_id, quantity in cart.items.items():

            if product_id not in self.products:
                raise ValueError(
                    f"Product {product_id} does not exist"
                )

            if not isinstance(quantity, int) or isinstance(quantity, bool):
                raise ValueError("Invalid quantity")

            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero")

            product = self.products[product_id]

            if quantity > product.stock:
                raise ValueError(
                    f"Insufficient stock for {product.name}"
                )

     

        subtotal = cart.calculate_subtotal(self)
        discount = subtotal * cart.discount_percent / 100
        total = subtotal - discount


        if os.path.exists(orders_file):
            with open(orders_file, "r", encoding="utf-8") as file:
                orders = json.load(file)

            if not isinstance(orders, list):
                raise ValueError("Invalid orders file")
        else:
            orders = []

      

        existing_ids = {
            order["order_id"]
            for order in orders
            if isinstance(order, dict) and "order_id" in order
        }

        order_id = uuid.uuid4().hex[:8].upper()

        while order_id in existing_ids:
            order_id = uuid.uuid4().hex[:8].upper()

        

        order_items = []

        for product_id, quantity in cart.items.items():
            product = self.products[product_id]

            order_items.append({
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity
            })

        order = Order(
            order_id,
            order_items,
            subtotal,
            discount,
            total
        )

      

        previous_stock = {
            product_id: self.products[product_id].stock
            for product_id in cart.items
        }

        try:
            for product_id, quantity in cart.items.items():
                self.products[product_id].stock -= quantity

            orders.append(order.to_dict())

            self.save_orders(orders, orders_file)

        except Exception:
            for product_id, old_stock in previous_stock.items():
                self.products[product_id].stock = old_stock

            raise

        return order

    @staticmethod
    def save_orders(orders, orders_file):
        temporary_file = orders_file + ".tmp"

        try:
            with open(temporary_file, "w", encoding="utf-8") as file:
                json.dump(orders, file, indent=4)

            os.replace(temporary_file, orders_file)

        finally:
            if os.path.exists(temporary_file):
                os.remove(temporary_file)




def load_inventory(filename):
    """Read product catalog from JSON."""

    if not os.path.exists(filename):
        sample_products = [
            {
                "product_id": "P001",
                "name": "Laptop",
                "price": 120000,
                "stock": 10
            },
            {
                "product_id": "P002",
                "name": "Mouse",
                "price": 1500,
                "stock": 20
            },
            {
                "product_id": "P003",
                "name": "Keyboard",
                "price": 3500,
                "stock": 15
            }
        ]

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(sample_products, file, indent=4)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Product catalog must contain a list")

        products = [Product(**item) for item in data]

        return Inventory(products)

    except (json.JSONDecodeError, TypeError, KeyError) as error:
        raise ValueError("Unable to read product catalog") from error




class TestOrderFulfillment(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        self.orders_file = os.path.join(
            self.temp_directory.name,
            "orders.json"
        )

        self.product1 = Product("P001", "Laptop", 1000, 5)
        self.product2 = Product("P002", "Mouse", 100, 10)

        self.inventory = Inventory([
            self.product1,
            self.product2
        ])

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_successful_order_with_discount(self):
        cart = Cart(discount_percent=10)

        cart.add_product(self.product1, 2)

        order = self.inventory.place_order(
            cart,
            self.orders_file
        )

        self.assertEqual(order.subtotal, 2000)
        self.assertEqual(order.discount, 200)
        self.assertEqual(order.total, 1800)

        self.assertEqual(self.product1.stock, 3)
        self.assertTrue(os.path.exists(self.orders_file))

    def test_reject_invalid_quantity(self):
        cart = Cart()

        with self.assertRaises(ValueError):
            cart.add_product(self.product1, 0)

        self.assertEqual(self.product1.stock, 5)

    def test_reject_out_of_stock(self):
        cart = Cart()

        cart.add_product(self.product1, 10)

        with self.assertRaises(ValueError):
            self.inventory.place_order(
                cart,
                self.orders_file
            )

        self.assertEqual(self.product1.stock, 5)

    def test_rollback_if_saving_fails(self):
        cart = Cart()

        cart.add_product(self.product1, 2)

        with patch("os.replace", side_effect=OSError("Save failed")):
            with self.assertRaises(OSError):
                self.inventory.place_order(
                    cart,
                    self.orders_file
                )

        self.assertEqual(self.product1.stock, 5)




def main():
    print("ORDER FULFILLMENT SYSTEM")
    print("=" * 45)

    inventory = load_inventory("products.json")

    inventory.display_products()

    print("\nProduct catalog loaded successfully.")

    print("\nRunning unit tests...")
    print("=" * 45)

    unittest.main(
        argv=["task_15.py"],
        exit=False
    )


if __name__ == "__main__":
    main()
