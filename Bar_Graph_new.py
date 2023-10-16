import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import re

# Load your data from both Otipy and BigBasket into DataFrames
otipy_data = pd.read_excel('E:\VegEase\Vegease\Otipy\otipy_products.xlsx')
bigbasket_data = pd.read_excel('E:\VegEase\Vegease\BigBasket\Bigbasket_products.xlsx')

# Load Vegease data into a DataFrame
vegease_data = pd.read_excel('E:\VegEase\Vegease\Vegease_products.xlsx')

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

# Merge the two DataFrames based on matching product names
otipy_data['matching_name'] = otipy_data['product_name'].apply(
    lambda x: find_matching_names(x, bigbasket_data['product_name'].tolist())
)
merged_data = pd.merge(otipy_data, bigbasket_data, left_on='matching_name', right_on='product_name', suffixes=('_otipy', '_bigbasket'))

# Merge the Vegease data based on matching product names
merged_data = pd.merge(merged_data, vegease_data, left_on='matching_name', right_on='product_name', suffixes=('', '_vegease'))

# Filter out rows where either price is 'N/A'
filtered_data = merged_data[(merged_data['discounted_price_otipy'] != 'N/A') & (merged_data['discounted_price_bigbasket'] != 'N/A') & (merged_data['discounted_price_vegease'] != 'N/A')]

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
filtered_data['discounted_price_otipy'] = filtered_data['discounted_price_otipy'].apply(extract_numeric)
filtered_data['discounted_price_bigbasket'] = filtered_data['discounted_price_bigbasket'].apply(extract_numeric)
filtered_data['discounted_price_vegease'] = filtered_data['discounted_price_vegease'].apply(extract_numeric)

# Create a bar chart to compare prices for multiple items
plt.figure(figsize=(12, 6))
bar_width = 0.25  # Reduce the width of bars to accommodate three datasets
index = range(len(filtered_data))

plt.bar(index, filtered_data['discounted_price_otipy'], bar_width, label='Otipy', alpha=0.7)
plt.bar([i + bar_width for i in index], filtered_data['discounted_price_bigbasket'], bar_width, label='BigBasket', alpha=0.7, align='edge')
plt.bar([i + bar_width * 2 for i in index], filtered_data['discounted_price_vegease'], bar_width, label='Vegease', alpha=0.7, color='green', align='edge')

plt.xlabel('Products')
plt.ylabel('Price (in INR)')
plt.xticks([i + bar_width for i in index], filtered_data['product_name_otipy'], rotation=45, fontsize=8, ha='right')
plt.title('Price Comparison Between Otipy, BigBasket, and Vegease for Different Products')
plt.legend()
plt.tight_layout()

# Save the plot as an image (e.g., PNG)
plt.savefig('price_comparison_new.png')

# Display the plot
plt.show()
