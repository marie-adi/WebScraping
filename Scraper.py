from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
opts.add_argument("--disable-notifications")
opts.add_argument("--disable-blink-features=AutomationControlled")

s = Service(executable_path = 'ChromeDriver.exe')
driver = webdriver.Chrome(service=s, options=opts)

try:
    driver.get('https://www.booking.com/searchresults.es.html?label=gen173nr-1BCAEoggI46AdIM1gEaEaIAQGYAQq4ARfIAQ_YAQHoAQGIAgGoAgO4AuK37b4GwAIB0gIkNWQzMzk4MzgtNTQxZC00ZWQwLWE5NTAtOTM2Zjc3ODI1NDky2AIF4AIB&sid=f96da1336d70906d23a507a72b3ec29a&aid=304142&checkin=2025-08-04&checkout=2025-08-10&dest_id=-401497&dest_type=city&group_adults=null&req_adults=null&no_rooms=null&group_children=null&req_children=null')

    try:
        reject_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler'))
        )
        reject_cookies.click()
    except TimeoutException:
        print("No se encontró el botón de cookies o no fue necesario")

     # Esperar a que se carguen los hoteles
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='title']"))
    )

      # Hacer scroll y cargar todos los resultados
    while True:
        # Hacer scroll hasta abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Espera para cargar contenido nuevo
        
        try:
            # Intentar encontrar y hacer clic en el botón "Cargar más resultados"
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Cargar más resultados')]]"))
            )
            load_more_button.click()
            time.sleep(3)  # Espera a que se carguen los nuevos hoteles
        except (TimeoutException, NoSuchElementException):
            print("No hay más hoteles para cargar.")
            break

    # Extraer los nombres de los hoteles
    hotel_names = set()  # Usamos un conjunto para evitar duplicados
    hotel_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='title']")

    for hotel in hotel_elements:
        if hotel.text.strip():  # Evitar nombres vacíos
            hotel_names.add(hotel.text.strip())

    # Guardar los datos en hoteles.txt
    with open("hoteles.txt", "w", encoding="utf-8") as txt_file:
        for name in sorted(hotel_names):
            txt_file.write(name + "\n")

    # Guardar los datos en hoteles.json
    with open("hoteles.json", "w", encoding="utf-8") as json_file:
        json.dump(sorted(hotel_names), json_file, ensure_ascii=False, indent=4)

    print(f"Se guardaron {len(hotel_names)} hoteles en hoteles.txt y hoteles.json")

except Exception as e:
    print(f"Se produjo un error: {e}")

finally:
    input("Presiona Enter para cerrar el navegador...")
    driver.quit()

