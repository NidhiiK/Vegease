import pandas as pd
import matplotlib.pyplot as plt

# Load your data from both Otipy and BigBasket into DataFrames
otipy_data = pd.read_excel(r'D:\Nidhi\Vegease\Otipy\otipy_products.xlsx')
bigbasket_data = pd.read_excel(r'D:\Nidhi\Vegease\BigBasket\Bigbasket_products.xlsx')


# Assuming both DataFrames have a 'product_name' and 'discounted_price' column
# Merge the two DataFrames on 'product_name'
merged_data = pd.merge(otipy_data, bigbasket_data, on='product_name', suffixes=('_otipy', '_bigbasket'))

# Filter out rows where either price is 'N/A'
filtered_data = merged_data[(merged_data['discounted_price_otipy'] != 'N/A') & (merged_data['discounted_price_bigbasket'] != 'N/A')]

# Convert price columns to numeric values (remove currency symbols if any)
filtered_data['discounted_price_otipy'] = filtered_data['discounted_price_otipy'].str.replace('₹', '').str.replace('/kg', '').astype(float)
filtered_data['discounted_price_bigbasket'] = filtered_data['discounted_price_bigbasket'].str.replace('₹', '').str.replace('/kg', '').astype(float)

# Create a bar chart to compare prices
plt.figure(figsize=(12, 6))
plt.bar(filtered_data['product_name'], filtered_data['discounted_price_otipy'], label='Otipy', alpha=0.7)
plt.bar(filtered_data['product_name'], filtered_data['discounted_price_bigbasket'], label='BigBasket', alpha=0.7)
plt.xlabel('Product Name')
plt.ylabel('Price (in INR)')
plt.xticks(rotation=90)
plt.title('Price Comparison Between Otipy and BigBasket')
plt.legend()
plt.tight_layout()

# Save the plot as an image (e.g., PNG)
plt.savefig('price_comparison.png')

# Display the plot
plt.show()

