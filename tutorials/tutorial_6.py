# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

flight_data = pd.read_table('flights.csv', sep=',')
del(flight_data['Unnamed: 13'])

flight_data["DELAYED"] = flight_data["ARR_DELAY"].apply(lambda x: x > 0)

delayed_by_carrier = flight_data.groupby(['UNIQUE_CARRIER','DELAYED']).size().unstack().reset_index()

delayed_by_carrier['flights_count'] = (delayed_by_carrier[False] + delayed_by_carrier[True])

delayed_by_carrier['proportion_delayed'] = delayed_by_carrier[True] / delayed_by_carrier['flights_count']

delayed_by_carrier = delayed_by_carrier.sort_values('proportion_delayed', ascending=False)

mean_del_carrier = flight_data.pivot_table(columns='UNIQUE_CARRIER', values='ARR_DELAY').sort_values(ascending=False)

chi_town = flight_data[flight_data['ORIGIN'] == 'ORD']['ARR_DELAY']
chi_town_describe = chi_town.describe()

bin_values = np.arange(start=-50, stop=200, step=10)
wn_carrier = flight_data[flight_data['UNIQUE_CARRIER'] == 'WN']
#wn_carrier['ARR_DELAY'].hist(bins=bin_values, figsize=[14,6])

wn_aa_airlines = flight_data[flight_data['UNIQUE_CARRIER'].isin(['WN','AA'])]
group_carriers = wn_aa_airlines.groupby('UNIQUE_CARRIER')['ARR_DELAY']
group_carriers.plot(kind='hist', bins=bin_values, figsize=[12,6], alpha=.4, legend=True)
