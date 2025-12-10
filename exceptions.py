# exceptions.py

class ECommerceError(Exception):
    """Base class for all application-specific exceptions."""
    pass

class AuthenticationError(ECommerceError):
    """Raised when login fails or user permissions are invalid."""
    pass

class OutOfStockError(ECommerceError):
    """Raised when an order requests more quantity than available."""
    pass

class ProductNotFoundError(ECommerceError):
    """Raised when an operation is performed on a non-existent product."""
    pass

class InvalidInputError(ECommerceError):
    """Raised when input data (like price or quantity) is invalid."""
    pass