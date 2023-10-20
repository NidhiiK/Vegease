import os
import pandas as pd
import xlsxwriter
from scraper import scrape_products  # Import your scraper function
from notifier import send_notification
from datetime import datetime
from notification_formatter import format_notification_table
from notification_formatter import format_notification_table_np
from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
db = client["bigbasket_db"]  # Create or connect to the "bigbasket_db" database

# Define a function to create an Excel file with multiple sheets
def create_excel_file(categories):
    workbook = xlsxwriter.Workbook('Bigbasket_products_new.xlsx')

    for _, category_name in categories:
        workbook.add_worksheet(category_name)

    workbook.close()

# Define the main function to scrape, process, and store data
def main_function(url, category_name, existing_df):
    # Scrape the website
    bigbasket_product_cards = scrape_products(url)

    # Get or create a MongoDB collection for products
    products_collection = db[category_name]

    # Lists to keep track of new and updated products
    new_products = []
    updated_products = []

    # Process and store data
    for card in bigbasket_product_cards:
        product_name_elem = card.find("h3", class_="text-base")
        original_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel2-sc-pldi2d-2 gJxZPQ hsCgvu")
        discounted_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi")
        discount_elem = card.find("span", class_="font-semibold lg:text-xs xl:text-sm leading-xxl xl:leading-md")
        quantity_elem = card.find("span", class_=["Label-sc-15v1nk5-0 PackChanger___StyledLabel-sc-newjpv-1 gJxZPQ cWbtUx", "Label-sc-15v1nk5-0 gJxZPQ truncate"])

        # Check if the elements are found, and get their text if found, or assign "N/A" if not found
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        original_price = original_price_elem.text.strip() if original_price_elem else "N/A"
        discounted_price = discounted_price_elem.text.strip() if discounted_price_elem else "N/A"
        discount = discount_elem.text.strip() if discount_elem else "N/A"
        quantity = quantity_elem.text.strip() if quantity_elem else "N/A"
        
        # Set the timezone to IST
        current_time = datetime.now()

        # Check if the product exists in the collection
        existing_product = products_collection.find_one({"product_name": product_name})

        if existing_product:
            last_price = existing_product["discounted_price"]

            if last_price != discounted_price:
                updated_products.append((product_name, last_price, discounted_price, quantity))

            # Update the existing product with the new data
            products_collection.update_one({"_id": existing_product["_id"]},
                                          {"$set": {
                                              "original_price": original_price,
                                              "discounted_price": discounted_price,
                                              "discount": discount,
                                              "quantity": quantity,
                                              "timestamp": current_time
                                          }})
        else:
            new_products.append((product_name, original_price, discounted_price, quantity))

            # Insert a new product document
            products_collection.insert_one({
                "product_name": product_name,
                "original_price": original_price,
                "discounted_price": discounted_price,
                "discount": discount,
                "quantity": quantity,
                "category": category_name,
                "timestamp": current_time
            })

    return new_products, updated_products

if __name__ == "__main__":
    categories = [
        ('https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/?nc=ct-fa', 'Fresh Vegetables'),
        ('https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/?nc=ct-fa', 'Fresh Fruits'),
    ]

    # Create Excel file with sheets if it doesn't exist
    if not os.path.isfile('Bigbasket_products_new.xlsx'):
        create_excel_file(categories)

    all_new_products = {}
    all_updated_products = {}
    existing_df = pd.DataFrame()  # Initialize an empty DataFrame to store existing data

    for url, category in categories:
        new_category_products, updated_category_products = main_function(url, category, existing_df)
        all_new_products[category] = new_category_products
        all_updated_products[category] = updated_category_products

    # Print out new and updated products
    for category, products in all_new_products.items():
        print(f"New Products in {category}: {products}")
    for category, products in all_updated_products.items():
        print(f"Updated Products in {category}: {products}")

    # Prepare notification messages for new and updated products
    new_products_notification_text = "\n".join([f"Category: {category}\n{format_notification_table_np(products)}" for category, products in all_new_products.items() if products])
    updated_products_notification_text = "\n".join([f"Category: {category}\n{format_notification_table(products)}" for category, products in all_updated_products.items() if products])

    # Send notifications for new and updated products
    if new_products_notification_text:
        send_notification("BigBasket: New Products Alert", f"New products added:\n{new_products_notification_text}\nCheck them out!", 'kdhini2807@gmail.com')

    if updated_products_notification_text:
        send_notification("BigBasket: Price Changes Alert", f"Price changes detected:\n{updated_products_notification_text}\nTime to grab a deal!", 'kdhini2807@gmail.com')
