import unidecode
import json
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class HotelScraper:
    def __init__(self, driver_path: str = 'ChromeDriver.exe'):
        
        self.opts = Options()
        self.opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        self.opts.add_argument("--disable-notifications")
        self.opts.add_argument("--disable-blink-features=AutomationControlled")
        
        self.service = Service(executable_path=driver_path)
        self.driver = None

    def clean_hotel_name(self, name: str) -> Dict[str, str | int]:
        
        # Remove accents and convert to lowercase
        cleaned_name = unidecode.unidecode(name.lower().strip())
        
        # Remove special characters (keeping alphanumeric and spaces)
        cleaned_name = ''.join(char for char in cleaned_name if char.isalnum() or char.isspace())
        
        return {
            'original_name': name,
            'cleaned_name': cleaned_name,
            'name_length': len(cleaned_name)
        }

    def setup_driver(self):
        
        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.opts)
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            raise

    def reject_cookies(self):
        
        try:
            reject_cookies = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler'))
            )
            reject_cookies.click()
        except TimeoutException:
            print("No se encontró el botón de cookies o no fue necesario")

    def load_all_hotels(self, url: str):
       
        try:
            self.driver.get(url)
            self.reject_cookies()

            # Wait for initial hotel results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='title']"))
            )

            # Load all hotel results
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                try:
                    load_more_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Cargar más resultados')]]"))
                    )
                    load_more_button.click()
                    time.sleep(3)
                except (TimeoutException, NoSuchElementException):
                    print("No hay más hoteles para cargar.")
                    break

        except Exception as e:
            print(f"Error loading hotels: {e}")
            raise

    def extract_hotel_names(self) -> List[Dict[str, str | int]]:
        
        hotel_names = []
        hotel_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='title']")
        
        seen_names = set()
        for hotel in hotel_elements:
            hotel_text = hotel.text.strip()
            if hotel_text and hotel_text not in seen_names:
                cleaned_hotel = self.clean_hotel_name(hotel_text)
                hotel_names.append(cleaned_hotel)
                seen_names.add(hotel_text)
        
        return hotel_names

    def save_hotel_data(self, hotel_names: List[Dict[str, str | int]]):
        
        # Sort by cleaned name for consistent output
        sorted_names = sorted(hotel_names, key=lambda x: x['cleaned_name'])

        # Save to text file
        with open("hoteles.txt", "w", encoding="utf-8") as txt_file:
            for hotel in sorted_names:
                txt_file.write(f"{hotel['original_name']}\n")

        # Save to JSON file
        with open("hoteles.json", "w", encoding="utf-8") as json_file:
            json.dump(sorted_names, json_file, ensure_ascii=False, indent=4)

        print(f"Se guardaron {len(sorted_names)} hoteles en hoteles.txt y hoteles.json")

    def scrape_hotels(self, url: str):
        
        try:
            self.setup_driver()
            self.load_all_hotels(url)
            hotel_names = self.extract_hotel_names()
            self.save_hotel_data(hotel_names)
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            if self.driver:
                self.driver.quit()

def main():
    url = 'https://www.booking.com/searchresults.es.html?label=gen173nr-1BCAEoggI46AdIM1gEaEaIAQGYAQq4ARfIAQ_YAQHoAQGIAgGoAgO4AuK37b4GwAIB0gIkNWQzMzk4MzgtNTQxZC00ZWQwLWE5NTAtOTM2Zjc3ODI1NDky2AIF4AIB&sid=f96da1336d70906d23a507a72b3ec29a&aid=304142&checkin=2025-08-04&checkout=2025-08-10&dest_id=-401497&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null'
    
    scraper = HotelScraper()
    scraper.scrape_hotels(url)

if __name__ == "__main__":
    main()