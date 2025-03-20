from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

s = Service(executable_path = 'ChromeDriver.exe')
driver = webdriver.Chrome(service=s)

driver.get('https://www.booking.com/searchresults.es.html?label=gen173nr-1BCAEoggI46AdIM1gEaEaIAQGYAQq4ARfIAQ_YAQHoAQGIAgGoAgO4AuK37b4GwAIB0gIkNWQzMzk4MzgtNTQxZC00ZWQwLWE5NTAtOTM2Zjc3ODI1NDky2AIF4AIB&sid=f96da1336d70906d23a507a72b3ec29a&aid=304142&checkin=2025-08-04&checkout=2025-08-10&dest_id=-401497&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null')

#localizar e interactuar con los elementos

rejectCookiesButton = driver.find_element(By.ID,'onetrust-reject-all-handler')
rejectCookiesButton.click()

sleep(10)

selectNameHotel = driver.find_element(By.CSS_SELECTOR, "div[data-testid='title']").click()

sleep(5)

allComments = driver.find_element(By.CSS_SELECTOR,"button[data-testid='fr-read-all-reviews']").click()

sleep(10)
