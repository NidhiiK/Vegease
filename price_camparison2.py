import pandas as pd
import matplotlib.pyplot as plt
import re

# Load your data from both Otipy and BigBasket into DataFrames
otipy_data = pd.read_excel(r'D:\Nidhi\Vegease\Otipy\otipy_products.xlsx')
bigbasket_data = pd.read_excel(r'D:\Nidhi\Vegease\BigBasket\Bigbasket_products.xlsx')


# Define a function to extract numeric values from strings
def extract_numeric(text):
    if isinstance(text, float):
        return text  # Return the float value as is
    numeric_part = re.search(r'\d+(\.\d+)?', str(text))
    if numeric_part:
        return float(numeric_part.group())
    else:
        return None

# Apply the extract_numeric function to convert price columns to numeric values
otipy_data['discounted_price'] = otipy_data['discounted_price'].apply(extract_numeric)
bigbasket_data['discounted_price'] = bigbasket_data['discounted_price'].apply(extract_numeric)

# Merge the datasets based on a common attribute (e.g., 'product_name')
merged_data = pd.merge(otipy_data, bigbasket_data, on='product_name')

# Create line plots to compare prices for different products
plt.figure(figsize=(12, 6))
for index, row in merged_data.iterrows():
    plt.plot(['Otipy', 'BigBasket'], [row['discounted_price'], row['discounted_price']], marker='o', label=row['product_name_otipy'], alpha=0.7)

plt.xlabel('Retailer')
plt.ylabel('Price (in INR)')
plt.xticks(rotation=45)
plt.title('Price Comparison Between Otipy and BigBasket for Different Products')
plt.legend()
plt.tight_layout()

# Save the plot as an image (e.g., PNG)
plt.savefig('price_comparison2.png')

# Display the plot
plt.show()

