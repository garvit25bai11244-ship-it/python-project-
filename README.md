PROJECT TITLE :-   KABRAJI --- BUILDING MATERIAL , PAINTS AND SANITARY STORE.

OVERVIEW OF PROJECT :- The KABRAJI Shop Management System is a desktop application developed using Python's Tkinter library. It provides a complete solution for managing a building materials and supplies shop, covering inventory, customer database, sales/billing (invoicing), order tracking, and sales reporting.

Features:-
1.Product Management: Add, update, and delete products with details like ID, name, category (Paints, Sanitary, Building Materials), price, stock quantity, and unit.
2.Customer Database: Maintain a record of customers including name, phone, email, and address.
3. Sales & Invoicing:
4. Point-of-Sale (POS) interface to select a customer and add multiple items to a cart.
5.Supports quantity and percentage-based item discounts.
6. Automatic calculation of Subtotal, Discount, GST (18%), and Total Amount.
7. Generates a detailed, well-formatted text-based invoice file for each sale.
8.Automatically updates product stock upon invoice generation.

Technologies/Tools Used

1.Language: Python 3.x

2.GUI Framework: tkinter (Standard Python library)
datetime: For timestamping sales and reports.

3.os: For file path operations.

4.datetime: For timestamping sales and reports.

5.os: For file path operations.

datetime: For timestamping sales and reports.

Steps to Install & Run the Project:-
1.Prerequisites: Ensure you have Python 3.x installed on your system.

2.Save the Code: Save the provided Python code into a file named kabraji.py.

3.Run from Terminal: Open your command line or terminal, navigate to the directory where you saved the file, and execute the script.
Instructions for Testing
Follow these steps to test the main functionalities of the system:

1. Products Tab (Inventory)
Navigate to the Products tab.

Test Default Products: Verify the pre-loaded products (Paints, Sanitary, Building Materials) are visible in the table.

Add Product: Enter a new Product ID (e.g., P0001), Name, select a Category, set a Price, Stock Quantity, and Unit. Click "Add Product".

Update Product: Select an item from the table (its details will populate the fields), change the Stock Quantity, and click "Update Product".

Delete Product: Select an item and click "Delete Product".

2. Customers Tab
Navigate to the Customers tab.

Add Customer: Enter a Customer ID (e.g., CUST001), Name, Phone, and optionally Email and Address. Click "Add Customer".

Delete Customer: Select a customer from the table and click "Delete Customer".

3. Sales & Billing Tab
Navigate to the Sales & Billing tab.

Select Customer: Select a customer you created from the "Customer Details" dropdown combo box.

Add to Cart: Select a product from the "Add Items" dropdown, enter a Quantity (ensure it's less than the current stock), and an optional Discount (%). Click "Add to Cart".

Test Stock Check: Try to enter a quantity higher than the available stock to verify the error message.

Review Summary: Check the INVOICE SUMMARY on the right to ensure the Subtotal, Discount, GST (18%), and TOTAL are calculated correctly.

Generate Invoice: Click "Generate Invoice". This will:

Create a new order.

Deduct the sold quantity from the product stock.

Open a new window displaying the invoice text.

Save the invoice as a text file (e.g., invoice_ORD00001.txt).

Clear the cart.

4. Orders and Reports Tabs
Navigate to the Orders tab. Verify the new order generated in the Sales tab is listed with the status Pending. Select the order and click "Mark as Completed".

<img width="1802" height="932" alt="Screenshot (158)" src="https://github.com/user-attachments/assets/1b500a6a-7338-461f-ada1-e314ff5778ea" />
<img width="1920" height="1080" alt="Screenshot (159)" src="https://github.com/user-attachments/assets/b233bb4c-e042-4e73-941d-c2dfb3871977" />
<img width="1920" height="1080" alt="Screenshot (160)" src="https://github.com/user-attachments/assets/47c6a045-dbaf-474e-85a6-5854ec79de29" />
<img width="1920" height="1080" alt="Screenshot (161)" src="https://github.com/user-attachments/assets/b878a1e8-3aa6-4d2a-a166-04fd1453f014" />
<img width="1920" height="1080" alt="Screenshot (162)" src="https://github.com/user-attachments/assets/f4b653eb-6b36-43f4-9151-c011f2ba8f13" />
<img width="1920" height="1080" alt="Screenshot (163)" src="https://github.com/user-attachments/assets/36ade3a0-df5e-407c-bb81-ab935d5d5a3d" />
<img width="1920" height="1080" alt="Screenshot (164)" src="https://github.com/user-attachments/assets/872889f5-82a2-4787-9485-ba30c82efe31" />
<img width="1920" height="1080" alt="Screenshot (165)" src="https://github.com/user-attachments/assets/8c2c3594-a206-4447-ac99-2ba58d2959c2" />



