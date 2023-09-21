import pandas as pd
from notifier import send_notification

def send_price_change_notifications(new_df, existing_df):
    # Merge the new DataFrame with the existing one to compare prices
    merged_df = existing_df.merge(new_df, on='product_name', suffixes=('_existing', '_new'))

    # Filter rows where the discounted price has changed
    price_changed_df = merged_df[merged_df['discounted_price_existing'] != merged_df['discounted_price_new']]

    if not price_changed_df.empty:
        # Create a notification message for price changes
        price_changed_df['price_change'] = (price_changed_df['discounted_price_existing'] +
                                            " -> " +
                                            price_changed_df['discounted_price_new'])

        notification_text = f"Price changes detected:\n{price_changed_df[['product_name', 'price_change']].to_string(index=False)}"

        # Send the notification
        send_notification("Price Changes Alert", notification_text, 'kdhini2807@gmail.com')

    return new_df

# Testing example
if __name__ == "__main__":
    # Sample data for existing and new products
    existing_data = {
        'product_name': ['Product A', 'Product B', 'Product C'],
        'discounted_price': ['10.00', '15.00', '20.00']
    }

    new_data = {
        'product_name': ['Product A', 'Product B', 'Product C'],
        'discounted_price': ['10.00', '14.00', '20.00']
    }

    # Create DataFrames for existing and new data
    existing_df = pd.DataFrame(existing_data)
    new_df = pd.DataFrame(new_data)

    # Call the function to send price change notifications
    send_price_change_notifications(new_df, existing_df)
