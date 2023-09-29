import pandas as pd
import matplotlib.pyplot as plt

# Load Otipy data (replace 'your_data.csv' with your actual data file)
otipy_data = pd.read_excel(r'D:\Nidhi\Vegease\Otipy\otipy_products.xlsx')

# Convert 'timestamp' to datetime format
otipy_data['timestamp'] = pd.to_datetime(otipy_data['timestamp'])

# Create a line plot
plt.figure(figsize=(10, 6))
plt.plot(otipy_data['timestamp'], otipy_data['discounted_price_otipy'], marker='o')
plt.title('Otipy Price Trends Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Price (INR)')
plt.grid()
plt.show()
