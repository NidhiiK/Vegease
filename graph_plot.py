import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data from both Otipy and BigBasket into DataFrames
otipy_data = pd.read_excel(r'D:\Nidhi\Vegease\Otipy\otipy_products.xlsx')
bigbasket_data = pd.read_excel(r'D:\Nidhi\Vegease\BigBasket\Bigbasket_products.xlsx')

# Assuming both DataFrames have the same columns
columns_to_use = ['product_name', 'original_price', 'discounted_price', 'discount', 'quantity', 'category', 'previous_price']

# Filter columns to use in both DataFrames
otipy_data = otipy_data[columns_to_use]
bigbasket_data = bigbasket_data[columns_to_use]

# Function to extract and convert numeric values from strings
def extract_numeric(value):
    try:
        return float(''.join(filter(str.isdigit, str(value))))
    except ValueError:
        return None  # Handle non-convertible values as needed

# Clean and convert the 'discounted_price' column
otipy_data['discounted_price'] = otipy_data['discounted_price'].apply(extract_numeric)
bigbasket_data['discounted_price'] = bigbasket_data['discounted_price'].apply(extract_numeric)

# Drop rows with NaN values (non-convertible values)
otipy_data = otipy_data.dropna(subset=['discounted_price'])
bigbasket_data = bigbasket_data.dropna(subset=['discounted_price'])

# # Clean the 'discounted_price' column by removing non-numeric characters
# otipy_data['discounted_price'] = otipy_data['discounted_price'].str.replace('₹', '').str.replace('/kg', '').str.replace('/Pack', '').astype(float)
# bigbasket_data['discounted_price'] = bigbasket_data['discounted_price'].str.replace('₹', '').str.replace('/kg', '').str.replace('/Pack', '').astype(float)

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Boxplot for Otipy
sns.boxplot(data=otipy_data, x='category', y='discounted_price', ax=axes[0, 0])
axes[0, 0].set_title('Otipy Discounted Prices by Category')

# Boxplot for BigBasket
sns.boxplot(data=bigbasket_data, x='category', y='discounted_price', ax=axes[0, 1])
axes[0, 1].set_title('BigBasket Discounted Prices by Category')

# Additional plots as needed
# ...

# Adjust layout
plt.tight_layout()

# Save the plot as an image (e.g., PNG)
plt.savefig('price_comparison3.png')

# Display the plots
plt.show()
