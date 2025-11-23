import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
from collections import defaultdict

class KabrajiShopSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("KABRAJI - Building Dreams, One Product at a Time")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a237e")
        
        # Data storage
        self.products = {}
        self.customers = {}
        self.orders = []
        self.sales_history = []
        
        self.load_data()
        self.initialize_default_products()
        
        # Header
        self.create_header()
        
        # Main notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_products_tab()
        self.create_customers_tab()
        self.create_sales_tab()
        self.create_orders_tab()
        self.create_reports_tab()
        
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg="#1a237e", height=80)
        header_frame.pack(fill='x', side='top')
        
        # Shop name and tagline
        tk.Label(header_frame, text="🏗️ KABRAJI", 
                font=("Arial", 28, "bold"), bg="#1a237e", fg="white").pack(pady=5)
        tk.Label(header_frame, text="Building Dreams, One Product at a Time | Quality Paints, Sanitary & Building Materials", 
                font=("Arial", 11, "italic"), bg="#1a237e", fg="#ffd700").pack()
    
    def initialize_default_products(self):
        """Add default products if none exist"""
        if not self.products:
            default_products = [
                # Paints
                {"name": "Asian Paints Royale", "category": "Paints", "price": 450.0, "stock": 50, "unit": "Liter"},
                {"name": "Berger Weather Coat", "category": "Paints", "price": 420.0, "stock": 40, "unit": "Liter"},
                {"name": "Nerolac Excel", "category": "Paints", "price": 380.0, "stock": 60, "unit": "Liter"},
                {"name": "Dulux Premium", "category": "Paints", "price": 500.0, "stock": 30, "unit": "Liter"},
                {"name": "Paint Primer", "category": "Paints", "price": 250.0, "stock": 45, "unit": "Liter"},
                
                # Sanitary
                {"name": "Hindware Toilet Seat", "category": "Sanitary", "price": 3500.0, "stock": 20, "unit": "Piece"},
                {"name": "Jaquar Basin Tap", "category": "Sanitary", "price": 1200.0, "stock": 35, "unit": "Piece"},
                {"name": "Cera Wash Basin", "category": "Sanitary", "price": 2800.0, "stock": 15, "unit": "Piece"},
                {"name": "Parryware Commode", "category": "Sanitary", "price": 4500.0, "stock": 12, "unit": "Piece"},
                {"name": "Shower Head Premium", "category": "Sanitary", "price": 800.0, "stock": 40, "unit": "Piece"},
                
                # Building Materials
                {"name": "Cement - UltraTech", "category": "Building Materials", "price": 380.0, "stock": 200, "unit": "Bag"},
                {"name": "Cement - ACC", "category": "Building Materials", "price": 375.0, "stock": 180, "unit": "Bag"},
                {"name": "TMT Steel Bars 8mm", "category": "Building Materials", "price": 55.0, "stock": 500, "unit": "Kg"},
                {"name": "TMT Steel Bars 12mm", "category": "Building Materials", "price": 54.0, "stock": 600, "unit": "Kg"},
                {"name": "Bricks - Red Clay", "category": "Building Materials", "price": 8.0, "stock": 5000, "unit": "Piece"},
                {"name": "Sand - River", "category": "Building Materials", "price": 1500.0, "stock": 100, "unit": "Ton"},
                {"name": "Gravel/Aggregate", "category": "Building Materials", "price": 1200.0, "stock": 80, "unit": "Ton"},
                {"name": "PVC Pipes 1 inch", "category": "Building Materials", "price": 45.0, "stock": 150, "unit": "Meter"},
                {"name": "PVC Pipes 2 inch", "category": "Building Materials", "price": 80.0, "stock": 120, "unit": "Meter"},
                {"name": "Electrical Wires", "category": "Building Materials", "price": 25.0, "stock": 300, "unit": "Meter"},
            ]
            
            for idx, prod in enumerate(default_products, 1):
                prod_id = f"PROD{idx:04d}"
                self.products[prod_id] = prod
            
            self.save_data()
    
    def create_dashboard_tab(self):
        """Dashboard with key metrics"""
        dash_frame = ttk.Frame(self.notebook)
        self.notebook.add(dash_frame, text="📊 Dashboard")
        
        # Title
        title = tk.Label(dash_frame, text="Business Overview", 
                        font=("Arial", 18, "bold"), bg="#e3f2fd")
        title.pack(fill='x', pady=10)
        
        # Metrics frame
        metrics_frame = tk.Frame(dash_frame, bg="white")
        metrics_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create metric cards
        cards_frame = tk.Frame(metrics_frame, bg="white")
        cards_frame.pack(pady=20)
        
        # Total Products
        self.create_metric_card(cards_frame, "Total Products", 
                               len(self.products), "#4CAF50", 0, 0)
        
        # Total Customers
        self.create_metric_card(cards_frame, "Total Customers", 
                               len(self.customers), "#2196F3", 0, 1)
        
        # Total Orders
        self.create_metric_card(cards_frame, "Total Orders", 
                               len(self.orders), "#FF9800", 0, 2)
        
        # Total Revenue
        total_revenue = sum(sale['total'] for sale in self.sales_history)
        self.create_metric_card(cards_frame, "Total Revenue", 
                               f"₹{total_revenue:,.2f}", "#9C27B0", 1, 0)
        
        # Low Stock Items
        low_stock = sum(1 for p in self.products.values() if p['stock'] < 10)
        self.create_metric_card(cards_frame, "Low Stock Items", 
                               low_stock, "#f44336", 1, 1)
        
        # Pending Orders
        pending = sum(1 for o in self.orders if o['status'] == 'Pending')
        self.create_metric_card(cards_frame, "Pending Orders", 
                               pending, "#FF5722", 1, 2)
        
        # Refresh button
        refresh_btn = tk.Button(metrics_frame, text="🔄 Refresh Dashboard", 
                               command=self.refresh_dashboard,
                               bg="#1a237e", fg="white", font=("Arial", 12, "bold"),
                               padx=20, pady=10)
        refresh_btn.pack(pady=20)
    
    def create_metric_card(self, parent, title, value, color, row, col):
        """Create a metric display card"""
        card = tk.Frame(parent, bg=color, relief='raised', bd=3, width=250, height=120)
        card.grid(row=row, column=col, padx=15, pady=15)
        card.grid_propagate(False)
        
        tk.Label(card, text=title, font=("Arial", 12, "bold"), 
                bg=color, fg="white").pack(pady=10)
        tk.Label(card, text=str(value), font=("Arial", 20, "bold"), 
                bg=color, fg="white").pack(pady=5)
    
    def refresh_dashboard(self):
        """Refresh dashboard metrics"""
        self.notebook.select(0)
        self.create_dashboard_tab()
        messagebox.showinfo("Success", "Dashboard refreshed!")
    
    def create_products_tab(self):
        """Products inventory management"""
        prod_frame = ttk.Frame(self.notebook)
        self.notebook.add(prod_frame, text="📦 Products")
        
        # Title
        title = tk.Label(prod_frame, text="Product Inventory Management", 
                        font=("Arial", 16, "bold"), bg="#e8f5e9")
        title.pack(fill='x', pady=10)
        
        # Input frame
        input_frame = tk.LabelFrame(prod_frame, text="Add/Update Product", 
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Product fields
        fields_frame = tk.Frame(input_frame, bg="white")
        fields_frame.pack()
        
        tk.Label(fields_frame, text="Product ID:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.prod_id_entry = tk.Entry(fields_frame, width=20, font=("Arial", 10))
        self.prod_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Product Name:", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.prod_name_entry = tk.Entry(fields_frame, width=25, font=("Arial", 10))
        self.prod_name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Category:", font=("Arial", 10), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.prod_cat_var = tk.StringVar()
        self.prod_cat_combo = ttk.Combobox(fields_frame, textvariable=self.prod_cat_var, 
                                          values=["Paints", "Sanitary", "Building Materials"],
                                          width=18, font=("Arial", 10))
        self.prod_cat_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Price (₹):", font=("Arial", 10), bg="white").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.prod_price_entry = tk.Entry(fields_frame, width=25, font=("Arial", 10))
        self.prod_price_entry.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Stock Quantity:", font=("Arial", 10), bg="white").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.prod_stock_entry = tk.Entry(fields_frame, width=20, font=("Arial", 10))
        self.prod_stock_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Unit:", font=("Arial", 10), bg="white").grid(row=2, column=2, padx=5, pady=5, sticky='w')
        self.prod_unit_var = tk.StringVar()
        self.prod_unit_combo = ttk.Combobox(fields_frame, textvariable=self.prod_unit_var,
                                           values=["Piece", "Liter", "Kg", "Meter", "Bag", "Ton"],
                                           width=23, font=("Arial", 10))
        self.prod_unit_combo.grid(row=2, column=3, padx=5, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Product", command=self.add_product,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Product", command=self.update_product,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Product", command=self.delete_product,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Fields", command=self.clear_product_fields,
                 bg="#607D8B", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        
        # Products table
        table_frame = tk.Frame(prod_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(table_frame, text="Product List", font=("Arial", 12, "bold"), bg="white").pack(anchor='w', pady=5)
        
        # Treeview
        tree_scroll_y = tk.Scrollbar(table_frame)
        tree_scroll_y.pack(side='right', fill='y')
        
        tree_scroll_x = tk.Scrollbar(table_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        self.products_tree = ttk.Treeview(table_frame, 
                                         columns=("ID", "Name", "Category", "Price", "Stock", "Unit"),
                                         show='headings',
                                         yscrollcommand=tree_scroll_y.set,
                                         xscrollcommand=tree_scroll_x.set,
                                         height=15)
        
        tree_scroll_y.config(command=self.products_tree.yview)
        tree_scroll_x.config(command=self.products_tree.xview)
        
        # Configure columns
        self.products_tree.heading("ID", text="Product ID")
        self.products_tree.heading("Name", text="Product Name")
        self.products_tree.heading("Category", text="Category")
        self.products_tree.heading("Price", text="Price (₹)")
        self.products_tree.heading("Stock", text="Stock")
        self.products_tree.heading("Unit", text="Unit")
        
        self.products_tree.column("ID", width=100)
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Category", width=150)
        self.products_tree.column("Price", width=100)
        self.products_tree.column("Stock", width=100)
        self.products_tree.column("Unit", width=80)
        
        self.products_tree.pack(fill='both', expand=True)
        self.products_tree.bind('<ButtonRelease-1>', self.select_product)
        
        self.refresh_products_table()
    
    def create_customers_tab(self):
        """Customer database management"""
        cust_frame = ttk.Frame(self.notebook)
        self.notebook.add(cust_frame, text="👥 Customers")
        
        # Title
        title = tk.Label(cust_frame, text="Customer Database", 
                        font=("Arial", 16, "bold"), bg="#e1f5fe")
        title.pack(fill='x', pady=10)
        
        # Input frame
        input_frame = tk.LabelFrame(cust_frame, text="Add Customer", 
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        fields_frame = tk.Frame(input_frame, bg="white")
        fields_frame.pack()
        
        tk.Label(fields_frame, text="Customer ID:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cust_id_entry = tk.Entry(fields_frame, width=20, font=("Arial", 10))
        self.cust_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Name:", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.cust_name_entry = tk.Entry(fields_frame, width=25, font=("Arial", 10))
        self.cust_name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Phone:", font=("Arial", 10), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.cust_phone_entry = tk.Entry(fields_frame, width=20, font=("Arial", 10))
        self.cust_phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Email:", font=("Arial", 10), bg="white").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.cust_email_entry = tk.Entry(fields_frame, width=25, font=("Arial", 10))
        self.cust_email_entry.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Address:", font=("Arial", 10), bg="white").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.cust_address_entry = tk.Entry(fields_frame, width=50, font=("Arial", 10))
        self.cust_address_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Customer", command=self.add_customer,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Customer", command=self.delete_customer,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        
        # Customers table
        table_frame = tk.Frame(cust_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(table_frame, text="Customer List", font=("Arial", 12, "bold"), bg="white").pack(anchor='w', pady=5)
        
        tree_scroll = tk.Scrollbar(table_frame)
        tree_scroll.pack(side='right', fill='y')
        
        self.customers_tree = ttk.Treeview(table_frame,
                                          columns=("ID", "Name", "Phone", "Email", "Address"),
                                          show='headings',
                                          yscrollcommand=tree_scroll.set,
                                          height=15)
        
        tree_scroll.config(command=self.customers_tree.yview)
        
        self.customers_tree.heading("ID", text="Customer ID")
        self.customers_tree.heading("Name", text="Name")
        self.customers_tree.heading("Phone", text="Phone")
        self.customers_tree.heading("Email", text="Email")
        self.customers_tree.heading("Address", text="Address")
        
        self.customers_tree.column("ID", width=100)
        self.customers_tree.column("Name", width=200)
        self.customers_tree.column("Phone", width=150)
        self.customers_tree.column("Email", width=200)
        self.customers_tree.column("Address", width=300)
        
        self.customers_tree.pack(fill='both', expand=True)
        
        self.refresh_customers_table()
    
    def create_sales_tab(self):
        """Sales and billing system"""
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="💰 Sales & Billing")
        
        # Title
        title = tk.Label(sales_frame, text="Create Invoice", 
                        font=("Arial", 16, "bold"), bg="#fff3e0")
        title.pack(fill='x', pady=10)
        
        # Main container
        main_container = tk.Frame(sales_frame, bg="white")
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left side - Customer and items
        left_frame = tk.Frame(main_container, bg="white")
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Customer selection
        cust_frame = tk.LabelFrame(left_frame, text="Customer Details", 
                                  font=("Arial", 11, "bold"), bg="white")
        cust_frame.pack(fill='x', pady=10)
        
        tk.Label(cust_frame, text="Customer:", font=("Arial", 10), bg="white").pack(side='left', padx=5)
        self.sale_cust_var = tk.StringVar()
        self.sale_cust_combo = ttk.Combobox(cust_frame, textvariable=self.sale_cust_var,
                                           width=30, font=("Arial", 10))
        self.sale_cust_combo.pack(side='left', padx=5, pady=5)
        self.refresh_customer_combo()
        
        # Add items
        item_frame = tk.LabelFrame(left_frame, text="Add Items", 
                                  font=("Arial", 11, "bold"), bg="white")
        item_frame.pack(fill='x', pady=10)
        
        tk.Label(item_frame, text="Product:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.sale_prod_var = tk.StringVar()
        self.sale_prod_combo = ttk.Combobox(item_frame, textvariable=self.sale_prod_var,
                                           width=30, font=("Arial", 10))
        self.sale_prod_combo.grid(row=0, column=1, padx=5, pady=5)
        self.refresh_product_combo()
        
        tk.Label(item_frame, text="Quantity:", font=("Arial", 10), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.sale_qty_entry = tk.Entry(item_frame, width=32, font=("Arial", 10))
        self.sale_qty_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(item_frame, text="Discount (%):", font=("Arial", 10), bg="white").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.sale_discount_entry = tk.Entry(item_frame, width=32, font=("Arial", 10))
        self.sale_discount_entry.insert(0, "0")
        self.sale_discount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(item_frame, text="Add to Cart", command=self.add_to_cart,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Cart items
        cart_frame = tk.LabelFrame(left_frame, text="Cart Items", 
                                  font=("Arial", 11, "bold"), bg="white")
        cart_frame.pack(fill='both', expand=True, pady=10)
        
        self.cart_tree = ttk.Treeview(cart_frame,
                                     columns=("Product", "Qty", "Price", "Discount", "Total"),
                                     show='headings',
                                     height=10)
        
        self.cart_tree.heading("Product", text="Product")
        self.cart_tree.heading("Qty", text="Quantity")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Discount", text="Discount %")
        self.cart_tree.heading("Total", text="Total")
        
        self.cart_tree.column("Product", width=200)
        self.cart_tree.column("Qty", width=80)
        self.cart_tree.column("Price", width=80)
        self.cart_tree.column("Discount", width=80)
        self.cart_tree.column("Total", width=100)
        
        self.cart_tree.pack(fill='both', expand=True)
        
        tk.Button(cart_frame, text="Remove Selected", command=self.remove_from_cart,
                 bg="#f44336", fg="white", font=("Arial", 9)).pack(pady=5)
        
        # Right side - Invoice summary
        right_frame = tk.Frame(main_container, bg="white", relief='solid', bd=2)
        right_frame.pack(side='right', fill='y', padx=10)
        
        tk.Label(right_frame, text="INVOICE SUMMARY", 
                font=("Arial", 14, "bold"), bg="#1a237e", fg="white").pack(fill='x', pady=5)
        
        summary_frame = tk.Frame(right_frame, bg="white")
        summary_frame.pack(padx=20, pady=20)
        
        self.subtotal_label = tk.Label(summary_frame, text="Subtotal: ₹0.00", 
                                      font=("Arial", 12), bg="white")
        self.subtotal_label.pack(anchor='w', pady=5)
        
        self.discount_label = tk.Label(summary_frame, text="Total Discount: ₹0.00", 
                                      font=("Arial", 12), bg="white")
        self.discount_label.pack(anchor='w', pady=5)
        
        self.tax_label = tk.Label(summary_frame, text="GST (18%): ₹0.00", 
                                 font=("Arial", 12), bg="white")
        self.tax_label.pack(anchor='w', pady=5)
        
        tk.Frame(summary_frame, height=2, bg="black").pack(fill='x', pady=10)
        
        self.total_label = tk.Label(summary_frame, text="TOTAL: ₹0.00", 
                                   font=("Arial", 16, "bold"), bg="white", fg="#4CAF50")
        self.total_label.pack(anchor='w', pady=10)
        
        tk.Button(right_frame, text="💳 Generate Invoice", command=self.generate_invoice,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10).pack(pady=10)
        
        tk.Button(right_frame, text="🗑️ Clear Cart", command=self.clear_cart,
                 bg="#FF9800", fg="white", font=("Arial", 11, "bold"), padx=20, pady=8).pack(pady=5)
        
        self.cart_items = []
    
    def create_orders_tab(self):
        """Order processing system"""
        order_frame = ttk.Frame(self.notebook)
        self.notebook.add(order_frame, text="📋 Orders")
        
        # Title
        title = tk.Label(order_frame, text="Order Management", 
                        font=("Arial", 16, "bold"), bg="#f3e5f5")
        title.pack(fill='x', pady=10)
        
        # Orders table
        table_frame = tk.Frame(order_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(table_frame, text="All Orders", font=("Arial", 12, "bold"), bg="white").pack(anchor='w', pady=5)
        
        tree_scroll = tk.Scrollbar(table_frame)
        tree_scroll.pack(side='right', fill='y')
        
        self.orders_tree = ttk.Treeview(table_frame,
                                       columns=("Order ID", "Customer", "Date", "Items", "Total", "Status"),
                                       show='headings',
                                       yscrollcommand=tree_scroll.set,
                                       height=20)
        
        tree_scroll.config(command=self.orders_tree.yview)
        
        self.orders_tree.heading("Order ID", text="Order ID")
        self.orders_tree.heading("Customer", text="Customer")
        self.orders_tree.heading("Date", text="Date")
        self.orders_tree.heading("Items", text="Items Count")
        self.orders_tree.heading("Total", text="Total Amount")
        self.orders_tree.heading("Status", text="Status")
        
        self.orders_tree.column("Order ID", width=120)
        self.orders_tree.column("Customer", width=200)
        self.orders_tree.column("Date", width=150)
        self.orders_tree.column("Items", width=100)
        self.orders_tree.column("Total", width=150)
        self.orders_tree.column("Status", width=120)
        
        self.orders_tree.pack(fill='both', expand=True)
        
        # Status update buttons
        btn_frame = tk.Frame(table_frame, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Mark as Completed", command=lambda: self.update_order_status("Completed"),
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Mark as Pending", command=lambda: self.update_order_status("Pending"),
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel Order", command=lambda: self.update_order_status("Cancelled"),
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side='left', padx=5)
        
        self.refresh_orders_table()
    
    def create_reports_tab(self):
        """Sales tracking and reporting"""
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="📈 Reports")
        
        # Title
        title = tk.Label(report_frame, text="Sales Reports & Analytics", 
                        font=("Arial", 16, "bold"), bg="#e8eaf6")
        title.pack(fill='x', pady=10)
        
        # Filters
        filter_frame = tk.LabelFrame(report_frame, text="Filter Reports", 
                                    font=("Arial", 11, "bold"), bg="white")
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(filter_frame, text="Date From:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.report_from_entry = tk.Entry(filter_frame, width=15, font=("Arial", 10))
        self.report_from_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.report_from_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Date To:", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.report_to_entry = tk.Entry(filter_frame, width=15, font=("Arial", 10))
        self.report_to_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.report_to_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(filter_frame, text="Generate Report", command=self.generate_report,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10, pady=5)
        
        # Report display
        display_frame = tk.Frame(report_frame, bg="white")
        display_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scroll = tk.Scrollbar(display_frame)
        scroll.pack(side='right', fill='y')
        
        self.report_text = tk.Text(display_frame, yscrollcommand=scroll.set, 
                                  font=("Courier", 10), wrap='word', height=25)
        self.report_text.pack(fill='both', expand=True)
        scroll.config(command=self.report_text.yview)
        
        # Export button
        tk.Button(report_frame, text="📥 Export Report", command=self.export_report,
                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=20, pady=8).pack(pady=10)
    
    # Product functions
    def add_product(self):
        prod_id = self.prod_id_entry.get().strip()
        name = self.prod_name_entry.get().strip()
        category = self.prod_cat_var.get()
        price = self.prod_price_entry.get().strip()
        stock = self.prod_stock_entry.get().strip()
        unit = self.prod_unit_var.get()
        
        if not all([prod_id, name, category, price, stock, unit]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value!")
            return
        
        if prod_id in self.products:
            messagebox.showerror("Error", "Product ID already exists!")
            return
        
        self.products[prod_id] = {
            'name': name,
            'category': category,
            'price': price,
            'stock': stock,
            'unit': unit
        }
        
        self.save_data()
        self.refresh_products_table()
        self.refresh_product_combo()
        self.clear_product_fields()
        messagebox.showinfo("Success", "Product added successfully!")
    
    def update_product(self):
        prod_id = self.prod_id_entry.get().strip()
        
        if prod_id not in self.products:
            messagebox.showerror("Error", "Product ID not found!")
            return
        
        name = self.prod_name_entry.get().strip()
        category = self.prod_cat_var.get()
        price = self.prod_price_entry.get().strip()
        stock = self.prod_stock_entry.get().strip()
        unit = self.prod_unit_var.get()
        
        if not all([name, category, price, stock, unit]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value!")
            return
        
        self.products[prod_id].update({
            'name': name,
            'category': category,
            'price': price,
            'stock': stock,
            'unit': unit
        })
        
        self.save_data()
        self.refresh_products_table()
        self.refresh_product_combo()
        messagebox.showinfo("Success", "Product updated successfully!")
    
    def delete_product(self):
        prod_id = self.prod_id_entry.get().strip()
        
        if prod_id not in self.products:
            messagebox.showerror("Error", "Product ID not found!")
            return
        
        if messagebox.askyesno("Confirm", f"Delete product {prod_id}?"):
            del self.products[prod_id]
            self.save_data()
            self.refresh_products_table()
            self.refresh_product_combo()
            self.clear_product_fields()
            messagebox.showinfo("Success", "Product deleted successfully!")
    
    def select_product(self, event):
        selected = self.products_tree.selection()
        if selected:
            values = self.products_tree.item(selected[0])['values']
            self.prod_id_entry.delete(0, 'end')
            self.prod_id_entry.insert(0, values[0])
            self.prod_name_entry.delete(0, 'end')
            self.prod_name_entry.insert(0, values[1])
            self.prod_cat_var.set(values[2])
            self.prod_price_entry.delete(0, 'end')
            self.prod_price_entry.insert(0, values[3])
            self.prod_stock_entry.delete(0, 'end')
            self.prod_stock_entry.insert(0, values[4])
            self.prod_unit_var.set(values[5])
    
    def clear_product_fields(self):
        self.prod_id_entry.delete(0, 'end')
        self.prod_name_entry.delete(0, 'end')
        self.prod_cat_var.set('')
        self.prod_price_entry.delete(0, 'end')
        self.prod_stock_entry.delete(0, 'end')
        self.prod_unit_var.set('')
    
    def refresh_products_table(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        for prod_id, prod in self.products.items():
            self.products_tree.insert('', 'end', values=(
                prod_id, prod['name'], prod['category'], 
                f"₹{prod['price']:.2f}", prod['stock'], prod['unit']
            ))
    
    def refresh_product_combo(self):
        products_list = [f"{pid} - {p['name']}" for pid, p in self.products.items()]
        self.sale_prod_combo['values'] = products_list
    
    # Customer functions
    def add_customer(self):
        cust_id = self.cust_id_entry.get().strip()
        name = self.cust_name_entry.get().strip()
        phone = self.cust_phone_entry.get().strip()
        email = self.cust_email_entry.get().strip()
        address = self.cust_address_entry.get().strip()
        
        if not all([cust_id, name, phone]):
            messagebox.showerror("Error", "Please fill required fields (ID, Name, Phone)!")
            return
        
        if cust_id in self.customers:
            messagebox.showerror("Error", "Customer ID already exists!")
            return
        
        self.customers[cust_id] = {
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        
        self.save_data()
        self.refresh_customers_table()
        self.refresh_customer_combo()
        
        self.cust_id_entry.delete(0, 'end')
        self.cust_name_entry.delete(0, 'end')
        self.cust_phone_entry.delete(0, 'end')
        self.cust_email_entry.delete(0, 'end')
        self.cust_address_entry.delete(0, 'end')
        
        messagebox.showinfo("Success", "Customer added successfully!")
    
    def delete_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a customer!")
            return
        
        cust_id = self.customers_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete customer {cust_id}?"):
            del self.customers[cust_id]
            self.save_data()
            self.refresh_customers_table()
            self.refresh_customer_combo()
            messagebox.showinfo("Success", "Customer deleted successfully!")
    
    def refresh_customers_table(self):
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        for cust_id, cust in self.customers.items():
            self.customers_tree.insert('', 'end', values=(
                cust_id, cust['name'], cust['phone'], 
                cust['email'], cust['address']
            ))
    
    def refresh_customer_combo(self):
        customers_list = [f"{cid} - {c['name']}" for cid, c in self.customers.items()]
        self.sale_cust_combo['values'] = customers_list
    
    # Sales functions
    def add_to_cart(self):
        prod_str = self.sale_prod_var.get()
        qty_str = self.sale_qty_entry.get().strip()
        discount_str = self.sale_discount_entry.get().strip()
        
        if not prod_str or not qty_str:
            messagebox.showerror("Error", "Please select product and enter quantity!")
            return
        
        try:
            qty = float(qty_str)
            discount = float(discount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or discount!")
            return
        
        prod_id = prod_str.split(' - ')[0]
        product = self.products[prod_id]
        
        if qty > product['stock']:
            messagebox.showerror("Error", f"Insufficient stock! Available: {product['stock']}")
            return
        
        price = product['price']
        subtotal = price * qty
        discount_amount = subtotal * (discount / 100)
        total = subtotal - discount_amount
        
        self.cart_items.append({
            'prod_id': prod_id,
            'name': product['name'],
            'qty': qty,
            'price': price,
            'discount': discount,
            'total': total
        })
        
        self.cart_tree.insert('', 'end', values=(
            product['name'], qty, f"₹{price:.2f}", f"{discount}%", f"₹{total:.2f}"
        ))
        
        self.update_invoice_summary()
        self.sale_qty_entry.delete(0, 'end')
        self.sale_discount_entry.delete(0, 'end')
        self.sale_discount_entry.insert(0, "0")
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to remove!")
            return
        
        index = self.cart_tree.index(selected[0])
        self.cart_items.pop(index)
        self.cart_tree.delete(selected[0])
        self.update_invoice_summary()
    
    def update_invoice_summary(self):
        subtotal = sum(item['qty'] * item['price'] for item in self.cart_items)
        total_discount = sum(item['qty'] * item['price'] * (item['discount'] / 100) for item in self.cart_items)
        after_discount = subtotal - total_discount
        tax = after_discount * 0.18
        total = after_discount + tax
        
        self.subtotal_label.config(text=f"Subtotal: ₹{subtotal:.2f}")
        self.discount_label.config(text=f"Total Discount: ₹{total_discount:.2f}")
        self.tax_label.config(text=f"GST (18%): ₹{tax:.2f}")
        self.total_label.config(text=f"TOTAL: ₹{total:.2f}")
    
    def clear_cart(self):
        if messagebox.askyesno("Confirm", "Clear all items from cart?"):
            self.cart_items = []
            for item in self.cart_tree.get_children():
                self.cart_tree.delete(item)
            self.update_invoice_summary()
    
    def generate_invoice(self):
        if not self.cart_items:
            messagebox.showerror("Error", "Cart is empty!")
            return
        
        cust_str = self.sale_cust_var.get()
        if not cust_str:
            messagebox.showerror("Error", "Please select a customer!")
            return
        
        cust_id = cust_str.split(' - ')[0]
        customer = self.customers[cust_id]
        
        # Calculate totals
        subtotal = sum(item['qty'] * item['price'] for item in self.cart_items)
        total_discount = sum(item['qty'] * item['price'] * (item['discount'] / 100) for item in self.cart_items)
        after_discount = subtotal - total_discount
        tax = after_discount * 0.18
        total = after_discount + tax
        
        # Generate order ID
        order_id = f"ORD{len(self.orders) + 1:05d}"
        
        # Create order
        order = {
            'order_id': order_id,
            'customer_id': cust_id,
            'customer_name': customer['name'],
            'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'items': self.cart_items.copy(),
            'subtotal': subtotal,
            'discount': total_discount,
            'tax': tax,
            'total': total,
            'status': 'Pending'
        }
        
        self.orders.append(order)
        self.sales_history.append({
            'date': datetime.now().strftime("%d/%m/%Y"),
            'order_id': order_id,
            'customer': customer['name'],
            'total': total
        })
        
        # Update stock
        for item in self.cart_items:
            self.products[item['prod_id']]['stock'] -= item['qty']
        
        self.save_data()
        self.refresh_products_table()
        self.refresh_orders_table()
        
        # Generate invoice text
        invoice_text = self.create_invoice_text(order, customer)
        
        # Save invoice
        filename = f"invoice_{order_id}.txt"
        with open(filename, 'w') as f:
            f.write(invoice_text)
        
        # Show invoice
        invoice_window = tk.Toplevel(self.root)
        invoice_window.title(f"Invoice - {order_id}")
        invoice_window.geometry("600x700")
        
        text_widget = tk.Text(invoice_window, font=("Courier", 9), wrap='word')
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', invoice_text)
        text_widget.config(state='disabled')
        
        tk.Button(invoice_window, text="Print/Save Invoice", 
                 command=lambda: messagebox.showinfo("Saved", f"Invoice saved as {filename}"),
                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=20, pady=10).pack(pady=10)
        
        # Clear cart
        self.cart_items = []
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        self.update_invoice_summary()
        
        messagebox.showinfo("Success", f"Invoice {order_id} generated successfully!")
    
    def create_invoice_text(self, order, customer):
        invoice = "=" * 70 + "\n"
        invoice += " " * 20 + "🏗️ KABRAJI\n"
        invoice += " " * 10 + "Building Dreams, One Product at a Time\n"
        invoice += " " * 8 + "Quality Paints, Sanitary & Building Materials\n"
        invoice += "=" * 70 + "\n\n"
        invoice += f"INVOICE NO: {order['order_id']}\n"
        invoice += f"DATE: {order['date']}\n"
        invoice += "-" * 70 + "\n\n"
        invoice += "CUSTOMER DETAILS:\n"
        invoice += f"Name: {customer['name']}\n"
        invoice += f"Phone: {customer['phone']}\n"
        invoice += f"Email: {customer['email']}\n"
        invoice += f"Address: {customer['address']}\n"
        invoice += "\n" + "=" * 70 + "\n"
        invoice += f"{'ITEM':<30} {'QTY':<8} {'PRICE':<12} {'DISC%':<8} {'TOTAL':<12}\n"
        invoice += "=" * 70 + "\n"
        
        for item in order['items']:
            invoice += f"{item['name']:<30} {item['qty']:<8.2f} ₹{item['price']:<10.2f} {item['discount']:<7.1f}% ₹{item['total']:<10.2f}\n"
        
        invoice += "=" * 70 + "\n"
        invoice += f"{'':<50} Subtotal: ₹{order['subtotal']:>12.2f}\n"
        invoice += f"{'':<50} Discount: ₹{order['discount']:>12.2f}\n"
        invoice += f"{'':<50} GST (18%): ₹{order['tax']:>12.2f}\n"
        invoice += "-" * 70 + "\n"
        invoice += f"{'':<50} TOTAL: ₹{order['total']:>12.2f}\n"
        invoice += "=" * 70 + "\n\n"
        invoice += "Thank you for your business!\n"
        invoice += "For queries: contact@kabraji.com | Phone: +91-XXXXXXXXXX\n"
        invoice += "=" * 70 + "\n"
        
        return invoice
    
    # Order functions
    def refresh_orders_table(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        for order in self.orders:
            self.orders_tree.insert('', 'end', values=(
                order['order_id'],
                order['customer_name'],
                order['date'],
                len(order['items']),
                f"₹{order['total']:.2f}",
                order['status']
            ))
    
    def update_order_status(self, status):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order!")
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        
        for order in self.orders:
            if order['order_id'] == order_id:
                order['status'] = status
                break
        
        self.save_data()
        self.refresh_orders_table()
        messagebox.showinfo("Success", f"Order status updated to {status}!")
    
    # Report functions
    def generate_report(self):
        self.report_text.delete('1.0', 'end')
        
        report = "=" * 80 + "\n"
        report += " " * 25 + "KABRAJI SALES REPORT\n"
        report += "=" * 80 + "\n\n"
        report += f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        # Total sales
        total_revenue = sum(sale['total'] for sale in self.sales_history)
        report += f"TOTAL REVENUE: ₹{total_revenue:,.2f}\n"
        report += f"TOTAL ORDERS: {len(self.orders)}\n"
        report += f"TOTAL CUSTOMERS: {len(self.customers)}\n\n"
        
        # Sales by category
        report += "-" * 80 + "\n"
        report += "SALES BY CATEGORY:\n"
        report += "-" * 80 + "\n"
        
        category_sales = defaultdict(float)
        for order in self.orders:
            for item in order['items']:
                prod = self.products[item['prod_id']]
                category_sales[prod['category']] += item['total']
        
        for category, amount in category_sales.items():
            report += f"{category:<30} ₹{amount:>15,.2f}\n"
        
        report += "\n"
        
        # Top products
        report += "-" * 80 + "\n"
        report += "TOP 10 SELLING PRODUCTS:\n"
        report += "-" * 80 + "\n"
        
        product_sales = defaultdict(lambda: {'qty': 0, 'revenue': 0})
        for order in self.orders:
            for item in order['items']:
                product_sales[item['name']]['qty'] += item['qty']
                product_sales[item['name']]['revenue'] += item['total']
        
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1]['revenue'], reverse=True)[:10]
        
        for i, (prod_name, data) in enumerate(sorted_products, 1):
            report += f"{i}. {prod_name:<40} Qty: {data['qty']:>8.2f}  Revenue: ₹{data['revenue']:>12,.2f}\n"
        
        report += "\n"
        
        # Low stock alert
        report += "-" * 80 + "\n"
        report += "LOW STOCK ALERT (Stock < 10):\n"
        report += "-" * 80 + "\n"
        
        low_stock_items = [(pid, p) for pid, p in self.products.items() if p['stock'] < 10]
        
        if low_stock_items:
            for prod_id, prod in low_stock_items:
                report += f"{prod_id} - {prod['name']:<40} Stock: {prod['stock']} {prod['unit']}\n"
        else:
            report += "No low stock items!\n"
        
        report += "\n" + "=" * 80 + "\n"
        
        self.report_text.insert('1.0', report)
    
    def export_report(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"kabraji_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(self.report_text.get('1.0', 'end'))
            messagebox.showinfo("Success", f"Report exported to {filename}!")
    
    # Data persistence
    def save_data(self):
        data = {
            'products': self.products,
            'customers': self.customers,
            'orders': self.orders,
            'sales_history': self.sales_history
        }
        with open('kabraji_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        if os.path.exists('kabraji_data.json'):
            try:
                with open('kabraji_data.json', 'r') as f:
                    data = json.load(f)
                    self.products = data.get('products', {})
                    self.customers = data.get('customers', {})
                    self.orders = data.get('orders', [])
                    self.sales_history = data.get('sales_history', [])
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = KabrajiShopSystem(root)
    root.mainloop()