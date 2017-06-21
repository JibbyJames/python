import pandas as pd
from urllib.parse import urlparse

log_data = pd.read_table('single-tab-file.tab', sep='\t')

# Column of true/false values
homepage_index = (log_data["URI Stem"] == "/")

# Rows of data where URI Stem == '/'
homepage_data = log_data[homepage_index]

# Top 15 Referrers to Homepage
homepage_data['Referrer'].value_counts()[:15]