from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Function to scroll down and load more content
def scroll_down(driver, num_scrolls):
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust sleep duration as needed

# Function to scrape products using Selenium
def scrape_products(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration

    # Initialize Chrome WebDriver with options
    driver = webdriver.Chrome(options=options)

    # Set an implicit wait to wait for elements to load
    driver.implicitly_wait(10)

    # Open the URL in the WebDriver
    driver.get(url)

    # Scroll down to load more content (you can adjust the number of scrolls)
    scroll_down(driver, 10)

    # Get the page source after scrolling
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find and return the product cards
    product_cards = soup.find_all("li", class_="PaginateItems___StyledLi-sc-1yrbjdr-0")

    # Create a list to store product details
    products = []

    # Loop through each product card and extract details
    for card in product_cards:
        product_name_elem = card.find("h3", class_="text-base")
        product_brand_elem = card.find("span", class_="Label-sc-15v1nk5-0 BrandName___StyledLabel2-sc-hssfrl-1")
        original_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel2-sc-pldi2d-2 gJxZPQ hsCgvu")
        discounted_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi")
        # Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1

        # Check if the elements are found, and get their text if found, or assign "N/A" if not found
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        product_brand = product_brand_elem.text.strip() if product_brand_elem else "N/A"
        original_price = original_price_elem.text.strip() if original_price_elem else "N/A"
        discounted_price = discounted_price_elem.text.strip() if discounted_price_elem else "N/A"

        # Create a dictionary to store the product details
        product_details = {
            "Product Name": product_name,
            "Brand": product_brand,
            "Original Price": original_price,
            "Discounted Price": discounted_price,
        }

        # Append the product details to the list of products
        products.append(product_details)

    # Close the WebDriver
    driver.quit()

    return products

# Test the scraper
if __name__ == "__main__":
    bigbasket_url = 'https://www.bigbasket.com/cl/fruits-vegetables/?nc=nb'
    products_list = scrape_products(bigbasket_url)

    # Print the scraped product details
    for product in products_list:
        print(f"Product Name: {product['Product Name']}")
        print(f"Brand: {product['Brand']}")
        print(f"Original Price: {product['Original Price']}")
        print(f"Discounted Price: {product['Discounted Price']}")
        print("-" * 50)
