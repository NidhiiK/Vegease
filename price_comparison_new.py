import pandas as pd
import matplotlib.pyplot as plt

# Load your data from both Otipy and BigBasket into DataFrames
otipy_data = pd.read_excel(r'D:\Nidhi\Vegease\Otipy\otipy_products.xlsx')
bigbasket_data = pd.read_excel(r'D:\Nidhi\Vegease\BigBasket\Bigbasket_products.xlsx')

# Assuming both DataFrames have the same columns
columns_to_use = ['product_name', 'timestamp', 'discounted_price']

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

# Create line plots for price trends over time
plt.figure(figsize=(12, 6))

# Line plot for Otipy
plt.plot(otipy_data['timestamp'], otipy_data['discounted_price'], marker='o', label='Otipy', alpha=0.7)
plt.xlabel('Timestamp')
plt.ylabel('Price (in INR)')
plt.title('Otipy Price Trends Over Time')
plt.grid()
plt.legend()

# Save the Otipy plot as an image (e.g., PNG)
plt.savefig('otipy_price_trend.png')
plt.show()

# Line plot for BigBasket
plt.figure(figsize=(12, 6))
plt.plot(bigbasket_data['timestamp'], bigbasket_data['discounted_price'], marker='o', label='BigBasket', alpha=0.7)
plt.xlabel('Timestamp')
plt.ylabel('Price (in INR)')
plt.title('BigBasket Price Trends Over Time')
plt.grid()
plt.legend()

# Save the BigBasket plot as an image (e.g., PNG)
plt.savefig('bigbasket_price_trend.png')
plt.show()

