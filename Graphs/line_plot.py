import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import re  # Import the regular expressions library

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

# Create a line chart to compare prices for multiple items
plt.figure(figsize=(12, 6))
for index, row in otipy_data.iterrows():
    # Find the corresponding product in the BigBasket DataFrame
    matching_product = bigbasket_data[bigbasket_data['product_name'] == row['product_name']]
    
    if not matching_product.empty:
        # If a matching product is found, plot the prices for both Otipy and BigBasket
        plt.plot(['Otipy', 'BigBasket'], [row['discounted_price'], matching_product['discounted_price'].values[0]], marker='o', label=row['product_name'], alpha=0.7)

plt.xlabel('Retailer')
plt.ylabel('Price (in INR)')
plt.xticks(rotation=45)
plt.title('Price Comparison Between Otipy and BigBasket for Different Products')
plt.legend()
plt.tight_layout()

# Save the plot as an image (e.g., PNG)
plt.savefig('price_comparison.png')

# Display the plot
plt.show()


