import sqlite3

# Step 1: Create the SQLite database for price records
def create_price_records_database():
    conn = sqlite3.connect('E:\VegEase\Vegease\Otipy\otipy_price_records.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS price_records (
        product_name TEXT,
        original_price REAL,
        discounted_price REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()

# Step 2: Create a function to update price records in the database
def update_price_records(product_name, original_price, discounted_price):
    conn = sqlite3.connect('E:\VegEase\Vegease\Otipy\otipy_price_records.db')
    c = conn.cursor()
    c.execute('''INSERT INTO price_records (product_name, original_price, discounted_price) VALUES (?, ?, ?)''',
              (product_name, original_price, discounted_price))
    conn.commit()
    conn.close()

# Step 3: Create a function to check for price changes and send notifications
def check_for_price_changes():
    conn = sqlite3.connect('E:\VegEase\Vegease\Otipy\otipy_price_records.db')
    c = conn.cursor()
    
    # Get the latest price records for each product
    c.execute('''
        SELECT product_name, original_price, discounted_price 
        FROM price_records 
        WHERE timestamp = (SELECT MAX(timestamp) FROM price_records WHERE product_name = product_name)''')
    
    price_records = c.fetchall()
    conn.close()
    
    for product_name, original_price, discounted_price in price_records:
        # Check for a price change
        if original_price != discounted_price:
            # Calculate discount percentage
            discount_percentage = ((original_price - discounted_price) / original_price) * 100
            
            # Send a notification
            send_price_change_notification(product_name, original_price, discounted_price, discount_percentage)

# Implement your notification sending logic here
def send_price_change_notification(product_name, original_price, discounted_price, discount_percentage):
    pass

