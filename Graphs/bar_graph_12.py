import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import re

# Load data from Otipy, BigBasket, and Vegease into DataFrames
otipy_data = pd.read_excel(r'D:\Nidhi\Vegease\Otipy\otipy_products.xlsx')
bigbasket_data = pd.read_excel(r'D:\Nidhi\Vegease\BigBasket\Bigbasket_products.xlsx')
vegease_data = pd.read_excel(r'D:\Nidhi\Vegease\Vegease\Vegease_products.xlsx')

# Define a function to find matching product names
def find_matching_names(name, name_list):
    max_similarity = -1
    matching_name = None
    for candidate in name_list:
        similarity = fuzz.ratio(name.lower(), candidate.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            matching_name = candidate
    return matching_name

# Merge the three DataFrames based on matching product names
otipy_data['matching_name'] = otipy_data['product_name'].apply(
    lambda x: find_matching_names(x, bigbasket_data['product_name'].tolist())
)
merged_data = pd.merge(otipy_data, bigbasket_data, left_on='matching_name', right_on='product_name', suffixes=('_otipy', '_bigbasket'))
merged_data['matching_name'] = merged_data['product_name_otipy'].apply(
    lambda x: find_matching_names(x, vegease_data['product_name'].tolist())
)
merged_data = pd.merge(merged_data, vegease_data, left_on='matching_name', right_on='product_name', suffixes=('', '_vegease'))

# Filter out rows where all three prices are numeric
filtered_data = merged_data[
    (pd.to_numeric(merged_data['discounted_price_otipy'], errors='coerce').notna()) &
    (pd.to_numeric(merged_data['discounted_price_bigbasket'], errors='coerce').notna()) &
    (pd.to_numeric(merged_data['discounted_price'], errors='coerce').notna())
]

# Create a bar chart to compare prices for multiple items
plt.figure(figsize=(12, 6))
bar_width = 0.25
index = range(len(filtered_data))

plt.bar(index, filtered_data['discounted_price_otipy'], bar_width, label='Otipy', alpha=0.7)
plt.bar(index, filtered_data['discounted_price_bigbasket'], bar_width, label='BigBasket', alpha=0.7, align='edge')
plt.bar(index, filtered_data['discounted_price'], bar_width, label='Vegease', alpha=0.7, align='edge')

plt.xlabel('Products')
plt.ylabel('Price (in INR)')
plt.xticks(index, filtered_data['product_name_otipy'], rotation=45, fontsize=8, ha='right')
plt.title('Price Comparison Between Otipy, BigBasket, and Vegease for Different Products')
plt.legend()
plt.tight_layout()

# Save the plot as an image (e.g., PNG)
plt.savefig('price_comparison.png')

# Display the plot
plt.show()

