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
        time.sleep(1)  # Adjust sleep duration as needed

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
    scroll_down(driver, 20)

    # Wait for the product elements to be present on the page
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-pf="reset"]'))
    )

    # Get the page source after scrolling
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find and return the product cards
    product_cards = soup.find_all("div", attrs={"data-pf": "reset"})
    print(len(product_cards))

    return product_cards

# Test the scraper
if __name__ == "__main__":
    blinkit_url = 'https://blinkit.com/cn/vegetables-fruits/fresh-vegetables/cid/1487/1489'  # Replace with the actual URL
    blinkit_product_cards = scrape_products(blinkit_url)
    for card in blinkit_product_cards:
        product_name_elem = card.find("div", class_="tw-text-300")
        product_quantity_elem = card.find("div", class_="tw-text-200 tw-font-medium tw-line-clamp-1")
        product_price_elem = card.find("div", class_="tw-text-200 tw-font-semibold")

        # Check if the elements are found, and get their text if found, or assign "N/A" if not found
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        product_quantity = product_quantity_elem.text.strip() if product_quantity_elem else "N/A"
        product_price = product_price_elem.text.strip() if product_price_elem else "N/A"

        print(f"Product Name: {product_name}")
        print(f"Product Quantity: {product_quantity}")
        print(f"Product Price: {product_price}\n")
