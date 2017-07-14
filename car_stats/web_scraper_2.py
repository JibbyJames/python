import requests
import os.path
import time
import random
import logging
import json
from bs4 import BeautifulSoup

#==============================================================================
# Variables
#==============================================================================
cars_dir = os.getcwd() + "\\data\\car_jsons\\"
car_logfile = os.getcwd() + "\\logs\\cars_2.log"

start_id = 45700000
total_id_count = 100000
chunk_size = 1000
num_of_chunks = int(total_id_count / chunk_size)
time_range_min = 0.25
time_range_max = 0.5
start_chunk = 13

count = 0
delay_total = 0
four_o_fours = 0
no_specs = 0
invalid_json = 0

script_prefix = "m.Store.dispatch( m.Action('setVehicle')("

car_list = []

req_headers = { 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/59.0.3071.86 Safari/537.36" }

#==============================================================================
# Functions
#==============================================================================
def is_scripts_specs_valid(script):
    return ((not script.isspace()) and (script_prefix in script))

def extract_json_string_from_scripts_specs(script):
    result = script.split(script_prefix)[1]
    result = result.split(") );")[0]
    return result


#==============================================================================
# Logging Setup
#==============================================================================
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(20)

fileHandler = logging.FileHandler(car_logfile)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

message = "STARTING JOB: Start Car ID: %s Total ID Count: %s Chunk Size: %s" % (start_id, total_id_count, chunk_size)
logging.info(message)


#==============================================================================
# Start Scraping
#==============================================================================

# Create the list of ids and shuffle them
car_ids = []
for chunk in range(0, num_of_chunks):
    tmp_start_id = start_id + (chunk * chunk_size)
    tmp_end_id = tmp_start_id + chunk_size
    car_ids.append(list(range(tmp_start_id, tmp_end_id)))
    random.shuffle(car_ids[chunk])

# Loop through [total_id_count] car ids, in [chunk_size] chunk sizes.
for chunk in range(start_chunk, int(total_id_count / chunk_size)): 
    
    chunk_filename = "%s_%s_%s_%s" % (start_id, (start_id + total_id_count),
                                      chunk, int(total_id_count / chunk_size))
    chunk_file = cars_dir + chunk_filename + ".json"

    with open(chunk_file, 'a+') as cf:   
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
            scripts_all = soup.findAll('script')
            scripts_specs = str(scripts_all[len(scripts_all) - 4])
            if(is_scripts_specs_valid(scripts_specs)):
                specs_json_string = extract_json_string_from_scripts_specs(scripts_specs)
            else:
                logging.info("   FAIL: Car script block was not on page or invlaid")
                no_specs += 1
                continue
            
            # Check extracted json is valid json
            try:
                specs_json_object = json.loads(specs_json_string)
            except ValueError:
                logging.info("   FAIL: Extracted json was invalid")
                invalid_json += 1
                continue
            
            # Flatten valid json, then write to chunk file
            cf.write(json.dumps(specs_json_object) + "\n")    
            logging.info("   SUCCESS: Successfully extracted car info, added to {}".format(chunk_filename))
    
    # Log current stats to logfile
    message = "CHUNK SUMMARY: Total rows: %s  404s: %s  No Specs: %s \
                InValid-JSON: %s Forced Delay: %s minutes" \
                % (chunk_size, four_o_fours, no_specs, \
                   invalid_json, round((delay_total / 60), 3))    
    logging.info(message)
    no_specs =  delay_total = four_o_fours = invalid_json = 0