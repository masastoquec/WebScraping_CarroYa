# -*- coding: latin-1 -*-

# Import libraries
import json
import datetime
import time
import pandas as pd
import logging
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
def main():
    
    print('==== START SCRIPT ====')
    # Initialize browser url from definitions
    driver, wait = ini_browser(url_base,xpath_dic,retries)


    # get the current date and time
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)

    total_car_list = []

        
    for page in range(max_pages):
        # Change pages
        url = url_base + f'?page={page+1}'
        driver.get(url)

        
        try:
            element_present = EC.presence_of_element_located((By.XPATH, xpath_dic['cards']))
            WebDriverWait(driver, timeout=10).until(element_present)
        except:
            print(f'Error or Timeout waiting page {url}')
            driver.refresh()
            driver.implicitly_wait(10) # seconds
            
        

        # Exctract  ids and links from every item
        ids = driver.find_elements(By.XPATH,value=xpath_dic['id'])
        list_ids = [item.get_attribute('id') for item in ids]
        items = len(ids)
        print(f'=== Page{page+1} === {url} === {items} items')


        links = driver.find_elements(By.XPATH,value=xpath_dic['link'])
        list_links = [link.get_attribute('href') for link in links] 

        if len(ids) == len(links):
            cars = list(zip(list_ids,list_links)) 
            total_car_list = total_car_list + cars
        else:
            print('==== Error getting links and ids ====')

    print(f'===== TOTAL ITEMS:{len(total_car_list)}')

    # get the current date and time
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)

    # Save data to json
    with open(f'./{json_file}', 'w') as file:
        json.dump(dict(total_car_list), file)



if __name__ == "__main__":
    main()