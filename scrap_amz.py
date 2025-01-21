

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Base URL with placeholders for page number
BASE_URL = "https://www.amazon.in/s?k=cameras&i=electronics&rh=n%3A976419031&dc&page={page}&crid=2YMWGXCFA04OD&qid=1737449834&sprefix=cameras%2Caps%2C230&ref=sr_pg_{page}"

# Headers to mimic browser behavior
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
driver = webdriver.Chrome(options=chrome_options)

# Function to scrape product data
def scrape_amazon_products(max_pages):
    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page=page)
        print(f"Scraping page: {page} | URL: {url}")
        response = requests.get(url, headers=HEADERS)

        # Check for successful response
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Find product elements
            products = soup.find_all("div", {"data-component-type": "s-search-result"})

            for product in products:
                # Extract product details
                title_tag = product.find("a", {"class": "a-link-normal s-line-clamp-2 s-link-style a-text-normal"})
                price_whole = product.find("span", {"class": "a-price-whole"})
                price_fraction = product.find("span", {"class": "a-price-fraction"})
                rating = product.find("span", {"class": "a-icon-alt"})
                rating_count = product.find("span", {"class": "a-size-base"})

                # Fetch the title text from the <h2> inside the <a> tag
                if title_tag:
                    title = title_tag.find("h2")
                    if title:
                        print(f"Title: {title.text.strip()}")

                    # Extract the product link (href attribute) and create the full URL
                    product_link = "https://www.amazon.in" + title_tag.get("href", "")
                    print(f"Product Link: {product_link}")

                    # Use Selenium to open the product link and scrape more data
                    driver.get(product_link)
                    time.sleep(3)  # Wait for the page to load completely

                    print("Product Information:==========================")
      

                      # Fetch product details from the "About this item" section
                    try:
                        about_item_section = driver.find_element(By.ID, "feature-bullets")
                        items = about_item_section.find_elements(By.TAG_NAME, "li")
                        print("About this item:")
                        for item in items:
                            print(f"- {item.text.strip()}")
                    except Exception as e:
                        print(f"Error fetching 'About this item' section: {e}")

                                        
                    # Fetch Product Information
                    try:
                        # Wait for the product details section to be visible
                        product_details_section = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "prodDetails"))
                        )

                        # Locate the technical details table
                        tech_spec_table = product_details_section.find_element(By.ID, "productDetails_techSpec_section_1")
                        
                        # Extract all rows in the table
                        rows = tech_spec_table.find_elements(By.TAG_NAME, "tr")
                        
                        # Loop through the rows and print each key-value pair
                        product_info = {}
                        for row in rows:
                            # Extract key and value from each row
                            columns = row.find_elements(By.TAG_NAME, "td")
                            if columns:
                                key = row.find_element(By.TAG_NAME, "th").text.strip()
                                value = columns[0].text.strip()
                                product_info[key] = value
                        
                        # Print the extracted product information
                        for key, value in product_info.items():
                            print(f"{key}: {value}")
                        
                    except Exception as e:
                        print(f"Error fetching product information: {e}")

                # Handle price
                if price_whole and price_fraction:
                    print(f"Price: ₹{price_whole.text.strip()}{price_fraction.text.strip()}")
                elif price_whole:
                    print(f"Price: ₹{price_whole.text.strip()}")

                # Handle rating
                if rating:
                    print(f"Rating: {rating.text.strip()}")

                # Handle number of ratings
                if rating_count:
                    print(f"Number of Ratings: {rating_count.text.strip()}")

                print("-" * 80)

        else:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
            break

# Specify the number of pages to scrape
scrape_amazon_products(max_pages=1)

# Close the Selenium WebDriver after scraping
driver.quit()
