# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

flight_data = pd.read_table('flights.csv', sep=',')
del(flight_data['Unnamed: 13'])

top_delayed = flight_data.sort_values(by='ARR_DELAY',ascending=False)[:10]

flight_data['DELAYED'] = flight_data['ARR_DELAY'].apply(lambda x: x > 0)
flight_data['SUPER_DELAYED'] = flight_data['ARR_DELAY'].apply(lambda x: x > 20)

delayed = flight_data["DELAYED"].value_counts()[1]
super_delayed = flight_data["SUPER_DELAYED"].value_counts()[1]

total_flights = len(flight_data)
#print("Delayed Flights: " + str(round(float(delayed/total_flights) * 100, 2)) + "% of Total")

group_by_carrier = flight_data.groupby(["UNIQUE_CARRIER", "DELAYED"])

count_delays_by_carrier = group_by_carrier.size().unstack()
#count_delays_by_carrier["Delay_Perc"] = round(count_delays_by_carrier[1] / (count_delays_by_carrier[0] + count_delays_by_carrier[1]) * 100, 2)
#count_delays_by_carrier = count_delays_by_carrier.sort_values(by="Delay_Perc", ascending=False)

#count_delays_by_carrier.plot(kind='barh', stacked=True, figsize=[16,6], colormap='winter')

flights_by_carrier = flight_data.pivot_table(index='FL_DATE', columns='UNIQUE_CARRIER', values='ARR_DELAY', aggfunc='mean')

delays_list = ['CARRIER_DELAY','WEATHER_DELAY','NAS_DELAY','SECURITY_DELAY','LATE_AIRCRAFT_DELAY']
flight_delays_by_day = flight_data.pivot_table(index='FL_DATE', values=delays_list, aggfunc='sum')

#flight_delays_by_day.plot(kind='area', figsize=[16,6], stacked=True, colormap='autumn')

flight_delays_by_carrier = flight_data.pivot_table(index="FL_DATE", columns='UNIQUE_CARRIER', values="ARR_DELAY", aggfunc='sum')
flight_delays_by_carrier.plot(kind='box', figsize=[16,8], stacked=True, colormap='Accent', rot=45)
