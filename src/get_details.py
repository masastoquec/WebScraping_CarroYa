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
from functions import *


# Main function
def main():
    
    print('==== START SCRIPT ====')

    if os.path.exists('data/carroya.json'):
        json_file = open('data/carroya.json','r')
        data = json.load(json_file)
        json_file.close()
    else:
        print('File not found - run extract_data.py first!!')
        
    
    # Load json file
    


if __name__ == '__main__':
    main()