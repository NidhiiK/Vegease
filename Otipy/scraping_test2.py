from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

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
    num_scrolls = 20
    for _ in range(num_scrolls):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Adjust sleep duration as needed

    # Wait for the product elements to be present on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "style_prod_name__QllSp"))
    )

    # Get the page source after scrolling
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find and return the product cards
    product_cards = soup.find_all("div", class_="style_card__v4i84")
    print(len(product_cards))

    return product_cards

# Test the scraper
if __name__ == "__main__":
    otipy_url = 'https://www.otipy.com/category/vegetables-1'
    otipy_product_cards = scrape_products(otipy_url)
    for card in otipy_product_cards:
        product_name_elem = card.find("h3", class_="style_prod_name__QllSp")
        original_price_elem = card.find("span", class_="style_striked_price__4ghn5")
        discounted_price_elem = card.find("span", class_="style_selling_price__GaIsF")
        discount_elem = card.find("p", class_="style_final_price__FERLK")
        quantity_elem = card.find("span", class_="style_prod_qt__cXcqe")


        # Check if the elements are found, and get their text if found, or assign "N/A" if not found
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        original_price = original_price_elem.text.strip() if original_price_elem else "N/A"
        discounted_price = discounted_price_elem.text.strip() if discounted_price_elem else "N/A"
        discount = discount_elem.text.strip() if discount_elem else "N/A"
        quantity = quantity_elem.text.strip() if quantity_elem else "N/A"


        print(f"Product Name: {product_name}")
        print(f"Original Price: {original_price}")
        print(f"Discounted Price: {discounted_price}")
        print(f"Discount: {discount}")
        print(f"Quantity: {quantity}\n")
