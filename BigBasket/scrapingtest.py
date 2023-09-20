from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# # Function to scroll down and load more content
# def scroll_down(driver, num_scrolls):
#     for _ in range(num_scrolls):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Adjust sleep duration as needed

# Function to scroll down and load more content until no more items are loaded
# Function to scroll down in smaller steps until no more items are loaded
# Function to scroll down until no more items are loaded (infinite scrolling)
# Function to scroll down until no more items are loaded (infinite scrolling)
def scroll_down_until_end(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust sleep duration as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height



# Function to scrape products using Selenium
def scrape_products(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration

    # Initialize Chrome WebDriver with options
    driver = webdriver.Chrome(options=options)  # Use `chrome_options` instead of `options`

    # Set an implicit wait to wait for elements to load
    driver.implicitly_wait(10)

    # Open the URL in the WebDriver
    driver.get(url)

    # Scroll down to load more content (you can adjust the number of scrolls)
    # scroll_down_until_end(driver)

    # Scroll down until no more items are loaded
    scroll_down_until_end(driver)

    # Wait for the page to fully load (you may need to adjust the timeout)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "PaginateItems___StyledLi-sc-1yrbjdr-0")))

    # Get the page source after scrolling
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find and return the product cards
    # Find and return the product cards (first class)
    product_cards = soup.find_all("li", class_=["PaginateItems___StyledLi-sc-1yrbjdr-0", "PaginateItems___StyledLi2-sc-1yrbjdr-1"])

    # # Find and return the product cards (second class)
    # product_cards_class2 = soup.find_all("li", class_="PaginateItems___StyledLi2-sc-1yrbjdr-1")

    # # Combine the product cards from both classes
    # all_product_cards = product_cards_class1 + product_cards_class2

    # Find the length (number) of product cards
    num_product_cards = len(product_cards)

    print(f"Number of Product Cards: {num_product_cards}")
    

    driver.quit()

    # Create a list to store product details
    products = []

    # Loop through each product card and extract details
    for card in product_cards:
        product_name_elem = card.find("h3", class_="text-base")
        # product_brand_elem = card.find("span", class_="Label-sc-15v1nk5-0 BrandName___StyledLabel2-sc-hssfrl-1")
        original_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel2-sc-pldi2d-2 gJxZPQ hsCgvu")
        discounted_price_elem = card.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi")
        discount_precentage_elm = card.find("span", class_= "font-semibold lg:text-xs xl:text-sm leading-xxl xl:leading-md")
        quantity_elm = card.find("span", class_= "Label-sc-15v1nk5-0 PackChanger___StyledLabel-sc-newjpv-1 gJxZPQ cWbtUx")


        # Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1

        # Check if the elements are found, and get their text if found, or assign "N/A" if not found
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        # product_brand = product_brand_elem.text.strip() if product_brand_elem else "N/A"
        original_price = original_price_elem.text.strip() if original_price_elem else "N/A"
        discounted_price = discounted_price_elem.text.strip() if discounted_price_elem else "N/A"
        discount_value = discount_precentage_elm.text.strip() if discount_precentage_elm else "N/A"
        quantity = quantity_elm.text.strip() if quantity_elm else "N/A"


        # Create a dictionary to store the product details
        product_details = {
            "Product Name": product_name,
            # "Brand": product_brand,
            "Original Price": original_price,
            "Discounted Price": discounted_price,
            "Discount" : discount_value,
            "Quantity" : quantity
        }

        # Append the product details to the list of products
        products.append(product_details)

    # Close the WebDriver
    driver.quit()

    return products

# Test the scraper
if __name__ == "__main__":
    bigbasket_url = 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/?nc=ct-fa'
    products_list = scrape_products(bigbasket_url)
    

    # Print the scraped product details
    for product in products_list:
        print(f"Product Name: {product['Product Name']}")
        # print(f"Brand: {product['Brand']}")
        print(f"Original Price: {product['Original Price']}")
        print(f"Discounted Price: {product['Discounted Price']}")
        print(f"Discount: {product['Discount']}")
        print(f"Quantity: {product['Quantity']}")
        print("-" * 50)

