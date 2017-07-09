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

#==============================================================================
# car_models contains a list of unique car models, rather than motors.co.uk records
#==============================================================================
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
car_models['model_full'] = car_models.index

polo_id = 45773053
my_polo = car_models[car_models['vehicle_id'] == polo_id]

all_stats = car_data.describe()
#==============================================================================


#==============================================================================
# Show with a scatter graph, the range in id values we have looked through
#==============================================================================
#new_index = list(range(min_id, max_id))
#car_data_nans = car_data.reindex(new_index)
#car_data_nans["not_null"] = car_data_nans["vehicle_id"].notnull()
#car_data_nans['index1'] = car_data_nans.index
#hmm = car_data_nans[["index1", "not_null"]]
#hmm.plot(kind="scatter", x="index1", y="not_null", figsize=(15,5))
#==============================================================================


#==============================================================================
# Print the total unique car count
#==============================================================================
#total_rows = car_data['vehicle_id'].count()
#title_count = car_data['vehicle_title'].nunique()
#print("Total Records: %s  Total Car Titles: %s (%s%%)" 
#      % (total_rows, title_count, round((title_count / total_rows) * 100, 1)))
#
#print("Total Records: %s  Total Car Models: %s (%s%%)" 
#      % (total_rows, len(car_models), round((len(car_models) / total_rows) * 100, 1)))
#==============================================================================


#==============================================================================
# MPG by BHP - Audi and VW as series
#==============================================================================

#mpg_bhp_data = []
#
#make_types = ['Volkswagen','Audi']
#
#for make in make_types: 
#    make_data = car_models['make'] == make
#    mpg_bhp_data.append(go.Scatter(mode="markers",
#                              y=car_models[make_data]['EC Combined (mpg)'],
#                              x=car_models[make_data]['0 to 62 mph (secs)'],
#                              text=car_models[make_data]['model'],
#                              name=make))
#
#mpg_bhp_layout = go.Layout(
#        title = "MPG by 0-60",
#        hovermode = "closest",
#        showlegend = True,
#        yaxis=dict(title="MPG"),
#        xaxis=dict(title="0-60 (secs)"))
#
#fig = go.Figure(data = mpg_bhp_data, layout = mpg_bhp_layout)
#
#py.plot(fig)

#==============================================================================


#==============================================================================
# My Polo shown in a variety of graphs
#==============================================================================

polo_speed = my_polo['0 to 62 mph (secs)'][0]
polo_mpg = my_polo['EC Combined (mpg)'][0]

df_other_cars = car_models.drop(car_models.index[car_models['vehicle_id'] == polo_id])
df_better_cars = df_other_cars[(df_other_cars['0 to 62 mph (secs)'] < (polo_speed / 2))
                                & (df_other_cars['EC Combined (mpg)'] >= polo_mpg)]

better_car_ratio = df_better_cars['make'].value_counts() / df_other_cars['make'].value_counts()

df_other_cars = df_other_cars.drop(df_better_cars.index)


df_better_cars.to_csv("better_cars.csv")

scatter_data = []

scatter_data.append(go.Scatter(mode="markers",
                               y=df_other_cars['EC Combined (mpg)'],
                               x=df_other_cars['0 to 62 mph (secs)'],
                               text=df_other_cars['model_full'],
                               name="Slow Cars"))

scatter_data.append(go.Scatter(mode="markers",
                               y=df_better_cars['EC Combined (mpg)'],
                               x=df_better_cars['0 to 62 mph (secs)'],
                               text=df_better_cars['model_full'],
                               name="Better Cars"))

scatter_data.append(go.Scatter(mode="markers",
                               name="My Polo",
                               y=my_polo['EC Combined (mpg)'],
                               x=my_polo['0 to 62 mph (secs)'],
                               text="My Polo: " + my_polo["model_full"],
                               marker=dict(color='rgba(0, 0, 0)', size=15)))

scatter_layout = dict(hovermode='closest',
              title='0-60 by MPG - My Polo vs Others',
              xaxis=dict(title='0-60'),
              yaxis=dict(title='MPG'))

fig = dict(data=scatter_data, layout=scatter_layout)

plotly.offline.plot(fig, filename="figures\\My Polo - 0-60 by MPG - 100% Quicker & Improved MPG.html");

#==============================================================================
# Older plots - might need later
#==============================================================================
# Count of cars by year
#car_data['vehicle_year'].value_counts().sort_index().plot(kind='bar', rot=45, figsize=[14, 6])

# Distrubution of price by year, on a logarithmic scale.
#price_by_year = car_data.sample(2000).pivot_table(index="vehicle_id", columns='vehicle_year', values="vehicle_price", aggfunc='mean')
#price_by_year.plot(kind='box', figsize=[12,8], stacked=True, colormap='Accent', rot=45, logy=True)


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
#==============================================================================











