import requests
import yaml
import re
import os.path
import pandas as pd
import time
import random
from bs4 import BeautifulSoup

# Set up Logging
import logging

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

rootLogger = logging.getLogger()

rootLogger.setLevel(20)

car_logfile = os.getcwd() + "\\logs\\cars.log"
fileHandler = logging.FileHandler(car_logfile)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

# Function which extracts GA script data in a single JSON object
def cleanGaVariable(ga_script):
    result = ga_script.split(',template_breakpoint:')[0] + "}"
    result = result.split('window.dataLayer = [')[1]
    result = result.replace("\r", "")
    result = result.replace("\n", "")
    return result

req_headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }

cars_dir = os.getcwd() + "\\data\\car_csvs\\"

start_id = 45773053
total_id_count = 1
chunk_size = 1
num_of_chunks = int(total_id_count / chunk_size)
time_range_min = 0.5
time_range_max = 1.5

car_list = []

count = 0;
delay_total = 0;
four_o_fours = 0;
no_specs = 0;

message = "STARTING JOB: Start Car ID: %s Total ID Count: %s Chunk Size: %s" % (start_id, total_id_count, chunk_size)
logging.info(message)

# Create the list of ids and shuffle them
car_ids = []
for chunk in range(0, num_of_chunks):
    tmp_start_id = start_id + (chunk * chunk_size)
    tmp_end_id = tmp_start_id + chunk_size
    car_ids.append(list(range(tmp_start_id, tmp_end_id)))
    random.shuffle(car_ids[chunk])

# Loop through [total_id_count] car ids, in [chunk_size] chunk sizes.
for chunk in range(0, int(total_id_count / chunk_size)): 
    car_list = []    
    for i in range(0, chunk_size):
        
        car_row = {}
        car_id = car_ids[chunk][i]
        url = "http://www.motors.co.uk/car-" + str(car_id)
        
        delay = round(random.uniform(time_range_min, time_range_max), 3)
        delay_total += delay
               
        count += 1
        message = str(count) + ": Fetching URL: " + url
        logging.info(message)
        
        message = "   DELAY: " + str(delay) + " seconds"
        logging.info(message)
        time.sleep(delay)
        
        response = requests.get(url, headers=req_headers)
        if(response.status_code == 200):
            page = response.content
            soup = BeautifulSoup(page, 'html.parser')            
        else:
            logging.info("   FAIL: Returned 404, skipping...")
            four_o_fours += 1
            continue
        
         # Get all tech specification <li> items
        specs_div = soup.find('div', class_='tech-spec__info')
        if(specs_div):
            spec_items = specs_div.find_all('li') 
        else:
            logging.info("   FAIL: Car page had no specifications section, skipping...")
            no_specs += 1
            continue
        
        # Loop through tech specs, adding key/value to car_row
        for i in range(0, len(spec_items)):
            key = spec_items[i].find(class_='key').get_text()
            value = spec_items[i].find(class_='val').get_text()
            car_row[key] = value
            
        # Extract GA Code, parsing into dict object
        pattern = re.compile(r'ga_account')
        ga_txt = soup.find("script", text=pattern).get_text()
        ga_clean = cleanGaVariable(ga_txt)
        ga_code = yaml.load(ga_clean)
        
        # Merge ga_code data into car_row     
        car_row.update(ga_code)
    
        # Get Parkers star rating at bottom of page
#        rating_div = soup.find('div', class_='parkers__rating')
#        rating = re.search('\d+', str(rating_div))[0]
#        car_row["rating"] = rating
        
        # Add car_row data to main list of car rows.
        logging.info("   SUCCESS: Successfully extracted car info. Moving to next page...")
        car_list.append(car_row)       
      
    # With a list of cars of [chunk_size] in car_list, save them to a csv
    logging.info("CHUNK COMPLETE: Saving to .CSV")
    car_data = pd.DataFrame(car_list)
    csv_title = "%s_%s_%s_%s" % (start_id, (start_id + total_id_count), chunk, int(total_id_count / chunk_size))
    csv_file = cars_dir + csv_title + ".csv"
    car_data.to_csv(csv_file)
    
    # Log current stats to a file
    message = "CHUNK SUMMARY: Total rows: %s  404s: %s  No Specs: %s  Forced Delay: %s minutes" % (chunk_size, four_o_fours, no_specs, round((delay_total / 60), 3))
    logging.info(message)
    no_specs = 0
    delay_total = 0
    four_o_fours = 0