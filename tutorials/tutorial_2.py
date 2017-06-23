import numpy as np

city_population = {
  'Tokyo': 13350000, # a key-value pair
  'Los Angeles': 18550000,
  'New York City': 8400000,
  'San Francisco': 1837442,
}

mean_vals = np.mean(list(city_population.values()))