from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

def scrape_products(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    try:
        # Wait for a specific element to load (you can change this to your needs)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "style_prod_name__QllSp"))
        )

        soup = BeautifulSoup(browser.page_source, "html.parser")
    except NoSuchElementException:
        print("Element not found. Check if the website structure has changed.")
        return []

    browser.quit()

    product_cards = soup.find_all("div", class_="style_card__v4i84")
    return product_cards



# Test the scraper
if __name__ == "__main__":
    otipy_url = 'https://www.otipy.com/category/vegetables-1'
    otipy_product_cards = scrape_products(otipy_url)
    for card in otipy_product_cards:
        product_name = card.find("h3", class_="style_prod_name__QllSp").text.strip()
        original_price = card.find("span", class_="style_striked_price__4ghn5").text.strip()
        discounted_price = card.find("span", class_="style_selling_price__GaIsF").text.strip()
        discount = card.find("p", class_="style_final_price__FERLK").text.strip()
        quantity = card.find("span", class_="style_prod_qt__cXcqe").text.strip()

        print(f"Product Name: {product_name}")
        print(f"Original Price: {original_price}")
        print(f"Discounted Price: {discounted_price}")
        print(f"Discount: {discount}")
        print(f"Quantity: {quantity}\n")