# 🛒 E-Commerce Order and Inventory Manager

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)]()

> A comprehensive Python-based desktop application simulating a complete e-commerce platform with role-based access control, inventory management, and state-based tax calculations.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Recent Updates](#-recent-updates)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Features in Detail](#-features-in-detail)
- [Custom Exception Handling](#-custom-exception-handling)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

The **E-Commerce Order and Inventory Manager** is a full-featured desktop application that demonstrates the practical application of data structures and algorithms in solving real-world business problems. Built with Python and Tkinter, it provides a complete e-commerce experience with separate interfaces for administrators and customers.

### Project Objectives

- Implement role-based authentication system (Admin/Customer)
- Provide comprehensive product and inventory management
- Enable seamless shopping cart and order processing
- Calculate accurate state-based sales tax for all 50 US states + DC
- Support promotional discount codes
- Track order history and status updates
- Generate business analytics and reports

---

## ✨ Key Features

### 👨‍💼 Administrator Features

- **Product Management**: Full CRUD operations (Create, Read, Update, Delete)
- **Order Management**: View all customer orders with detailed information
- **Order Status Updates**: Update order status (Placed → Shipped → Delivered)
- **Business Analytics**:
  - Total revenue calculation
  - Best-selling products identification
  - Inventory health monitoring
  - Out-of-stock alerts
  - Total orders processed

### 🛍️ Customer Features

- **Product Browsing**: Search and filter products by category
- **Shopping Cart**: Add, remove, and update product quantities
- **Discount Codes**: Apply promotional codes at checkout
- **State-Based Tax**: Automatic tax calculation for all 51 US jurisdictions
- **Order Placement**: Secure checkout with address and state selection
- **Order History**: Track past orders and current status
- **Product Reviews**: Write and view product reviews with ratings

---

## 🆕 Recent Updates

### ⭐ State-Based Tax System (v1.0)

- **Comprehensive Coverage**: Support for all 50 US states + District of Columbia
- **Real-Time Calculation**: Automatic tax updates based on state selection
- **Tax Rate Display**: Transparent tax rate percentage shown to customers
- **Accurate Rates**: Includes states with no sales tax (AK, DE, MT, NH, OR)
- **Order Records**: State information stored with each order for compliance

### 🛡️ Exception Handling Framework

- **Custom Exception Hierarchy**: Specialized exceptions for different error scenarios
- **Input Validation**: Comprehensive validation at all entry points
- **User-Friendly Errors**: Clear error messages for better user experience
- **Robust Operation**: Graceful error handling prevents application crashes
- **Test Coverage**: 16 test cases covering all exception scenarios

---

## 🔧 Technology Stack

### Core Technologies

- **Python 3.x**: Primary programming language
- **Tkinter**: GUI framework for desktop interface
- **ttk**: Themed widgets for modern UI appearance

### Data Structures

- **HashMaps (Dictionaries)**: O(1) product lookups, user authentication
- **Lists**: Order history, shopping cart items
- **Min-Heaps**: Efficient best-selling product identification
- **Frequency Maps**: Product popularity tracking

### Design Patterns

- **MVC Architecture**: Separation of models, managers, and views
- **Exception Hierarchy**: Custom exception classes for error handling
- **Modular Design**: Clear separation of concerns across modules

---

## 📦 Installation

### Prerequisites

- Python 3.x installed on your system
- Tkinter (usually included with Python)

### Steps

1. **Clone or Download the Repository**
   ```bash
   cd /home/CSC530/ecommerce_project
   ```

2. **Verify Python Installation**
   ```bash
   python3 --version
   ```

3. **Verify Tkinter Installation**
   ```bash
   python3 -c "import tkinter; print('Tkinter is installed')"
   ```

4. **No Additional Dependencies Required**
   - The project uses only Python standard library modules
   - No pip installations needed

---

## 🚀 Usage

### Running the Application

```bash
cd /home/CSC530/ecommerce_project
python3 main.py
```

### Pre-Configured Accounts

The application comes with sample accounts for testing:

#### Administrator Account
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full product and order management capabilities

#### Customer Accounts
- **Username**: `alice` | **Password**: `alice123`
- **Username**: `bob` | **Password**: `bob123`
- **Access**: Shopping, cart, and order history features

### Sample Products

The system is pre-populated with sample products:
- Laptop (Electronics) - $1,200.00
- Smartphone (Electronics) - $800.00
- Coffee Maker (Appliances) - $75.50
- Desk Chair (Furniture) - $150.75
- Wireless Mouse (Electronics) - $25.00
- Monitor (Electronics) - $300.00 (Out of Stock)

---

## 📁 Project Structure

```
ecommerce_project/
│
├── main.py                              # Application entry point
├── models.py                            # Data models (User, Product, Order, Cart, Review)
├── managers.py                          # Business logic (UserManager, ProductManager, OrderManager)
├── gui.py                               # Tkinter GUI implementation
├── exceptions.py                        # Custom exception classes
├── state_tax_rates.py                   # US state tax rate mappings
├── test_exceptions.py                   # Exception handling test suite
│
├── README.md                            # This file
├── COMPREHENSIVE_PROJECT_REPORT.md      # Detailed project documentation
├── CHANGES_STATE_TAX.md                 # State tax system implementation details
└── EXCEPTION_INTEGRATION_SUMMARY.md     # Exception handling integration guide
```

### Module Descriptions

| Module | Lines | Purpose |
|--------|-------|---------|
| `main.py` | 40 | Application initialization and sample data setup |
| `models.py` | 82 | Data classes with validation |
| `managers.py` | 205 | Business logic and data management |
| `gui.py` | 658 | Complete GUI implementation |
| `exceptions.py` | 20 | Custom exception hierarchy |
| `state_tax_rates.py` | 198 | State tax rate database and utilities |
| `test_exceptions.py` | 172 | Comprehensive test suite |

---

## 🎨 Features in Detail

### 1. User Authentication

**Role-Based Access Control**
- Two distinct user roles: Administrator and Customer
- Secure login with username/password validation
- Registration system for new customers
- Session management throughout application lifecycle

**Exception Handling**
- `AuthenticationError`: Invalid credentials, empty fields
- Clear error messages guide users to correct issues

---

### 2. Product Management (Admin Only)

**CRUD Operations**
- **Create**: Add new products with ID, name, category, price, quantity
- **Read**: View all products in searchable table
- **Update**: Modify product details and inventory levels
- **Delete**: Remove products from catalog

**Input Validation**
- Product ID must be unique and non-empty
- Price must be non-negative
- Quantity must be non-negative integer
- Raises `InvalidInputError` for violations

**Search & Filter**
- Search by product name or ID
- Filter by category (All, Electronics, Appliances, Furniture)
- Real-time results update

---

### 3. Shopping Cart & Order Processing

**Cart Management**
- Add products with desired quantities
- Update quantities directly in cart
- Remove items from cart
- Real-time subtotal calculation

**Discount Codes**
- Apply promotional codes at checkout
- Automatic discount calculation
- Visual feedback on applied discounts

**Checkout Process**
1. Select shipping state from dropdown (all 51 US jurisdictions)
2. Enter shipping address
3. View real-time tax calculation based on state
4. Review order summary with itemized costs
5. Confirm and place order

**Order Validation**
- Ensures cart is not empty
- Validates state selection
- Validates shipping address
- Checks product availability
- Verifies sufficient inventory
- Raises appropriate exceptions for violations

---

### 4. State-Based Tax Calculation

**Comprehensive Coverage**
- All 50 US states + District of Columbia
- Accurate tax rates for each jurisdiction
- Includes states with 0% sales tax (AK, DE, MT, NH, OR)

**Tax Rate Examples**
| State | Tax Rate |
|-------|----------|
| California (CA) | 7.25% |
| Texas (TX) | 6.25% |
| Pennsylvania (PA) | 6.00% |
| New York (NY) | 4.00% |
| Oregon (OR) | 0.00% |

**Real-Time Calculation**
- Tax updates automatically when state is selected
- Tax rate percentage displayed for transparency
- Formula: `tax_amount = subtotal × tax_rate`

**Order Records**
- State code stored with each order
- Enables accurate historical reporting
- Supports tax compliance and auditing

---

### 5. Product Reviews & Ratings

**Review System**
- Customers can write reviews for products
- 5-star rating system
- Reviews displayed with customer name and timestamp
- Average rating calculation

**Validation**
- Review text cannot be empty
- Product must exist to receive reviews
- Raises `ProductNotFoundError` for invalid products

---

### 6. Inventory Management

**Real-Time Tracking**
- Inventory automatically decremented on order placement
- Out-of-stock detection prevents overselling
- Admin can update stock levels

**Stock Validation**
- Checks availability before order placement
- Raises `OutOfStockError` with detailed message
- Shows available vs. requested quantities

**Inventory Reports**
- Admin dashboard shows out-of-stock products
- Alerts for low inventory items
- Total inventory value calculation

---

### 7. Order Tracking

**Order Status Workflow**
```
Placed → Shipped → Delivered
```

**Customer View**
- View all past orders sorted by date
- See order details: items, quantities, prices, tax, total
- Track current order status
- View shipping address and state

**Admin View**
- View all customer orders system-wide
- Update order status with single click
- Filter and search orders
- Export order data for reporting

---

### 8. Reports & Analytics (Admin Only)

**Business Metrics**
- **Total Revenue**: Sum of all completed orders
- **Total Orders**: Count of all orders placed
- **Best-Selling Products**: Top products by quantity sold (Min-Heap)
- **Out-of-Stock Products**: Products with zero inventory

**Data Structures Used**
- **Min-Heap**: Efficient top-N product identification (O(n log k))
- **Frequency Map**: Track product sales counts
- **HashMap**: Fast product lookups (O(1))

---

## 🛡️ Custom Exception Handling

### Exception Hierarchy

```
ECommerceError (Base)
├── AuthenticationError
├── OutOfStockError
├── ProductNotFoundError
└── InvalidInputError
```

### Exception Descriptions

| Exception | Purpose | Example Scenarios |
|-----------|---------|-------------------|
| `ECommerceError` | Base class for all app exceptions | Catch-all for e-commerce errors |
| `AuthenticationError` | Login/authentication failures | Invalid password, user not found |
| `OutOfStockError` | Insufficient inventory | Requested quantity exceeds stock |
| `ProductNotFoundError` | Product doesn't exist | Invalid product ID in operations |
| `InvalidInputError` | Invalid input data | Negative price, empty fields |

### Error Handling Strategy

**Backend (managers.py)**
- Validates all inputs at entry points
- Raises specific exceptions with descriptive messages
- No silent failures or `None` returns

**Frontend (gui.py)**
- Catches all custom exceptions
- Displays user-friendly error dialogs
- Prevents application crashes
- Guides users to correct issues

**Example Flow**
```python
# Backend
def add_product(self, product):
    if product.product_id in self.products:
        raise InvalidInputError("Product ID already exists.")
    self.products[product.product_id] = product

# Frontend
try:
    self.controller.product_manager.add_product(new_product)
    messagebox.showinfo("Success", "Product added successfully!")
except InvalidInputError as e:
    messagebox.showerror("Invalid Input", str(e))
```

---

## 🧪 Testing

### Test Suite

**File**: `test_exceptions.py`  
**Test Cases**: 16 comprehensive tests  
**Coverage**: All exception scenarios + successful operations

### Test Categories

#### 1. Product Validation Tests (4 tests)
- ✅ Empty product ID
- ✅ Empty product name
- ✅ Negative price
- ✅ Negative quantity

#### 2. Product Management Tests (5 tests)
- ✅ Duplicate product ID
- ✅ Get non-existent product
- ✅ Update non-existent product
- ✅ Delete non-existent product
- ✅ Add review to non-existent product

#### 3. Authentication Tests (3 tests)
- ✅ Empty username/password
- ✅ Non-existent user
- ✅ Invalid password

#### 4. Order Processing Tests (3 tests)
- ✅ Empty shipping address
- ✅ Out of stock error
- ✅ Order with non-existent product

#### 5. Success Tests (1 test)
- ✅ Complete order flow (add product → login → place order)

### Running Tests

```bash
cd /home/CSC530/ecommerce_project
python3 test_exceptions.py
```

**Expected Output**
```
Running E-Commerce Exception Handling Tests...
================================================

Test 1: Product with empty ID
✓ PASS: Correctly raised InvalidInputError

Test 2: Product with negative price
✓ PASS: Correctly raised InvalidInputError

[... 14 more tests ...]

================================================
All 16 tests passed successfully! ✓
================================================
```

---

## 🚀 Future Enhancements

### Planned Features

1. **Enhanced Tax System**
   - Local/county tax rates for more accuracy
   - Tax exemption support for eligible customers
   - International VAT/GST support

2. **Payment Integration**
   - Credit card processing
   - PayPal integration
   - Payment history tracking

3. **Advanced Search**
   - Full-text search across product descriptions
   - Price range filters
   - Sort by price, popularity, rating

4. **Notifications**
   - Email order confirmations
   - Shipping notifications
   - Low stock alerts for admins

5. **Data Persistence**
   - Database integration (SQLite/PostgreSQL)
   - Export orders to CSV/Excel
   - Backup and restore functionality

6. **Enhanced Analytics**
   - Sales trends over time
   - Customer purchase patterns
   - Revenue forecasting
   - Interactive charts and graphs

7. **User Experience**
   - Product images
   - Wishlist functionality
   - Product recommendations
   - Multi-language support

8. **Security**
   - Password hashing (bcrypt)
   - Session timeout
   - Role-based permissions granularity
   - Audit logging

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/HamedDiakite/ecommerce-order-inventory-manager.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/ecommerce-order-inventory-manager
   ```

3. **Make Your Changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   python3 test_exceptions.py
   ```

5. **Commit Your Changes**
   ```bash
   git commit -m "Add: This project demonstrates a basic e-commerce Inventory management and Shopping system using Data Structure approach."
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/HamedDiakite
   ```

7. **Submit a Pull Request**
   - Describe your changes in detail
   - Reference any related issues

### Code Style Guidelines

- Follow PEP 8 Python style guide
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Write comprehensive tests for new features

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Hamed Diakite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

**Hamed Diakite**

- **Course**: CSC 530-02 – Data Structures
- **Institution**: West Chester University
- **Department**: Computer Science
- **Instructor**: Dr. Bhuiyan
- **Project Date**: December 2025

### Contact

- 📧 Email: [hamedjdiakite@gmail.com](hamedjdiakite@gmail.com.com)
- 💼 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- 🐙 GitHub: [github.com/yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **Dr. Bhuiyan** - Course instructor and project guidance
- **West Chester University** - Computer Science Department
- **Python Community** - Excellent documentation and resources
- **Tkinter Documentation** - GUI framework reference

---

## 📚 Additional Documentation

For more detailed information, please refer to:

- **[COMPREHENSIVE_PROJECT_REPORT.md](COMPREHENSIVE_PROJECT_REPORT.md)** - Complete project documentation with architecture details
- **[CHANGES_STATE_TAX.md](CHANGES_STATE_TAX.md)** - State tax system implementation guide
- **[EXCEPTION_INTEGRATION_SUMMARY.md](EXCEPTION_INTEGRATION_SUMMARY.md)** - Exception handling integration details

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ by Hamed Diakite

</div>
