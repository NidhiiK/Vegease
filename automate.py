import subprocess
import time

def run_main_files():
    # Replace with the paths to your main files
    bigbasket_main_path = r'D:\Nidhi\Vegease\BigBasket\main_office.py'
    otipy_main_path = r'D:\Nidhi\Vegease\BigBasket\main_office.py'
    
    # Run the main files using subprocess
    subprocess.call(['python', bigbasket_main_path])
    subprocess.call(['python', otipy_main_path])

if __name__ == "__main__":
    while True:
        run_main_files()  # Run the main files
        time.sleep(3600)  # Sleep for an hour before running again
