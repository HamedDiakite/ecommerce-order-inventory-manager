#!/usr/bin/env python3
"""
Test script to verify custom exception integration
"""

from models import User, Product
from managers import UserManager, ProductManager, OrderManager
from exceptions import (
    AuthenticationError,
    OutOfStockError,
    ProductNotFoundError,
    InvalidInputError
)

def test_authentication_errors():
    """Test AuthenticationError in UserManager"""
    print("\n=== Testing AuthenticationError ===")
    user_manager = UserManager()
    user_manager.register(User("u1", "testuser", "password123", "customer"))
    
    # Test 1: Invalid password
    try:
        user_manager.login("testuser", "wrongpassword")
        print("❌ FAIL: Should have raised AuthenticationError for wrong password")
    except AuthenticationError as e:
        print(f"✓ PASS: AuthenticationError raised for wrong password: {e}")
    
    # Test 2: Non-existent user
    try:
        user_manager.login("nonexistent", "password")
        print("❌ FAIL: Should have raised AuthenticationError for non-existent user")
    except AuthenticationError as e:
        print(f"✓ PASS: AuthenticationError raised for non-existent user: {e}")
    
    # Test 3: Empty credentials
    try:
        user_manager.login("", "")
        print("❌ FAIL: Should have raised AuthenticationError for empty credentials")
    except AuthenticationError as e:
        print(f"✓ PASS: AuthenticationError raised for empty credentials: {e}")

def test_product_not_found_errors():
    """Test ProductNotFoundError in ProductManager"""
    print("\n=== Testing ProductNotFoundError ===")
    product_manager = ProductManager()
    product_manager.add_product(Product("P001", "Test Product", "Category", 10.0, 5))
    
    # Test 1: Get non-existent product
    try:
        product_manager.get_product("P999")
        print("❌ FAIL: Should have raised ProductNotFoundError")
    except ProductNotFoundError as e:
        print(f"✓ PASS: ProductNotFoundError raised for get_product: {e}")
    
    # Test 2: Update non-existent product
    try:
        product_manager.update_product("P999", "Name", "Cat", 20.0, 10)
        print("❌ FAIL: Should have raised ProductNotFoundError")
    except ProductNotFoundError as e:
        print(f"✓ PASS: ProductNotFoundError raised for update_product: {e}")
    
    # Test 3: Delete non-existent product
    try:
        product_manager.delete_product("P999")
        print("❌ FAIL: Should have raised ProductNotFoundError")
    except ProductNotFoundError as e:
        print(f"✓ PASS: ProductNotFoundError raised for delete_product: {e}")

def test_invalid_input_errors():
    """Test InvalidInputError in Product and ProductManager"""
    print("\n=== Testing InvalidInputError ===")
    
    # Test 1: Negative price in Product
    try:
        Product("P001", "Product", "Cat", -10.0, 5)
        print("❌ FAIL: Should have raised InvalidInputError for negative price")
    except InvalidInputError as e:
        print(f"✓ PASS: InvalidInputError raised for negative price: {e}")
    
    # Test 2: Negative quantity in Product
    try:
        Product("P001", "Product", "Cat", 10.0, -5)
        print("❌ FAIL: Should have raised InvalidInputError for negative quantity")
    except InvalidInputError as e:
        print(f"✓ PASS: InvalidInputError raised for negative quantity: {e}")
    
    # Test 3: Empty product ID
    try:
        Product("", "Product", "Cat", 10.0, 5)
        print("❌ FAIL: Should have raised InvalidInputError for empty product ID")
    except InvalidInputError as e:
        print(f"✓ PASS: InvalidInputError raised for empty product ID: {e}")
    
    # Test 4: Duplicate product ID
    product_manager = ProductManager()
    product_manager.add_product(Product("P001", "Product", "Cat", 10.0, 5))
    try:
        product_manager.add_product(Product("P001", "Product2", "Cat", 20.0, 10))
        print("❌ FAIL: Should have raised InvalidInputError for duplicate ID")
    except InvalidInputError as e:
        print(f"✓ PASS: InvalidInputError raised for duplicate ID: {e}")

def test_out_of_stock_errors():
    """Test OutOfStockError in OrderManager"""
    print("\n=== Testing OutOfStockError ===")
    product_manager = ProductManager()
    order_manager = OrderManager(product_manager)
    
    # Add a product with limited stock
    product_manager.add_product(Product("P001", "Limited Product", "Cat", 10.0, 3))
    
    # Create a cart with more items than available
    from models import ShoppingCart
    cart = ShoppingCart("customer1")
    cart.add_item(product_manager.products["P001"], 5)  # Request 5, but only 3 available
    
    try:
        order_manager.place_order(cart, 50.0, 0.0, 50.0, "123 Test St")
        print("❌ FAIL: Should have raised OutOfStockError")
    except OutOfStockError as e:
        print(f"✓ PASS: OutOfStockError raised: {e}")

def test_successful_operations():
    """Test that valid operations work correctly"""
    print("\n=== Testing Successful Operations ===")
    
    # Test successful user registration and login
    user_manager = UserManager()
    user_manager.register(User("u1", "validuser", "validpass", "customer"))
    user = user_manager.login("validuser", "validpass")
    print(f"✓ PASS: User logged in successfully: {user.username}")
    
    # Test successful product operations
    product_manager = ProductManager()
    product_manager.add_product(Product("P001", "Valid Product", "Electronics", 99.99, 10))
    product = product_manager.get_product("P001")
    print(f"✓ PASS: Product retrieved successfully: {product.name}")
    
    product_manager.update_product("P001", "Updated Product", "Electronics", 89.99, 15)
    print(f"✓ PASS: Product updated successfully")
    
    # Test successful order
    from models import ShoppingCart
    cart = ShoppingCart("customer1")
    cart.add_item(product, 2)
    order_manager = OrderManager(product_manager)
    order = order_manager.place_order(cart, 179.98, 0.0, 179.98, "456 Valid St, PA")
    print(f"✓ PASS: Order placed successfully: {order.order_id}")

def main():
    """Run all tests"""
    print("=" * 60)
    print("CUSTOM EXCEPTION INTEGRATION TEST SUITE")
    print("=" * 60)
    
    try:
        test_authentication_errors()
        test_product_not_found_errors()
        test_invalid_input_errors()
        test_out_of_stock_errors()
        test_successful_operations()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
