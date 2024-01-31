from ast import While
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import datetime
import tkinter as tk
from tkinter import FIRST, messagebox



class WebScraper:
    def __init__(self):
        # Initialize the webdriver
        self.firefox_options = Options()
        self.firefox_options.headless = True
        self.driver = webdriver.Firefox(options=self.firefox_options)
        self.actions = ActionChains(self.driver)
        self.data_export = []

    def close_browser(self):
        self.driver.quit()

    def navigate_to_url(self, url):
        self.driver.get(url)
        sleep(5)  # Adjust sleep as needed

    def Start(self):
        # Now that the content is loaded, get the HTML
        print('Render the dynamic content to static HTML')
        html = self.driver.page_source       
        print(' Parse the static HTML')
        soup = BeautifulSoup(html, "html.parser")
        
        # Find all occurrences of 'div' with class "menu"
        all_menu_divs = soup.find_all("div", {"class": "menu"})
        
        # Process each 'div' separately
        for menu_div in all_menu_divs:
            # Access the 'a' tags within each 'div'
            value = menu_div.find_all('a')
            
            # Process Each Brand:
            for link in value:
                child_link = link.get('href')
                new_link = 'https://www.benkibrewingtools.com' + child_link
                self.navigate_to_url(new_link)
                html_brand = self.driver.page_source       
                brand_soup = BeautifulSoup(html_brand, "html.parser")
                all_name_divs = brand_soup.find_all("div", {"class": "name"})
                for name_div in all_name_divs:
                    # Access the 'a' tags within each 'div'
                    product_atag = name_div.find_all('a')
                    
                    # Process each Product:
                    for link_product in product_atag:
                        child_link_product = link_product.get('href')
                        new_productlink = 'https://www.benkibrewingtools.com' + child_link_product
                        self.navigate_to_url(new_productlink)

                        #Get Product detail information:
                        html_Product = self.driver.page_source       
                        Product_soup = BeautifulSoup(html_Product, "html.parser")
                        
                        ##Get product name:
                        meta_tag = Product_soup.find("meta", {"itemprop": "name"})
                        Product_name = meta_tag.get("content")

                         ##Get product vendor_name:
                        vendor_divs = Product_soup.find("div", {"class": "vendor"})
                        vendor_a_tag = vendor_divs.find("a")
                        vendor_name = vendor_a_tag.text

                         ##Get product description:
                        description_div = Product_soup.find("div", {"class": "description"})

                        # Check if the div exists before trying to access its content
                        if description_div:
                            # Find the <span> with itemprop="sku" within the <p> with class "variant-sku"
                            sku_span = description_div.find("span", {"itemprop": "sku"})

                            # Check if the span with itemprop="sku" exists before trying to access its text content
                            if sku_span:
                                product_code = sku_span.text.strip()

                                # Find the <span> with class "stock" within the <p> with class "variation-availability"
                                stock_span = description_div.find("span", {"class": "stock"})

                                # Check if the span with class "stock" exists before trying to access its text content
                                if stock_span:
                                    availability = stock_span.text.strip()
                                    print(f"Product Code: {product_code}")
                                    print(f"Availability: {availability}")
                                else:
                                    print("No span with class 'stock' found within the div.")
                            else:
                                print("No span with itemprop='sku' found within the div.")
                        else:
                            print("Div with class 'description' not found.")



                        # Append the data to the list
                        self.data_export.append({'Product_name': Product_name, 'Vendor': vendor_name, 'SKU': product_code, 'STOCK': availability })
                        print("Info: \n", self.data_export)
                        self.export_to_excel()

    def export_to_excel(self, file_name='output.xlsx'):
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(self.data_export)

        # Export DataFrame to Excel
        df.to_excel(file_name, index=False)
        print(f'Data exported to {file_name}')


# Example usage:
if __name__ == "__main__":
    url = "https://www.benkibrewingtools.com"
    scraper = WebScraper()

    try:
        scraper.navigate_to_url(url)
        scraper.Start()

    finally:
        scraper.close_browser()
