# -*- coding: latin-1 -*-

# Import libraries
import json
import datetime
import time
import pandas as pd
import os

import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# import custom definitions and functions
from definitions import *
from functions_ws import *


# Main function
def main() -> None:
    
    print('==== START SCRIPT ====')

    print(f'=== Currect Directory - {os.getcwd()} ===')
    file = f'./{json_file}'
    
    if os.path.exists(file):
        with open(file) as f:
            d = f.readlines()
            dic = json.loads(d[0])
            print(f'=== Items list:{len(dic)} ===')
            cars_urls = delete_new_cars(dic)
            print(f'=== Items to get details (only used cars):{len(cars_urls)} ===')
    else:
        print('File not found - run extract_data.py first!! and then run again this script')
        return
        
    # Start borwser
    driver, wait = ini_browser(url_base, xpath_dic= xpath_dic)
    total_car_detail = []

    for key, value in cars_urls.items():
        print(f"{key}, {value}")
        try:
            # Entra pagina de detalles del vehiculo
            temp_car = get_car_details(key,value,xpath_dic,driver,wait, retries=retries, type='link')
            total_car_detail.append(temp_car)
        except:
            print('==== Error en la extraccion de detalles')
        print(f'\tItems: {len(total_car_detail)}')

    df = pd.DataFrame(total_car_detail)
    print(f'size: {df.shape} - columns: {df.columns}' )

    # Save data to csv
    df.to_csv(f'./{csv_file}',index=False)
    print(f'=== Data saved to {csv_file} ===')
    


if __name__ == '__main__':
    main()