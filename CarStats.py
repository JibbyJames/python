import requests
import yaml
import re
import os.path
import pandas as pd
from bs4 import BeautifulSoup

#==============================================================================
# This program scans motors.co.uk pages about a car for the technical specification
# of the car, and loads this data intp
#==============================================================================

def cleanGaVariable(ga_script):
    result = ga_script.split(',template_breakpoint:')[0] + "}"
    result = result.split('window.dataLayer = [')[1]
    result = result.replace("\r", "")
    result = result.replace("\n", "")
    return result

car_urls = {
        "My Polo" : "http://www.motors.co.uk/car-45773657/?i=24&m=sp",   
        "Slavas A3": "http://www.motors.co.uk/car-44579840/?i=17&m=sr",
        "2017 VW Scirrocco": "http://www.motors.co.uk/car-45761697/?i=0&m=scp",
        "2017 Diesel BMW 1": "http://www.motors.co.uk/car-45755523/?i=2&m=srs",
        "2016 Golf TDI GTD": "http://www.motors.co.uk/car-45701270/?i=1&m=srs",
        "2016 Golf TSI GTE": "http://www.motors.co.uk/car-45660596/?i=0&m=srf",
        "2016 A3 TDI S Line": "http://www.motors.co.uk/car-44712036/?i=0&m=srf"
        }

req_headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }

car_pages_dir = os.getcwd() + "\\car_pages\\"

car_list = []

for car in car_urls:    
    # Car_row dict object, start with "Friendly Name" value.
    car_row = {}
    car_row['Friendly Name'] = car
    
    # Fetch HTML Content if it hasn't been saved locally
    fname = car_pages_dir + car + '.html'
    if os.path.isfile(fname) :
        # Read local fine
        with open(fname) as f:
            page = f.read()
        soup = BeautifulSoup(page, 'lxml')
    else:
        # Read web file       
        response = requests.get(car_urls[car], headers=req_headers)
        if(response.status_code == 200):
            page = response.content
            with open(fname, 'wb') as f:
                f.write(page)
            soup = BeautifulSoup(page, 'html.parser')  
    
    # Get all tech specification <li> items
    specs_div = soup.find('div', class_='tech-spec__info')
    spec_items = specs_div.find_all('li')  
    
    # Loop through tech specs, adding key/value to car_row
    for i in range(0, len(spec_items)):
        key = spec_items[i].find(class_='key').get_text()
        value = spec_items[i].find(class_='val').get_text()
        car_row[key] = value
        
    # Extract GA Code, parsing into dict object
    ga_txt = soup.find_all("script")[5].get_text()
    ga_clean = cleanGaVariable(ga_txt)
    ga_code = yaml.load(ga_clean)
    
    # Merge ga_code data into car_row     
    car_row.update(ga_code)

    # Get Parkers star rating at bottom of page
#    rating_div = soup.find('div', class_='parkers__rating')
#    rating = re.search('\d+', str(rating_div))[0]
#    car_row["rating"] = rating   
    
    # Add car_row data to main list of car rows. 
    car_list.append(car_row)
    
car_data = pd.DataFrame(car_list)

#TODO - Get car reviews from somewhere
    

    



