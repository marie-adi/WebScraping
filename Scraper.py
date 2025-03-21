from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

    select_hotel = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='title']"))
    )
    select_hotel.click()

    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    
    # Esperar y hacer clic en "Ver todos los comentarios"
    try:
    # Esperar a que la página se cargue completamente
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
    )
    
        # Intentar primero usando el selector data-testid
        try:
            all_comments_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='fr-read-all-reviews']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_comments_button)
            WebDriverWait(driver, 2).until(lambda d: True)  # Pequeña pausa para estabilizar
            all_comments_button.click()
            print("Comentarios cargados con éxito (usando data-testid)")
        except:
            # Si falla, intentar con el texto dentro del span
            try:
                all_comments_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Leer todos los comentarios')]/parent::button"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_comments_button)
                WebDriverWait(driver, 2).until(lambda d: True)  # Pequeña pausa para estabilizar
                all_comments_button.click()
                print("Comentarios cargados con éxito (usando texto del span)")
            except:
                # Si aún falla, intentar con JavaScript directamente
                try:
                    driver.execute_script("""
                        var buttons = document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {
                            if (buttons[i].innerText.includes('Leer todos los comentarios')) {
                                buttons[i].click();
                                return true;
                            }
                        }
                        return false;
                    """)
                    print("Comentarios cargados con éxito (usando JavaScript)")
                except:
                    print("No se pudo encontrar el botón de todos los comentarios")

    except TimeoutException:
            print("No se pudo encontrar el botón de todos los comentarios")

except Exception as e:
    print(f"Se produjo un error: {e}")

finally:
    # Mantener el navegador abierto para verificar resultados
    input("Presiona Enter para cerrar el navegador...")
    driver.quit()