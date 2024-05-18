# url used to scrape data
url_base = 'https://www.carroya.com/automoviles-y-camionetas'
# number of retries in case of error Default 5
retries = 5
# max number of pages to scrape
max_pages = 5
# json file to save data
json_file = f'data/car_list_{max_pages}.json'
csv_file = f'data/car_details_{max_pages}.csv'
# xpath dictionary to scrape data
xpath_dic = {
    ## General response
    'resultados': '//h5[@class="countOffert"]',
    'cards':'//div[@class="new-card"]',
    'cookies':'//div[@id="consent_prompt_submit"]',
    'close_recomendation':'//div[@class="close-recommendation"]',
    ## General atributtes
    'id':'//div[@class="cy-publication-card-ds-milla"]',
    'link':'//div[@class="cy-publication-card-ds-milla__container"]/a',
    'modelo':'//h1[@class="title text"]',
    'version':'//h3[@class="h3P text version"]',
    'precio':'//h1[@class="priceInfo text"]',
    'ciudad':'//div[@class="usageInfo"]/h3[@class="h3P"][1]',
    'km':'//div[@class="usageInfo"]/h3[@class="h3P"][2]',
    'año':'//div[@class="usageInfo"]/h3[@class="h3P yearDetail"]',
    ## Detail attributes
    'key':'//h5[@class="name"]',
    'value':'//h4[@class="description"]',

}


