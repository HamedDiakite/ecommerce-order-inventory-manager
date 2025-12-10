# main.py

from models import User, Product
from managers import UserManager, ProductManager, OrderManager
from gui import Application
from exceptions import ECommerceError, InvalidInputError

def main():
    try:
        # --- Backend Initialization ---
        product_manager = ProductManager()
        user_manager = UserManager()
        order_manager = OrderManager(product_manager)

        # --- Pre-populate with Sample Data ---
        # Users
        user_manager.register(User("admin01", "admin", "admin123", "admin"))
        user_manager.register(User("cust01", "alice", "alice123", "customer"))
        user_manager.register(User("cust02", "bob", "bob123", "customer"))

        # Products
        product_manager.add_product(Product("P001", "Laptop", "Electronics", 1200.00, 10))
        product_manager.add_product(Product("P002", "Smartphone", "Electronics", 800.00, 25))
        product_manager.add_product(Product("P003", "Coffee Maker", "Appliances", 75.50, 50))
        product_manager.add_product(Product("P004", "Desk Chair", "Furniture", 150.75, 15))
        product_manager.add_product(Product("P005", "Wireless Mouse", "Electronics", 25.00, 100))
        product_manager.add_product(Product("P006", "Monitor", "Electronics", 300.00, 0))

        # --- Frontend Initialization and Execution ---
        app = Application(user_manager, product_manager, order_manager)
        app.mainloop()
        
    except InvalidInputError as e:
        print(f"Data Initialization Error: {e}")
    except ECommerceError as e:
        print(f"Application Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()