import pandas as pd
from urllib.parse import urlparse

log_data = pd.read_table('single-tab-file.tab', sep='\t')

# Column of true/false values
homepage_index = (log_data["URI Stem"] == "/")

# Rows of data where URI Stem == '/'
homepage_data = log_data[homepage_index]

# Top 15 Referrers to Homepage
homepage_data['Referrer'].value_counts()[:15]

example_ref_dom = urlparse(log_data['Referrer'][5000]).hostname
                          
def getDomain(url):
    return urlparse(url).hostname

# Create new column of referring domains
log_data['ref_domain'] = log_data['Referrer'].apply(getDomain)

# Top 15 Referring Domains
log_data['ref_domain'].value_counts()[:15]

for x in range(1,101):
    result = str(x) + ": "
    if(x % 3 == 0):
        result += "Fizz"
    if(x % 5 == 0):
        result += "Buzz"
    print(result)