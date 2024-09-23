import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



def ini_browser(link:str, xpath_dic:dict, retries=5):
    """ Inicializa el browser y abre la pagina del vehiculo
    link: (str) enlace inicial de la página
    driver: (webdriver) driver del browser selenium
    wait: (WebDriverWait) objeto de espera del driver selenium
    """
    print(f'selenium version: {selenium.__version__}')

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    #options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')

    #service = ChromeService(executable_path='../driver/chromedriver.exe')
    #C:\Users\Msastoqu\OneDrive - Caracol Televisión S.A\Master\TFM\project\driver\chromedriver.exe
    service = ChromeService(executable_path='C:\\Users\\Msastoqu\\OneDrive - Caracol Televisión S.A\\Master\\TFM\\project\\driver\\chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, timeout=10)
    
    # Obtener la versión de ChromeDriver
    chrome_driver_version = driver.capabilities['browserVersion']
    print(f'ChromeDriver version: {chrome_driver_version}')

    driver.implicitly_wait(3) # seconds
    driver.get(link)
    
    print(f'Browser started ====> {driver.title}')

    # Load princial web
    results = 0
    while results == 0:
        results = int(get_element(xpath_dic['resultados'], driver, wait).split(' ')[0].replace('.',''))
        print(f'\tresutlados: {results}')
        if results == 0:
            driver.implicitly_wait(1)
            driver.refresh()

    # click Cookies
    while True:
        try:
            click_element(xpath_dic['cookies'], driver, wait)
            print('=== Cookies clicked ====')
            break
        except:
            print(' === No cookies yet ===')
            driver.implicitly_wait(5)
            driver.refresh()
    driver.implicitly_wait(5)
    return driver, wait




def click_element(xpath_value:str, driver, wait) -> int:
    """ Click en elemento de la pagina"""
    find = 0
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_value)))
        driver.find_element(By.XPATH,value=xpath_value).click()
        find = 1
        #print(f'Elemento encontrado y clickeado \n {xpath_value}')
    except NoSuchElementException as e:
        print(f'==== Error No element {xpath_value} ====')
    except Exception as ex:
        print(f'==== TimeOut element {xpath_value} ====')
    return find


def get_element(xpath_value:str, driver, wait):
    """ Obtiene el texto de un elemento de la pagina
        xpatn_value: (str) xpath del elemento
        driver: (webdriver) driver del browser selenium
        wait: (WebDriverWait) objeto de espera del driver selenium
        texto: (str) texto del primer elemento encontrado
    """
    find = 0
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_value)))
        texto = driver.find_element(By.XPATH,value=xpath_value).text
        find = 1
    except NoSuchElementException as e:
        print(f'==== Error No element {xpath_value} ====')
        return None
    except Exception as ex:
        print(f'==== TimeOut element {xpath_value} ====')
        return None
    return texto


def get_car_details(id,link, xpath_dic, driver, wait, retries=5 , type='link'):
    """ Extrae los detalles del vehiculo
        id: (str) id del vehiculo
        link: (str) link a la pagina del vehiculo
        xpath_dic: (dict) diccionario con los xpath de los elementos a extraer
        driver: (webdriver) driver del browser selenium
        wait: (WebDriverWait) objeto de espera del driver selenium
        retries: (int) numero de intentos para cargar la pagina
        type: (str) tipo de busqueda (id o link)

        car_info: (dict) diccionario con la informacion del vehiculo (modelo, version, precio, ciudad, km, año, etc.
    """
    # carga pagina detalle
    i = 0
    while True:
        try:
            if type == 'link':
                driver.get(link)
            elif type== 'id':
                driver.find_element(By.ID,value=id).click()
            #wait until load detail car page
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "titleContainerDesktop")))
            break
        except NoSuchElementException as e:
            print(f'==== Error No element {i}====')
            i += 1
        except Exception as ex:
            print(f'==== TimeOut element {i}====')
            i += 1
        driver.refresh()
        driver.implicitly_wait(2) # seconds
        if i >= retries:
            break

    car_info = {
        'id':id,
        'link':link,
        'modelo': get_element(xpath_dic['modelo'], driver, wait),
        'version': get_element(xpath_dic['version'], driver, wait),
        'precio': get_element(xpath_dic['precio'], driver, wait),
        'ciudad': get_element(xpath_dic['ciudad'], driver, wait),
        'km': get_element(xpath_dic['km'], driver, wait),
        'año': get_element(xpath_dic['año'], driver, wait),
    } 

    # Extrae las caracteristicas detalladas
    keys = driver.find_elements(By.XPATH,value=xpath_dic['key'])
    list_keys = [key.text for key in keys]

    values = driver.find_elements(By.XPATH,value=xpath_dic['value'])
    list_values = [value.text for value in values] 

    if len(keys) == len(values):
        cars_details = {list_keys[i]: list_values[i] for i in range(len(list_keys))}
        # Unifica la información en el diccionario
        car_info = {**car_info, **cars_details}
    else:
        print(f'Error en la extraccion de detalles {id}')

    # Retorna a la pagina anterior
    driver.back()
    driver.implicitly_wait(2) # seconds

    return car_info


def delete_new_cars(d:dict) -> dict:
    """ Remove dictionary items with 'nuevoficha' in the link"""
    for key in list(d.keys()):
        if 'nuevoficha' in d[key]:
            del d[key]
    new_dict = d
    return new_dict


