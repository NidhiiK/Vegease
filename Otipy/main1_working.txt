import os
import sqlite3
import pandas as pd
import xlsxwriter
from scraper import scrape_products
from notifier import send_notification
from utils import load_inserted_products, update_inserted_products
from datetime import datetime
from notification_formatter import format_notification_table


# Define a function to create an Excel file with multiple sheets
def create_excel_file(categories):
    workbook = xlsxwriter.Workbook('E:\VegEase\Vegease_newProject\Otipy\otipy_products.xlsx')
    
    for _, category_name in categories:
        workbook.add_worksheet(category_name)
    
    workbook.close()

# Define the main function to scrape, process, and store data
def main_function(url, category_name, existing_df):
    # Scrape the website
    otipy_product_cards = scrape_products(url)

    # Set up SQLite database connection
    conn = sqlite3.connect('E:\VegEase\Vegease_newProject\Otipy\otipy_products_database.db')
    c = conn.cursor()

    # Create products table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        product_name TEXT,
        original_price TEXT,
        discounted_price TEXT,
        discount TEXT,
        category TEXT,
        quantity TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Load the set of inserted products from the file
    inserted_products = load_inserted_products('E:\VegEase\Vegease_newProject\Otipy\otipy_inserted_products.txt')

    # Lists to keep track of new and updated products
    new_products = []
    updated_products = []

    # Process and store data
    for card in otipy_product_cards:
        product_name_elem = card.find("h3", class_="style_prod_name__QllSp")
        original_price_elem = card.find("span", class_="style_striked_price__4ghn5")
        discounted_price_elem = card.find("span", class_="style_selling_price__GaIsF")
        discount_elem = card.find("p", class_="style_final_price__FERLK")
        quantity_elem = card.find("span", class_="style_prod_qt__cXcqe")


        # Check if the elements are found, and get their text if found, or assign "N/A" if not found
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        original_price = original_price_elem.text.strip() if original_price_elem else "N/A"
        discounted_price = discounted_price_elem.text.strip() if discounted_price_elem else "N/A"
        discount = discount_elem.text.strip() if discount_elem else "N/A"
        quantity = quantity_elem.text.strip() if quantity_elem else "N/A"

        # Check if the product is new or updated
        if product_name not in inserted_products:
            new_products.append((product_name, original_price, discounted_price, discount))
            inserted_products.add(product_name)
        else:
            existing_product = c.execute("SELECT DISTINCT * FROM products WHERE product_name=?", (product_name,)).fetchone()
            if existing_product and existing_product[2] != discounted_price:
                updated_products.append((product_name, original_price, discounted_price, discount))
        # Update or insert the product details in the database
        c.execute('''INSERT OR REPLACE INTO products (product_name, original_price, discounted_price, discount, quantity, category) VALUES (?,?,?,?,?,?)''',
                  (product_name, original_price, discounted_price, discount, quantity, category_name))
        
        # ...

        # Remove duplicates based on product_name
        # c.execute('''DELETE FROM products WHERE rowid NOT IN (
        # SELECT MIN(rowid) 
        # FROM products 
        # GROUP BY product_name
        # )''')


    # Commit changes and close database connection
    conn.commit()
    conn.close()

    # Update the inserted products file
    update_inserted_products('E:\VegEase\Vegease_newProject\Otipy\otipy_inserted_products.txt', inserted_products)

    return new_products, updated_products

if __name__ == "__main__":
    categories = [
        ('https://www.otipy.com/category/vegetables-1', 'Vegetables'),
        ('https://www.otipy.com/category/fruits-2', 'Fruits'),
    ]

    # Create Excel file with sheets if it doesn't exist
    if not os.path.isfile('E:\VegEase\Vegease_newProject\Otipy\otipy_products.xlsx'):
        create_excel_file(categories)

    all_new_products = {}
    all_updated_products = {}
    existing_df = pd.DataFrame()  # Initialize an empty DataFrame to store existing data

    for url, category in categories:
        new_category_products, updated_category_products = main_function(url, category, existing_df)
        all_new_products[category] = new_category_products
        all_updated_products[category] = updated_category_products
    
    # Concatenate the existing DataFrame with new data
    for category in categories:
        category_name = category[1]
        conn = sqlite3.connect('E:\VegEase\Vegease_newProject\Otipy\otipy_products_database.db')
        df = pd.read_sql_query(f"SELECT * FROM products WHERE category='{category_name}'", conn)
        conn.close()
        existing_df = pd.concat([existing_df, df], ignore_index=True)
     
        # Remove duplicates from the combined DataFrame
        existing_df.drop_duplicates(subset=["product_name"], keep="last", inplace=True)    
        
    # Update Excel file and sheets
    with pd.ExcelWriter('E:\VegEase\Vegease_newProject\Otipy\otipy_products.xlsx', engine='xlsxwriter') as writer:
        for category in categories:
            category_name = category[1]
            df_category = existing_df[existing_df["category"] == category_name]
            df_category.to_excel(writer, sheet_name=category_name, index=False)
            
    # Prepare notification messages for new and updated products
    new_products_notification_text = "\n".join([f"Category: {category}\n{format_notification_table(products)}" for category, products in all_new_products.items() if products])
    updated_products_notification_text = "\n".join([f"Category: {category}\n{format_notification_table(products)}" for category, products in all_updated_products.items() if products])

    # Send notifications for new and updated products
    if new_products_notification_text:
        send_notification("New Products Alert", f"New products added:\n{new_products_notification_text}\nCheck them out!", 'kdhini2807@gmail.com')

    if updated_products_notification_text:
        send_notification("Price Changes Alert", f"Price changes detected:\n{updated_products_notification_text}\nTime to grab a deal!", 'kdhini2807@gmail.com')


