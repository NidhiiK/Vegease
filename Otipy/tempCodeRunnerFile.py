        # # Check if the product is new or updated
        # if product_name not in inserted_products:
        #     new_products.append((product_name, original_price, discounted_price, discount))
        #     inserted_products.add(product_name)
        # else:
        #     existing_product = c.execute("SELECT DISTINCT * FROM products WHERE product_name=?", (product_name,)).fetchone()
        #     if existing_product and existing_product[2] != discounted_price:
        #         updated_products.append((product_name, original_price, discounted_price, discount))
        #     # Update the previous price in the database
        #     c.execute("UPDATE products SET previous_price = ? WHERE product_name = ?", (existing_product[2], product_name))