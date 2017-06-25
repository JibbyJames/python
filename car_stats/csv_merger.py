# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd

path = os.getcwd() + "\\data\\car_csvs\\to_be_merged\\"
all_files = glob.glob(os.path.join(path, "*.csv")) 

df_from_each_file = (pd.read_csv(filepath_or_buffer =f, encoding='latin1') for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

min_id = concatenated_df['vehicle_id'].min()
max_id = concatenated_df['vehicle_id'].max()
count = concatenated_df['vehicle_id'].count()

filepath = os.getcwd() + "\\data\\car_csvs\\merged\\"
filename = "%s_%s_%s.csv" % (min_id, max_id, count)

concatenated_df.to_csv(filepath + filename)