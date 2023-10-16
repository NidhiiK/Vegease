import os
import sqlite3
import pandas as pd
import xlsxwriter
from scraper import scrape_products  # Import your BigBasket scraper function
from notifier import send_notification
from utils import load_inserted_products, update_inserted_products
from datetime import datetime
from notification_formatter import format_notification_table

# Define a function to create an Excel file with multiple sheets
def create_excel_file(categories):
    workbook = xlsxwriter.Workbook('E:\VegEase\Vegease\BigBasket\Bigbasket_products.xlsx')
    
    for _, category_name in categories:
        workbook.add_worksheet(category_name)
    
    workbook.close()

# Define the main function to scrape, process, and store data
def main_function(url, category_name, existing_df):
    # Scrape the website
    bigbasket_product_cards = scrape_products(url)  # Replace 'scrape_products' with your actual BigBasket scraper function name

    # Set up SQLite database connection
    conn = sqlite3.connect('E:\VegEase\Vegease\BigBasket\Bigbasket_products_database.db')
    c = conn.cursor()

    # Create products table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        product_name TEXT,
        original_price TEXT,
        discounted_price TEXT,
        discount TEXT,
        previous_price TEXT,
        category TEXT,
        quantity TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Load the set of inserted products from the file
    inserted_products = load_inserted_products('E:\VegEase\Vegease\BigBasket\Bigbasket_inserted_products.txt')

    # Lists to keep track of new and updated products
    new_products = []
    updated_products = []

    # Process and store data
    for card in bigbasket_product_cards:
        product_name_elem = card.find("h3", class_="text-base")
        original_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel2-sc-pldi2d-2 gJxZPQ hsCgvu")
        discounted_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi")
        discount_elem = card.find("span", class_="font-semibold lg:text-xs xl:text-sm leading-xxl xl:leading-md")
        quantity_elem = card.find("span", class_=["Label-sc-15v1nk5-0 PackChanger___StyledLabel-sc-newjpv-1 gJxZPQ cWbtUx", "Label-sc-15v1nk5-0 gJxZPQ truncate" ])

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

        # Update previous prices for the product
        c.execute("UPDATE products SET previous_price = ? WHERE product_name = ?", (discounted_price, product_name))

    # Commit changes and close database connection
    conn.commit()
    conn.close()

    # Update the inserted products file
    update_inserted_products('E:\VegEase\Vegease\BigBasket\Bigbasket_inserted_products.txt', inserted_products)

    return new_products, updated_products

if __name__ == "__main__":
    categories = [
        ('https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/?nc=ct-fa', 'Fresh Vegetables'),
        ('https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/?nc=ct-fa', 'Fresh Fruits'),
    ]

    # Create Excel file with sheets if it doesn't exist
    if not os.path.isfile('E:\VegEase\Vegease\BigBasket\Bigbasket_products.xlsx'):
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
        conn = sqlite3.connect('E:\VegEase\Vegease\BigBasket\Bigbasket_products_database.db')
        df = pd.read_sql_query(f"SELECT * FROM products WHERE category='{category_name}'", conn)
        conn.close()
        existing_df = pd.concat([existing_df, df], ignore_index=True)
     
        # Remove duplicates from the combined DataFrame
        existing_df.drop_duplicates(subset=["product_name"], keep="last", inplace=True)    
        
    # Update Excel file and sheets
    with pd.ExcelWriter('E:\VegEase\Vegease\BigBasket\Bigbasket_products.xlsx', engine='xlsxwriter') as writer:
        for category in categories:
            category_name = category[1]
            df_category = existing_df[existing_df["category"] == category_name]
            df_category.to_excel(writer, sheet_name=category_name, index=False)
            
    # Prepare notification messages for new and updated products
    new_products_notification_text = "\n".join([f"Category: {category}\n{format_notification_table(products)}" for category, products in all_new_products.items() if products])
    updated_products_notification_text = "\n".join([f"Category: {category}\n{format_notification_table(products)}" for category, products in all_updated_products.items() if products])

    # Send notifications for new and updated products
    if new_products_notification_text:
        send_notification("BigBasket: New Products Alert", f"New products added:\n{new_products_notification_text}\nCheck them out!", 'kdhini2807@gmail.com')

    if updated_products_notification_text:
        send_notification("BigBasket: Price Changes Alert", f"Price changes detected:\n{updated_products_notification_text}\nTime to grab a deal!", 'kdhini2807@gmail.com')
