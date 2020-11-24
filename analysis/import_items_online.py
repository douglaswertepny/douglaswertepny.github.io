'''
Created on Nov 24, 2020

This module imports the files from the Iowa Liquor Products database using an API.
Creates a pandas dataframe from the imported data.

URL of the data base:
https://data.iowa.gov/Sales-Distribution/Iowa-Liquor-Products/gckp-fe7r

API end point:
https://data.iowa.gov/resource/gckp-fe7r.json

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

# Downloads file
print('Downloading File')
results = client.get("gckp-fe7r", select='itemno,im_desc,proof,state_bottle_retail,bottle_volume_ml',limit=20*10**6)

# Convert to pandas DataFrame
print('Processing File with pandas')
df = pd.DataFrame.from_records(results)
df=df.astype({'itemno':'str','im_desc':'str','proof':'float64','state_bottle_retail':'float64','bottle_volume_ml':'float64'})

# Saves data file
df.to_csv('data_sets\Iowa_Liquor_Items.csv',sep=",",index=False)