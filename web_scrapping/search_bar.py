import regex as re
import selenium.webdriver as webdriver
import time

from geopy.geocoders import Nominatim
from geopy import distance
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_results(search):

    url = "https://www.envigo.uy"
    browser = webdriver.Chrome("./chromedriver")
    browser.get(url)
    timeout = 15

    ### Clickear en cruz para quitar pop-up inicial:
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

    ### Latitudes y longitudes

    # lat_retiro = browser.find_element_by_id("estimate_pickup_lat").get_attribute('value')
    # lng_retiro = browser.find_element_by_id("estimate_pickup_lng").get_attribute('value')
    # lat_entrega = browser.find_element_by_id("estimate_pickup_lat").get_attribute('value')
    # lng_entrega = browser.find_element_by_id("estimate_pickup_lng").get_attribute('value')

    geolocator = Nominatim(user_agent="sanico")
    coordenadas_retiro = geolocator.geocode(search["retiro"])
    coordenadas_entrega = geolocator.geocode(search["entrega"])
    lat_retiro = coordenadas_retiro.latitude
    lng_retiro = coordenadas_retiro.longitude
    lat_entrega = coordenadas_entrega.latitude
    lng_entrega = coordenadas_entrega.longitude

    coords_1 = (lat_retiro, lng_retiro)
    coords_2 = (lat_entrega, lng_entrega)
    km = distance.geodesic(coords_1, coords_2).km

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
    precio_txt = browser.find_element_by_id("estimate_value_label").text
    patron = re.compile('(?<=\$)\s(.*?)\s(?=IVA)')
    precio = patron.match(precio_txt)
    print(f"""
    Latitud de retiro es: {lat_retiro}
    Longitud de retiro es: {lng_retiro}
    Latitud de entrega es: {lat_entrega}
    Longitud de entrega es: {lng_entrega}
    Kilómetros: {km}
    El precio del envío es de {precio}
    """)
    time.sleep(1)

search = {
    "retiro":"Sir Eugen Millington Drake, Montevideo, Uruguay",
    "entrega":"Mantua, Montevideo, Uruguay",
    "tamano":"medium",
    "cantidad_de_paquetes":2,
    "opcion_de_entrega": "express",
    "cantidad_de_asistentes":3
}

get_results(search)