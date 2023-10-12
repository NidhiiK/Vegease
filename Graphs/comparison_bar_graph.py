import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import re

# Load your data from both Otipy and BigBasket into DataFrames
otipy_data = pd.read_excel(r'D:\Nidhi\Vegease\Otipy\otipy_products.xlsx')
bigbasket_data = pd.read_excel(r'D:\Nidhi\Vegease\BigBasket\Bigbasket_products.xlsx')

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

# Filter out rows where either price is 'N/A'
filtered_data = merged_data[(merged_data['discounted_price_otipy'] != 'N/A') & (merged_data['discounted_price_bigbasket'] != 'N/A')]

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

# Create a larger bar chart to compare prices for multiple items
plt.figure(figsize=(18, 6))  # Increase the figure width

bar_width = 0.35
index = range(len(filtered_data))

plt.bar(index, filtered_data['discounted_price_otipy'], bar_width, label='Otipy', alpha=0.7)
plt.bar(index, filtered_data['discounted_price_bigbasket'], bar_width, label='BigBasket', alpha=0.7, align='center')

plt.xlabel('Products')
plt.ylabel('Price (in INR)')
plt.xticks(index, filtered_data['product_name_otipy'], rotation=90, fontsize=8, ha='right')  # Rotate labels and increase font size
plt.title('Price Comparison Between Otipy and BigBasket for Different Products')
plt.legend()
plt.tight_layout()

# Save the plot as an image (e.g., PNG)
plt.savefig('price_comparison_bar.png')

# Display the plot
plt.show()
