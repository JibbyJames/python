# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd

# Read data from all files in /merged directory
car_csv_path = os.getcwd() + "\\data\\car_csvs\\merged\\"
all_files = glob.glob(os.path.join(car_csv_path, "*.csv")) 
df_from_each_file = (pd.read_csv(f) for f in all_files)
car_data   = pd.concat(df_from_each_file, ignore_index=True)

# Get mix/max car id values.
min_id = car_data['vehicle_id'].min()
max_id = car_data['vehicle_id'].max()

# Set vehicle_id as index. Remove previous index.
car_data = car_data.drop('Unnamed: 0', axis=1)
car_data["id"] = car_data["vehicle_id"]
car_data = car_data.set_index(['id'])

# Find out how many in car ID range are null
new_index = list(range(min_id, max_id))
car_data_nans = car_data.reindex(new_index)

car_data_nans["not_null"] = car_data_nans["vehicle_id"].notnull()
car_data_nans['index1'] = car_data_nans.index

hmm = car_data_nans[["index1", "not_null"]]

hmm[10000:].plot(kind="scatter", x="index1", y="not_null", figsize=(15,5))