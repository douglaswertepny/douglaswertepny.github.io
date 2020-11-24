'''
Created on Nov 24, 2020

This module imports the files from the Iowa Liquor Sales database using an API.
Processes and creates a pandas dataframe from the imported data.
Groups by 'date' and 'itemno' and sums over 'sale_dollar' and 'sale_liters'

URL of the data base:
https://data.iowa.gov/Sales-Distribution/Iowa-Liquor-Sales/m3tr-qhgy

API end point:
https://data.iowa.gov/resource/m3tr-qhgy.json



@author: Douglas Wertepny
'''

# Needed packages
import pandas as pd
from sodapy import Socrata

# Loads credentials
print('Loading credentials')
client = Socrata("data.iowa.gov",
                 app_token = '____',
                 username= '____',
                 password= '____',
                 timeout=1000)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
print('Downloading File')
results = client.get("m3tr-qhgy", select='date,itemno,sale_dollars,sale_liters', limit=20*10**6)

# Convert to pandas DataFrame and summarizes
print('Processing File with pandas')
df = pd.DataFrame.from_records(results)
df=df.astype({'date':'str','itemno':'str','sale_dollars':'float64','sale_liters':'float64'})
df = df.groupby(['date','itemno'],as_index=False).sum()

# Saves file
df.to_csv('data_sets\Iowa_Liquor_Sales.csv',sep=",",index=False)