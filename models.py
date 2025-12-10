# models.py

import uuid
import datetime
from exceptions import InvalidInputError

class Product:
    """Represents a product in the inventory."""
    def __init__(self, product_id, name, category, price, quantity):
        # Validate inputs
        if not product_id or not isinstance(product_id, str):
            raise InvalidInputError("Product ID must be a non-empty string.")
        if not name or not isinstance(name, str):
            raise InvalidInputError("Product name must be a non-empty string.")
        
        try:
            price = float(price)
            if price < 0:
                raise InvalidInputError("Price cannot be negative.")
        except (ValueError, TypeError):
            raise InvalidInputError("Price must be a valid number.")
        
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise InvalidInputError("Quantity cannot be negative.")
        except (ValueError, TypeError):
            raise InvalidInputError("Quantity must be a valid integer.")
        
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        # NEW: Added a list to store reviews
        self.reviews = [] # List of tuples: (username, review_text)

    def add_review(self, username, review_text):
        self.reviews.append((username, review_text))

    def __lt__(self, other):
        return self.price < other.price

class User:
    """Represents a user of the system."""
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

class ShoppingCart:
    """Manages items for a customer before purchase."""
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.items = {} 

    def add_item(self, product, quantity=1):
        if product.product_id in self.items:
            self.items[product.product_id] += quantity
        else:
            self.items[product.product_id] = quantity

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def clear(self):
        self.items = {}

class Order:
    """Represents a completed transaction."""
    # MODIFIED: Added address, state, and tax to the order
    def __init__(self, customer_id, items_with_details, total_price, tax, address, state_code):
        self.order_id = str(uuid.uuid4())[:8]
        self.customer_id = customer_id
        self.items = items_with_details
        self.total_price = total_price # This is the final price INCLUDING tax
        self.tax = tax
        self.address = address
        self.state_code = state_code  # Two-letter state code (e.g., "CA", "NY")
        self.timestamp = datetime.datetime.now()
        self.status = "Placed"