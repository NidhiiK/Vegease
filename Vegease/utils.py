
import os

def load_inserted_products(filename):
    inserted_products = set()
    if os.path.exists(filename):  # Check if the file exists before trying to read
        with open(filename, 'r') as file:
            for line in file:
                inserted_products.add(line.strip())
    return inserted_products

def update_inserted_products(filename, inserted_products):
    with open(filename, 'w') as file:
        for product in inserted_products:
            file.write(f'{product}\n')