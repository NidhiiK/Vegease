# price_change_notifier.py

# import pandas as pd
# from notifier import send_notification

# def send_price_change_notifications(existing_df, all_updated_products):
#     if existing_df.empty:
#         return  # No previous data, cannot send price change notifications

#     for category, updated_products in all_updated_products.items():
#         if not updated_products:
#             continue  # No updated products in this category

#         # Create a DataFrame for the new products in this category
#         new_df = pd.DataFrame(updated_products, columns=["product_name", "original_price", "discounted_price", "discount"])

#         # Merge the new DataFrame with the existing DataFrame based on product_name
#         merged_df = pd.merge(existing_df, new_df, on='product_name', suffixes=('_prev', '_cur'))

#         # Find rows where the discounted_price has changed
#         price_changed_rows = merged_df[merged_df['discounted_price_prev'] != merged_df['discounted_price_cur']]

#         # Check if there are any price changes in this category
#         if not price_changed_rows.empty:
#             # Prepare and send notifications for price changes in this category
#             price_change_notification_text = price_changed_rows.to_string(index=False)
#             send_notification("Price Changes Alert", f"Price changes detected in '{category}':\n{price_change_notification_text}\nTime to grab a deal!", 'kdhini2807@gmail.com')



# price_change_notifier.py

# price_change_notifier.py

# price_change_notifier.py

import pandas as pd
from notification_formatter import format_notification_table

def send_price_change_notifications(existing_df, all_updated_products):
    # Initialize a dictionary to store category-wise notifications
    category_notifications = {}

    for category, updated_products in all_updated_products.items():
        # Check if there are updated products in this category
        if updated_products:
            # Create a DataFrame for the updated products
            updated_df = pd.DataFrame(updated_products, columns=["product_name", "original_price_prev", "discounted_price_prev", "discount_prev", "category", "quantity", "timestamp", "original_price_cur", "discounted_price_cur", "discount_cur"])

            # Find rows where prices have changed
            price_changed_rows = updated_df[updated_df['discounted_price_prev'] != updated_df['discounted_price_cur']]

            # Check if there are price changes in this category
            if not price_changed_rows.empty:
                # Format notification for this category
                category_notification_text = f"Price changes detected in '{category}':\n"
                category_notification_text += format_notification_table(price_changed_rows[["product_name", "original_price_prev", "discounted_price_prev", "discount_prev", "original_price_cur", "discounted_price_cur", "discount_cur"]].values.tolist())
                
                # Store the notification for this category
                category_notifications[category] = category_notification_text

    # Create a combined notification text for all categories
    combined_notification_text = "\n".join(category_notifications.values())

    return combined_notification_text


