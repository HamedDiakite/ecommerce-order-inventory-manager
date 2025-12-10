# managers.py

import heapq
from collections import defaultdict
from models import Order
from exceptions import (
    AuthenticationError,
    OutOfStockError,
    ProductNotFoundError,
    InvalidInputError
)
from state_tax_rates import get_tax_rate, is_valid_state, calculate_tax

class ProductManager:
    """Handles all operations related to products and inventory."""
    def __init__(self):
        self.products = {} 

    def add_product(self, product):
        if product.product_id in self.products:
            raise InvalidInputError("Product ID already exists.")
        self.products[product.product_id] = product

    def get_product(self, product_id):
        product = self.products.get(product_id)
        if product is None:
            raise ProductNotFoundError(f"Product with ID '{product_id}' not found.")
        return product

    def update_product(self, product_id, name, category, price, quantity):
        if product_id not in self.products:
            raise ProductNotFoundError(f"Product with ID '{product_id}' not found.")
        
        # Validate inputs
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
        
        product = self.products[product_id]
        product.name = name
        product.category = category
        product.price = price
        product.quantity = quantity
        return True

    def delete_product(self, product_id):
        if product_id not in self.products:
            raise ProductNotFoundError(f"Product with ID '{product_id}' not found.")
        del self.products[product_id]
        return True
    
    def get_all_products(self):
        return list(self.products.values())

    def search_product_by_name(self, query):
        query = query.lower()
        return [p for p in self.products.values() if query in p.name.lower()]
    
    def get_products_sorted_by_price(self):
        return heapq.nsmallest(len(self.products), self.products.values())

    def get_out_of_stock_products(self):
        return [p for p in self.products.values() if p.quantity == 0]

    # --- NEW: Review Methods ---
    def add_review_to_product(self, product_id, username, review_text):
        product = self.products.get(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID '{product_id}' not found.")
        if not review_text or not isinstance(review_text, str) or not review_text.strip():
            raise InvalidInputError("Review text cannot be empty.")
        product.add_review(username, review_text)
        return True

    def get_product_reviews(self, product_id):
        product = self.products.get(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID '{product_id}' not found.")
        return product.reviews

class UserManager:
    """Manages user authentication."""
    def __init__(self):
        self.users = {} 

    def register(self, user):
        if user.username in self.users:
            raise InvalidInputError("Username already exists.")
        self.users[user.username] = user

    def login(self, username, password):
        if not username or not password:
            raise AuthenticationError("Username and password cannot be empty.")
        
        user = self.users.get(username)
        if not user:
            raise AuthenticationError(f"User '{username}' not found.")
        
        if user.password != password:
            raise AuthenticationError("Invalid password.")
        
        return user

class OrderManager:
    """Handles order processing and history."""
    def __init__(self, product_manager):
        self.orders = []
        self.product_manager = product_manager

    # --- UPDATED: State-Based Tax Calculation Logic ---
    def calculate_order_totals(self, subtotal, state_code):
        """
        Calculates tax and final total based on customer's state.
        Uses comprehensive state tax rate mapping.
        
        Args:
            subtotal (float): Order subtotal before tax
            state_code (str): Two-letter state code (e.g., "CA", "NY")
        
        Returns:
            tuple: (tax_amount, final_total)
        """
        if not state_code:
            # No state provided, no tax applied
            return 0.0, subtotal
        
        # Validate state code
        if not is_valid_state(state_code):
            raise InvalidInputError(f"Invalid state code: '{state_code}'")
        
        # Calculate tax using state-specific rate
        tax_amount, final_total = calculate_tax(subtotal, state_code)
        return tax_amount, final_total

    # UPDATED: Accepts address, state, and tax details
    def place_order(self, cart, subtotal_with_discount, tax, final_total, address, state_code):
        # Validate address
        if not address or not isinstance(address, str) or not address.strip():
            raise InvalidInputError("Shipping address cannot be empty.")
        
        # Validate state code
        if not state_code or not isinstance(state_code, str) or not state_code.strip():
            raise InvalidInputError("State must be selected.")
        
        if not is_valid_state(state_code):
            raise InvalidInputError(f"Invalid state code: '{state_code}'")
        
        # Validate quantities
        for product_id, quantity in cart.items.items():
            product = self.product_manager.products.get(product_id)
            if not product:
                raise ProductNotFoundError(f"Product with ID '{product_id}' not found.")
            if product.quantity < quantity:
                raise OutOfStockError(f"Not enough stock for '{product.name}'. Available: {product.quantity}, Requested: {quantity}")

        items_with_details = []
        for product_id, quantity in cart.items.items():
            product = self.product_manager.products.get(product_id)
            items_with_details.append((product.name, product.price, quantity))
            product.quantity -= quantity

        # Create order with state information
        new_order = Order(cart.customer_id, items_with_details, final_total, tax, address, state_code)
        self.orders.append(new_order)
        return new_order

    def get_orders_by_customer(self, user_id):
        return [o for o in self.orders if o.customer_id == user_id]
    
    def get_all_orders(self):
        return self.orders
        
    def update_order_status(self, order_id, new_status):
        for order in self.orders:
            if order.order_id == order_id:
                order.status = new_status
                return True
        raise ProductNotFoundError(f"Order with ID '{order_id}' not found.")

    def get_total_revenue(self):
        return sum(o.total_price for o in self.orders)
    
    def get_total_orders_placed(self):
        return len(self.orders)
        
    def get_most_frequently_ordered_product(self):
        freq_map = defaultdict(int)
        for order in self.orders:
            for name, price, quantity in order.items:
                freq_map[name] += quantity
        
        if not freq_map: return "N/A"
        return max(freq_map, key=freq_map.get)