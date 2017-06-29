# -*- coding: utf-8 -*-
import os
import glob
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import car_columns as cc
import pandas as pd

# Set up graphing library
plotly.tools.set_credentials_file(username='jibbyjames', api_key='odf0iY1IVJsyIAvlP7IQ')

# Read data from all files in /merged directory
car_csv_path = os.getcwd() + "\\data\\car_csvs\\merged\\"
all_files = glob.glob(os.path.join(car_csv_path, "*.csv")) 
all_df = (pd.read_csv(filepath_or_buffer=f, dtype=cc.get_dtypes()) for f in all_files)
car_data = pd.concat(all_df, ignore_index=True)

# Select columns we're interested in analysing.
car_data = car_data[cc.get_main_columns()]

# Get mix/max car id values.
min_id = car_data['vehicle_id'].min()
max_id = car_data['vehicle_id'].max()

# Set vehicle_id as index. Remove previous index.
main_cols = [c for c in car_data.columns if c.lower()[:7] != 'unnamed']
car_data = car_data[main_cols]
car_data["id"] = car_data["vehicle_id"]
car_data = car_data.set_index(['id'])

# Show with a scatter graph, the range in id values we have looked through
#new_index = list(range(min_id, max_id))
#car_data_nans = car_data.reindex(new_index)
#car_data_nans["not_null"] = car_data_nans["vehicle_id"].notnull()
#car_data_nans['index1'] = car_data_nans.index
#hmm = car_data_nans[["index1", "not_null"]]
#hmm.plot(kind="scatter", x="index1", y="not_null", figsize=(15,5))

# car_models contains a list of unique car models, rather than motors.co.uk records
car_data['year'] = car_data['vehicle_year']
car_data['make'] = car_data['vehicle_make']
car_data['model'] = car_data['vehicle_model']
car_data['trim'] = car_data['vehicle_trim']
car_data['fuel_type'] = car_data['vehicle_fuel_type']
car_data['transmission'] = car_data['vehicle_transmission']
car_models = car_data.set_index(['vehicle_year','vehicle_make','vehicle_model','vehicle_trim', 'vehicle_fuel_type', 'vehicle_transmission'])
car_models = car_models[~car_models.index.duplicated(keep='first')]
car_models['model_messy'] = car_models.index
car_models['model_clean'] = car_models['model_messy'].apply(lambda x : str(x).translate(dict.fromkeys(map(ord, u"(,')"))))
car_models = car_models.set_index(['model_clean'])
car_models['model'] = car_models.index

mpg_bhp_data = []

fuel_types = ['Volkswagen','Audi']

for fuel_type in fuel_types: 
    fuel_type_data = car_models['make'] == fuel_type
    mpg_bhp_data.append(go.Scatter(mode="markers",
                              y=car_models[fuel_type_data]['EC Combined (mpg)'],
                              x=car_models[fuel_type_data]['0 to 62 mph (secs)'],
                              text=car_models[fuel_type_data]['model'],
                              name=fuel_type))

mpg_bhp_layout = go.Layout(
        title = "MPG by 0-60",
        hovermode = "closest",
        showlegend = True,
        yaxis=dict(range=[0, 150],title="MPG"),
        xaxis=dict(title="0-60 (secs)"))

fig = go.Figure(data = mpg_bhp_data, layout = mpg_bhp_layout)

py.plot(fig)

# Print the total unique car count
#total_rows = car_data['vehicle_id'].count()
#title_count = car_data['vehicle_title'].nunique()
#print("Total Records: %s  Total Car Titles: %s (%s%%)" 
#      % (total_rows, title_count, round((title_count / total_rows) * 100, 1)))
#
#print("Total Records: %s  Total Car Models: %s (%s%%)" 
#      % (total_rows, len(car_models), round((len(car_models) / total_rows) * 100, 1)))

#car_models.plot(kind='scatter',x='Engine Power - BHP',y='EC Combined (mpg)', ylim=[10,500])

# Count of cars by year
#car_data['vehicle_year'].value_counts().sort_index().plot(kind='bar', rot=45, figsize=[14, 6])

# Distrubution of price by year, on a logarithmic scale.
#price_by_year = car_data.sample(2000).pivot_table(index="vehicle_id", columns='vehicle_year', values="vehicle_price", aggfunc='mean')
#price_by_year.plot(kind='box', figsize=[12,8], stacked=True, colormap='Accent', rot=45, logy=True)

all_stats = car_data.describe()
#top_25 = 20000 #price_stats[6]
#expensive_cars = car_data[car_data['vehicle_price'] >= top_25]
#cars_by_make = pd.concat([car_data['vehicle_make'].value_counts(), 
#                         expensive_cars['vehicle_make'].value_counts()],
#                         axis=1)
#cars_by_make.columns = ["All", "Expensive"]
#cars_by_make['ratio'] = cars_by_make["Expensive"] / cars_by_make["All"]
#ax = cars_by_make['ratio'].fillna(0).sort_values().plot(kind='bar', figsize=[16,6], rot=80)
#ax.grid(zorder=3)

#make_prices = car_data.pivot_table(columns='vehicle_make', values='vehicle_price', aggfunc='describe')
#make_prices['mean'].plot(kind='bar', logy=True)

# Distrubution of price by year, on a logarithmic scale.
#price_by_make = car_data.sample(8000).pivot_table(index="vehicle_id", columns='vehicle_make', values="vehicle_price", aggfunc='mean')
#meds = price_by_make.median()
#meds = meds.sort_values(ascending=False)
#price_by_make = price_by_make[meds.index]
#ax = price_by_make.plot(kind='box', vert=False, figsize=[10,20], stacked=True, colormap='Accent', rot=0, logx=True)
#
#fig = ax.get_figure()
#fig.savefig('car_make_prices.png')

#years = car_data.groupby(['vehicle_make'])['vehicle_year'].describe().unstack()












