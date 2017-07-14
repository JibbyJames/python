# -*- coding: utf-8 -*-
import os
import pandas as pd

car_json_path = os.getcwd() + "\\data\\car_jsons\\merged\\4500000_4580000_11924.json"

car_data = pd.read_json(car_json_path, orient = 'records', lines=True)