import selenium.webdriver as webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_results(search):

    url = "https://www.envigo.uy"
    browser = webdriver.Chrome("./chromedriver")
    browser.get(url)
    timeout = 15

    browser.find_element_by_xpath("//div[@id='modal-content']/div/button").click()

    ### Ingresar dirección de retiro:
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.ID, 'estimate_pickup_address'))
    )
    retiro = browser.find_element_by_id("estimate_pickup_address")
    retiro.send_keys(search['retiro'])
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='pac-container pac-logo hdpi']/div[1]"))
    )
    browser.find_element_by_xpath("//div[@class='pac-container pac-logo hdpi']/div[1]").click()

    ### Ingresar dirección de entrega:
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.ID, 'estimate_delivery_address'))
    )
    entrega = browser.find_element_by_id("estimate_delivery_address")
    entrega.send_keys(search['entrega'])
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='pac-container pac-logo hdpi']/div[1]"))
    )
    browser.find_element_by_xpath("//div[@class='pac-container pac-logo hdpi']/div[1]").click()

    ### Ingresar tamaño de paquete:
    if search["tamano"]=="small":
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.ID, 'estimate_package_size_small'))
        )
        browser.find_element_by_xpath("//div[@id='package-size']/div/label[1]").click()
    elif search["tamano"]=="medium":
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.ID, 'estimate_package_size_medium'))
        )
        browser.find_element_by_xpath("//div[@id='package-size']/div/label[2]").click()
    elif search["tamano"]=="large":
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.ID, 'estimate_package_size_large'))
        )
        browser.find_element_by_xpath("//div[@id='package-size']/div/label[3]").click()
    else:
        raise Exception('Valor no válido')

    ### Ingresar cantidad de paquetes:
    if search["cantidad_de_paquetes"]>=0 and search["cantidad_de_paquetes"]<=10:
        cantidad_de_paquetes = browser.find_element_by_id("estimate_number_of_packages")
        cantidad_de_paquetes.send_keys(search["cantidad_de_paquetes"])
    else:
        raise Exception('Valor no válido')

    ### Ingresar opción de entrega:
    if search["opcion_de_entrega"]=="express":
        browser.find_element_by_xpath("//div[@id='estimate_form_container']/div[2]/div[14]/div/label[1]").click()
    elif search["opcion_de_entrega"]=="coordinado":
        browser.find_element_by_xpath("//div[@id='estimate_form_container']/div[2]/div[14]/div/label[2]").click()

    ### Ingresar cantidad de asistentes:
    if search["cantidad_de_asistentes"]>=0 and search["cantidad_de_asistentes"]<=5:
        cantidad_de_asistentes = browser.find_element_by_id("estimate_laborer_number")
        cantidad_de_asistentes.send_keys(search["cantidad_de_asistentes"])
    else:
        raise Exception('Valor no válido')

    time.sleep(1)
    precio = browser.find_element_by_id("estimate_value_label").text
    print(f"El precio del envío es de {precio}")
    time.sleep(3)

search = {
"retiro":"Sir Eugen Millington Drake, Montevideo Departamento de Montevideo, Uruguay",
"entrega":"Mantua, Montevideo Departamento de Montevideo, Uruguay",
"tamano":"medium",
"cantidad_de_paquetes":7,
"opcion_de_entrega": "express",
"cantidad_de_asistentes":3
}

get_results(search)