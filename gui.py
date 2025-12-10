# gui.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from models import ShoppingCart, Product
from exceptions import (
    ECommerceError,
    AuthenticationError,
    OutOfStockError,
    ProductNotFoundError,
    InvalidInputError
)
from state_tax_rates import STATE_DISPLAY_LIST, STATE_CODES, get_tax_rate, get_state_name

# --- NEW: Review Window ---
class ReviewWindow(tk.Toplevel):
    """A new window for viewing and adding product reviews."""
    def __init__(self, parent, controller, product):
        super().__init__(parent)
        self.controller = controller
        self.product = product
        
        self.title(f"Reviews for {self.product.name}")
        self.geometry("500x500")
        
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # --- View Reviews ---
        review_frame = ttk.LabelFrame(main_frame, text="Existing Reviews", padding=10)
        review_frame.pack(fill="both", expand=True, pady=5)
        
        self.review_list = scrolledtext.ScrolledText(review_frame, height=15, wrap=tk.WORD, state="disabled")
        self.review_list.pack(fill="both", expand=True)
        
        # --- Add Review ---
        add_frame = ttk.LabelFrame(main_frame, text="Write Your Review", padding=10)
        add_frame.pack(fill="x", pady=5)
        
        self.review_text = tk.Text(add_frame, height=5, wrap=tk.WORD)
        self.review_text.pack(fill="x", expand=True, pady=(0, 5))
        
        submit_btn = ttk.Button(add_frame, text="Submit Review", command=self.submit_review)
        submit_btn.pack(anchor="e")
        
        self.load_reviews()

    def load_reviews(self):
        self.review_list.config(state="normal")
        self.review_list.delete('1.0', tk.END)
        try:
            reviews = self.controller.product_manager.get_product_reviews(self.product.product_id)
            if not reviews:
                self.review_list.insert(tk.END, "No reviews for this product yet.")
            else:
                for username, text in reviews:
                    self.review_list.insert(tk.END, f"From: {username}\n", ("bold",))
                    self.review_list.insert(tk.END, f"{text}\n\n")
        except ProductNotFoundError as e:
            self.review_list.insert(tk.END, f"Error: {str(e)}")
        
        self.review_list.tag_config("bold", font=("Arial", 10, "bold"))
        self.review_list.config(state="disabled")

    def submit_review(self):
        review_text = self.review_text.get("1.0", tk.END).strip()
        if not review_text:
            messagebox.showwarning("Empty Review", "Please write a review before submitting.", parent=self)
            return
        
        try:
            username = self.controller.current_user.username
            self.controller.product_manager.add_review_to_product(self.product.product_id, username, review_text)
            
            messagebox.showinfo("Review Submitted", "Thank you for your review!", parent=self)
            self.review_text.delete("1.0", tk.END)
            self.load_reviews()
        except (ProductNotFoundError, InvalidInputError) as e:
            messagebox.showerror("Error", str(e), parent=self)


class Application(tk.Tk):
    """Main application window that manages different frames."""
    def __init__(self, user_manager, product_manager, order_manager):
        super().__init__()
        self.title("E-Commerce Order and Inventory Manager")
        self.geometry("1000x700")

        self.user_manager = user_manager
        self.product_manager = product_manager
        self.order_manager = order_manager
        self.current_user = None
        self.cart = None

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        login_frame = LoginFrame(self.container, self)
        self.frames[LoginFrame] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, FrameClass):
        if FrameClass == MainFrame:
            frame = MainFrame(self.container, self)
            self.frames[MainFrame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        frame = self.frames[FrameClass]
        frame.tkraise()

    def on_login_success(self, user):
        self.current_user = user
        self.cart = ShoppingCart(user.user_id)
        self.show_frame(MainFrame)

class LoginFrame(tk.Frame):
    """Login and registration screen."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = ttk.Frame(self, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Username", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Password", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(frame, text="Login", command=self.login).grid(row=2, column=1, sticky="e", pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            user = self.controller.user_manager.login(username, password)
            self.password_entry.delete(0, tk.END)
            self.controller.on_login_success(user)
        except AuthenticationError as e:
            messagebox.showerror("Login Failed", str(e))

class MainFrame(tk.Frame):
    """Main application interface, with role-specific tabs."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.discount_applied = False
        
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        if self.controller.current_user.role == 'admin':
            self.create_admin_ui(notebook)
        else:
            self.create_customer_ui(notebook)

        logout_frame = ttk.Frame(self)
        logout_frame.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Label(logout_frame, text=f"Logged in as: {self.controller.current_user.username} ({self.controller.current_user.role})").pack(side="left")
        ttk.Button(logout_frame, text="Logout", command=self.logout).pack(side="right")

    def logout(self):
        self.controller.current_user = None
        self.controller.cart = None
        self.controller.show_frame(LoginFrame)

    # --- ADMIN UI CREATION ---
    def create_admin_ui(self, notebook):
        product_tab = ttk.Frame(notebook)
        orders_tab = ttk.Frame(notebook)
        reports_tab = ttk.Frame(notebook)
        notebook.add(product_tab, text="Product Management")
        notebook.add(orders_tab, text="View All Orders")
        notebook.add(reports_tab, text="System Reports")
        self.setup_product_management_tab(product_tab)
        self.setup_admin_orders_tab(orders_tab)
        self.setup_reports_tab(reports_tab)

    # --- CUSTOMER UI CREATION ---
    def create_customer_ui(self, notebook):
        browse_tab = ttk.Frame(notebook)
        cart_tab = ttk.Frame(notebook)
        history_tab = ttk.Frame(notebook)
        notebook.add(browse_tab, text="Browse Products")
        notebook.add(cart_tab, text="Shopping Cart")
        notebook.add(history_tab, text="My Past Orders")
        self.setup_browse_products_tab(browse_tab)
        self.setup_cart_tab(cart_tab)
        self.setup_order_history_tab(history_tab)

    # --- ADMIN TAB IMPLEMENTATIONS ---
    def setup_product_management_tab(self, tab):
        # (Unchanged from previous version)
        form_frame = ttk.LabelFrame(tab, text="Add/Update Product", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)
        labels = ["ID", "Name", "Category", "Price", "Quantity"]
        self.product_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.product_entries[label.lower()] = entry
        form_frame.grid_columnconfigure(1, weight=1)
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Add Product", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Product", command=self.update_product).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Product", command=self.delete_product).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_product_form).pack(side="left", padx=5)
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)
        columns = ("id", "name", "category", "price", "quantity")
        self.product_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns: self.product_tree.heading(col, text=col.title())
        self.product_tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.product_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        self.product_tree.bind("<<TreeviewSelect>>", self.on_product_select)
        self.refresh_product_list()
        
    def setup_admin_orders_tab(self, tab):
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # UPDATED: Added State column
        columns = ("order_id", "customer_id", "total_price", "tax", "state", "address", "timestamp", "status")
        self.admin_orders_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.admin_orders_tree.heading(col, text=col.title())
            self.admin_orders_tree.column(col, width=120)
        self.admin_orders_tree.column("address", width=180)
        self.admin_orders_tree.column("state", width=60)
        self.admin_orders_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.admin_orders_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.admin_orders_tree.configure(yscrollcommand=scrollbar.set)
        
        status_frame = ttk.Frame(tab)
        status_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(status_frame, text="Update Status for Selected Order:").pack(side="left")
        self.order_status_var = tk.StringVar()
        status_menu = ttk.Combobox(status_frame, textvariable=self.order_status_var, values=["Placed", "Shipped", "Delivered"], state="readonly")
        status_menu.pack(side="left", padx=10)
        status_menu.set("Shipped")
        ttk.Button(status_frame, text="Update Status", command=self.update_order_status).pack(side="left")
        ttk.Button(status_frame, text="Refresh List", command=self.refresh_admin_orders_list).pack(side="left", padx=10)
        
        self.refresh_admin_orders_list()

    def setup_reports_tab(self, tab):
        # (Unchanged from previous version)
        report_frame = ttk.LabelFrame(tab, text="Summary Reports", padding=20)
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.total_revenue_label = ttk.Label(report_frame, text="Total Revenue: ", font=("Arial", 12))
        self.total_revenue_label.pack(anchor="w", pady=5)
        self.total_orders_label = ttk.Label(report_frame, text="Total Orders Placed: ", font=("Arial", 12))
        self.total_orders_label.pack(anchor="w", pady=5)
        self.most_ordered_label = ttk.Label(report_frame, text="Most Ordered Product: ", font=("Arial", 12))
        self.most_ordered_label.pack(anchor="w", pady=5)
        self.out_of_stock_label = ttk.Label(report_frame, text="Out of Stock Products:", font=("Arial", 12))
        self.out_of_stock_label.pack(anchor="w", pady=15)
        self.out_of_stock_listbox = tk.Listbox(report_frame, height=10)
        self.out_of_stock_listbox.pack(fill="x", anchor="w")
        ttk.Button(report_frame, text="Generate/Refresh Report", command=self.generate_reports).pack(pady=20)
        self.generate_reports()

    # --- CUSTOMER TAB IMPLEMENTATIONS ---
    def setup_browse_products_tab(self, tab):
        controls_frame = ttk.Frame(tab)
        controls_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(controls_frame, text="Search by Name:").pack(side="left", padx=(0, 5))
        self.search_entry = ttk.Entry(controls_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Search", command=self.customer_search_products).pack(side="left")
        ttk.Button(controls_frame, text="Sort by Price", command=self.sort_products_by_price).pack(side="left", padx=10)
        ttk.Button(controls_frame, text="Refresh / Show All", command=self.customer_refresh_product_list).pack(side="left")

        tree_frame = ttk.Frame(tab)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)
        columns = ("id", "name", "category", "price", "quantity")
        self.customer_product_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns: self.customer_product_tree.heading(col, text=col.title())
        self.customer_product_tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.customer_product_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.customer_product_tree.configure(yscrollcommand=scrollbar.set)
        
        # MODIFIED: Added Review Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Add Selected Item to Cart", command=self.add_to_cart).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="View/Add Reviews for Selected", command=self.open_review_window).pack(side="left")
        
        self.customer_refresh_product_list()

    def setup_cart_tab(self, tab):
        cart_frame = ttk.LabelFrame(tab, text="My Shopping Cart", padding=10)
        cart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("product_id", "name", "price", "quantity", "item_total")
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings")
        for col in columns: self.cart_tree.heading(col, text=col.title())
        self.cart_tree.pack(fill="both", expand=True)
        
        # --- UPDATED: State Selector ---
        state_frame = ttk.Frame(cart_frame)
        state_frame.pack(fill="x", pady=5, anchor="w")
        ttk.Label(state_frame, text="State:").pack(side="left", padx=(0, 5))
        self.state_combobox = ttk.Combobox(state_frame, values=STATE_DISPLAY_LIST, width=25, state="readonly")
        self.state_combobox.pack(side="left", padx=5)
        self.state_combobox.set("Select State")
        # Bind state selection to update tax calculation
        self.state_combobox.bind("<<ComboboxSelected>>", lambda e: self.refresh_cart_view())
        
        # State tax info label
        self.state_tax_label = ttk.Label(state_frame, text="", foreground="blue")
        self.state_tax_label.pack(side="left", padx=10)
        
        # --- UPDATED: Address Field ---
        address_frame = ttk.Frame(cart_frame)
        address_frame.pack(fill="x", pady=5, anchor="w")
        ttk.Label(address_frame, text="Shipping Address:").pack(side="left", padx=(0, 5))
        self.address_entry = ttk.Entry(address_frame, width=60)
        self.address_entry.pack(side="left", fill="x", expand=True)
        ttk.Label(address_frame, text="(Street, City, ZIP)", foreground="gray").pack(side="left", padx=5)
        
        discount_frame = ttk.Frame(cart_frame)
        discount_frame.pack(fill="x", pady=5, anchor="w")
        ttk.Label(discount_frame, text="Discount Code:").pack(side="left", padx=(0, 5))
        self.discount_entry = ttk.Entry(discount_frame, width=20)
        self.discount_entry.pack(side="left", padx=5)
        ttk.Button(discount_frame, text="Apply", command=self.apply_discount).pack(side="left")

        self.total_price_label = ttk.Label(cart_frame, text="Total: $0.00", font=("Arial", 14, "bold"), justify="left")
        self.total_price_label.pack(pady=10, anchor="w")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Place Order", command=self.place_order).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Remove Selected Item", command=self.remove_from_cart).pack(side="left", padx=10)
        
        tab.bind("<Visibility>", lambda e: self.refresh_cart_view())

    def setup_order_history_tab(self, tab):
        top_frame = ttk.Frame(tab)
        top_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(top_frame, text="Refresh Order Statuses", command=self.refresh_order_history).pack(anchor="e")

        history_frame = ttk.LabelFrame(tab, text="My Order History", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # UPDATED: Added State column
        columns = ("order_id", "total_price", "tax", "state", "address", "timestamp", "status")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        for col in columns:
            self.history_tree.heading(col, text=col.title())
            self.history_tree.column(col, width=120)
        self.history_tree.column("address", width=180)
        self.history_tree.column("state", width=60)
        self.history_tree.pack(fill="both", expand=True)
        
        tab.bind("<Visibility>", lambda e: self.refresh_order_history())
    
    # --- LOGIC METHODS (ADMIN) ---
    def refresh_product_list(self):
        self.product_tree.delete(*self.product_tree.get_children())
        for p in self.controller.product_manager.get_all_products():
            self.product_tree.insert("", "end", values=(p.product_id, p.name, p.category, f"{p.price:.2f}", p.quantity))

    def on_product_select(self, event):
        selected_item = self.product_tree.focus()
        if not selected_item: return
        values = self.product_tree.item(selected_item)['values']
        self.product_entries['id'].delete(0, tk.END); self.product_entries['id'].insert(0, values[0])
        self.product_entries['name'].delete(0, tk.END); self.product_entries['name'].insert(0, values[1])
        self.product_entries['category'].delete(0, tk.END); self.product_entries['category'].insert(0, values[2])
        self.product_entries['price'].delete(0, tk.END); self.product_entries['price'].insert(0, values[3])
        self.product_entries['quantity'].delete(0, tk.END); self.product_entries['quantity'].insert(0, values[4])

    def clear_product_form(self):
        for entry in self.product_entries.values(): entry.delete(0, tk.END)

    def validate_product_inputs(self):
        try:
            pid = self.product_entries['id'].get()
            name = self.product_entries['name'].get()
            price = float(self.product_entries['price'].get())
            quantity = int(self.product_entries['quantity'].get())
            if not all([pid, name]) or price < 0 or quantity < 0: raise ValueError
            return pid, name, self.product_entries['category'].get(), price, quantity
        except (ValueError, TypeError):
            messagebox.showerror("Validation Error", "Please enter valid data. Price/Quantity must be positive numbers.")
            return None

    def add_product(self):
        if not (data := self.validate_product_inputs()): return
        try:
            self.controller.product_manager.add_product(Product(*data))
            self.refresh_product_list(); self.clear_product_form()
            messagebox.showinfo("Success", f"Product '{data[1]}' added.")
        except (InvalidInputError, ECommerceError) as e: 
            messagebox.showerror("Error", str(e))

    def update_product(self):
        if not (data := self.validate_product_inputs()): return
        try:
            self.controller.product_manager.update_product(*data)
            self.refresh_product_list(); self.clear_product_form()
            messagebox.showinfo("Success", f"Product '{data[0]}' updated.")
        except (ProductNotFoundError, InvalidInputError) as e: 
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        pid = self.product_entries['id'].get()
        if not pid: 
            messagebox.showwarning("Selection Error", "Please select a product.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete product '{pid}'?"):
            try:
                self.controller.product_manager.delete_product(pid)
                self.refresh_product_list(); self.clear_product_form()
                messagebox.showinfo("Success", f"Product '{pid}' deleted.")
            except ProductNotFoundError as e: 
                messagebox.showerror("Error", str(e))
    
    def refresh_admin_orders_list(self):
        self.admin_orders_tree.delete(*self.admin_orders_tree.get_children())
        for o in self.controller.order_manager.get_all_orders():
            self.admin_orders_tree.insert("", "end", values=(
                o.order_id, o.customer_id, f"${o.total_price:.2f}", f"${o.tax:.2f}",
                o.state_code, o.address, o.timestamp.strftime('%Y-%m-%d %H:%M'), o.status
            ))

    def update_order_status(self):
        if not (sel := self.admin_orders_tree.focus()):
            messagebox.showwarning("Selection Error", "Please select an order.")
            return
        order_id = self.admin_orders_tree.item(sel)['values'][0]
        new_status = self.order_status_var.get()
        try:
            self.controller.order_manager.update_order_status(order_id, new_status)
            messagebox.showinfo("Success", f"Order {order_id} status updated.")
            self.refresh_admin_orders_list()
        except ProductNotFoundError as e: 
            messagebox.showerror("Error", str(e))
            
    def generate_reports(self):
        om = self.controller.order_manager; pm = self.controller.product_manager
        self.total_revenue_label.config(text=f"Total Revenue: ${om.get_total_revenue():.2f}")
        self.total_orders_label.config(text=f"Total Orders Placed: {om.get_total_orders_placed()}")
        self.most_ordered_label.config(text=f"Most Ordered Product: {om.get_most_frequently_ordered_product()}")
        self.out_of_stock_listbox.delete(0, tk.END)
        if not (out_of_stock := pm.get_out_of_stock_products()): self.out_of_stock_listbox.insert(tk.END, "None")
        else: [self.out_of_stock_listbox.insert(tk.END, f"{p.name} (ID: {p.product_id})") for p in out_of_stock]

    # --- LOGIC METHODS (CUSTOMER) ---
    def customer_refresh_product_list(self, products=None):
        self.customer_product_tree.delete(*self.customer_product_tree.get_children())
        product_list = products if products is not None else self.controller.product_manager.get_all_products()
        for p in product_list: self.customer_product_tree.insert("", "end", values=(p.product_id, p.name, p.category, f"{p.price:.2f}", p.quantity))

    def customer_search_products(self): self.customer_refresh_product_list(self.controller.product_manager.search_product_by_name(self.search_entry.get()))
            
    def sort_products_by_price(self): self.customer_refresh_product_list(self.controller.product_manager.get_products_sorted_by_price())

    def add_to_cart(self):
        if not (sel := self.customer_product_tree.focus()): 
            messagebox.showwarning("Selection Error", "Please select a product.")
            return
        try:
            product_id = self.customer_product_tree.item(sel)['values'][0]
            # Get product without raising exception (use dict access)
            product = self.controller.product_manager.products.get(product_id)
            if product and product.quantity > 0: 
                self.controller.cart.add_item(product)
                messagebox.showinfo("Cart", f"Added '{product.name}'.")
            else: 
                messagebox.showerror("Out of Stock", "Product unavailable.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # --- NEW: Opens the Review Window ---
    def open_review_window(self):
        if not (sel := self.customer_product_tree.focus()):
            messagebox.showwarning("Selection Error", "Please select a product to review.")
            return
        try:
            product_id = self.customer_product_tree.item(sel)['values'][0]
            # Get product without raising exception (use dict access)
            product = self.controller.product_manager.products.get(product_id)
            if product:
                ReviewWindow(self, self.controller, product)
            else:
                messagebox.showerror("Error", "Product not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def refresh_cart_view(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        subtotal = 0
        try:
            for pid, qty in self.controller.cart.items.items():
                # Use dict access to avoid raising exception
                p = self.controller.product_manager.products.get(pid)
                if p:
                    item_total = p.price * qty
                    subtotal += item_total
                    self.cart_tree.insert("", "end", values=(pid, p.name, f"{p.price:.2f}", qty, f"{item_total:.2f}"))
            
            # Calculate totals
            discount_amount = 0.0
            discount_text = ""
            if self.discount_applied:
                discount_amount = subtotal * 0.10
                discount_text = f"\nDiscount (10%): -${discount_amount:.2f}"
                
            discounted_subtotal = subtotal - discount_amount
            
            # Get selected state code
            state_selection = self.state_combobox.get()
            state_code = None
            tax_rate_pct = 0.0
            
            if state_selection and state_selection != "Select State":
                # Extract state code from selection (format: "AL - Alabama")
                state_code = state_selection.split(" - ")[0]
                tax_rate_pct = get_tax_rate(state_code) * 100
                
                # Update state tax info label
                self.state_tax_label.config(text=f"(Tax Rate: {tax_rate_pct:.2f}%)")
            else:
                self.state_tax_label.config(text="")
            
            # Calculate tax using state code
            try:
                if state_code:
                    tax, final_total = self.controller.order_manager.calculate_order_totals(discounted_subtotal, state_code)
                else:
                    tax = 0.0
                    final_total = discounted_subtotal
            except InvalidInputError:
                # Invalid state code, no tax
                tax = 0.0
                final_total = discounted_subtotal
            
            self.total_price_label.config(text=f"Subtotal: ${subtotal:.2f}"
                                               f"{discount_text}"
                                               f"\nTax: +${tax:.2f}"
                                               f"\nTotal: ${final_total:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh cart: {str(e)}")

    def remove_from_cart(self):
        if not (sel := self.cart_tree.focus()): messagebox.showwarning("Selection Error", "Please select an item."); return
        self.controller.cart.remove_item(self.cart_tree.item(sel)['values'][0]); self.refresh_cart_view()

    def apply_discount(self):
        code = self.discount_entry.get()
        if code == "DISCOUNT10":
            if not self.discount_applied:
                self.discount_applied = True
                messagebox.showinfo("Discount", "10% discount applied!")
                self.refresh_cart_view()
            else:
                messagebox.showwarning("Discount", "Discount already applied.")
        else:
            messagebox.showerror("Error", "Invalid discount code.")
        self.refresh_cart_view()

    # UPDATED: Handles state, address, tax, and final confirmation
    def place_order(self):
        if not self.controller.cart.items:
            messagebox.showerror("Empty Cart", "Your cart is empty.")
            return
        
        # Validate state selection
        state_selection = self.state_combobox.get()
        if not state_selection or state_selection == "Select State":
            messagebox.showerror("State Required", "Please select your state for tax calculation.")
            return
        
        # Extract state code from selection (format: "AL - Alabama")
        state_code = state_selection.split(" - ")[0]
        state_name = state_selection.split(" - ")[1]
        
        # Validate address
        address = self.address_entry.get().strip()
        if not address:
            messagebox.showerror("Address Required", "Please enter a shipping address.")
            return

        # --- Calculate final totals ---
        subtotal = 0
        try:
            for pid, qty in self.controller.cart.items.items():
                p = self.controller.product_manager.products.get(pid)
                if p:
                    subtotal += p.price * qty
            
            discounted_subtotal = subtotal * 0.90 if self.discount_applied else subtotal
            tax, final_total = self.controller.order_manager.calculate_order_totals(discounted_subtotal, state_code)
            
            # Get tax rate for display
            tax_rate_pct = get_tax_rate(state_code) * 100
            
            # --- Confirmation ---
            if not messagebox.askyesno("Confirm Order", 
                                       f"Please confirm your order:\n\n"
                                       f"Subtotal: ${discounted_subtotal:.2f}\n"
                                       f"Tax ({state_code} - {tax_rate_pct:.2f}%): ${tax:.2f}\n"
                                       f"Total: ${final_total:.2f}\n\n"
                                       f"Ship to:\n{address}\n{state_name}\n\n"
                                       "Place this order?"):
                return
                
            order = self.controller.order_manager.place_order(
                self.controller.cart, discounted_subtotal, tax, final_total, address, state_code
            )
            
            # --- Clear cart and fields ---
            self.controller.cart.clear()
            self.discount_applied = False
            self.discount_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            self.state_combobox.set("Select State")
            self.state_tax_label.config(text="")
            self.refresh_cart_view()
            self.customer_refresh_product_list()
            messagebox.showinfo("Order Placed", f"Order #{order.order_id} placed successfully!")
        except OutOfStockError as e:
            messagebox.showerror("Out of Stock", str(e))
        except ProductNotFoundError as e:
            messagebox.showerror("Product Not Found", str(e))
        except InvalidInputError as e:
            messagebox.showerror("Invalid Input", str(e))
        except ECommerceError as e:
            messagebox.showerror("Order Failed", str(e))
            
    def refresh_order_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        orders = self.controller.order_manager.get_orders_by_customer(self.controller.current_user.user_id)
        for o in sorted(orders, key=lambda o: o.timestamp, reverse=True):
            self.history_tree.insert("", "end", values=(
                o.order_id, f"${o.total_price:.2f}", f"${o.tax:.2f}",
                o.state_code, o.address, o.timestamp.strftime('%Y-%m-%d %H:%M'), o.status
            ))