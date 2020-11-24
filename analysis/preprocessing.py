'''
Created on Nov 24, 2020

Processes the downloaded data before use in analysis.
Finds the dollar per alcohol (dpa) using the 'data_sets/Iowa_Liquor_Items.csv' data for each item.
Saves the data as 'data_sets/Iowa_Liquor_Items_dpa.csv'.
Finds the total amount of sales in dollars, liters and alcohol per date.
Saves the data as 'data_sets/Iowa_Liquor_Sales_data.csv'.
Plots the final results as a sanity check.

@author: Douglas Wertepny
'''
# Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

########################################################################################
############# Calculates dollar per liter of alcohol (dpa) and saves file ##############
########################################################################################

# Loads Iowa_Liquor_Items.csv
cols_list = ['itemno','im_desc','proof','state_bottle_retail','bottle_volume_ml']
dtype_dic = {'itemno':'str','im_desc':'str','proof':np.float64,'state_bottle_retail':np.float64,'bottle_volume_ml':np.float64}
df = pd.read_csv('data_sets/Iowa_Liquor_Items.csv', sep= ",",usecols=cols_list,dtype=dtype_dic)

# Calculates 'dpa'
df['dpa']=df['state_bottle_retail']/(df['bottle_volume_ml']*df['proof']/200000.0)

# Saves new file
df.to_csv('data_sets/Iowa_Liquor_Items_dpa.csv',sep=",",index=False)

########################################################################################
############# Calculates alcohol sold and creates new file #############################
########################################################################################

# Imports reduced data set
cols_list = ['date','itemno','sale_dollars','sale_liters']
dtype_dic = {'itemno':str,'sale_dollars':np.float64,'sale_liters':np.float64}
df = pd.read_csv('data_sets/Iowa_Liquor_Sales.csv', sep= ",",usecols=cols_list,dtype=dtype_dic,date_parser=['date'])
df['date']=pd.to_datetime(df['date'])
df = df.groupby(['date','itemno'],as_index=False).sum()

# Imports items list
cols_list = ['itemno','im_desc','proof']
dtype_dic = {'itemno':str,'proof':np.float64}
df_item = pd.read_csv('data_sets/Iowa_Liquor_Items.csv', sep= ",",usecols=cols_list,dtype=dtype_dic,date_parser=['date'])
df_item = df_item.drop('im_desc',axis=1)

# Normalize volume by proof
df = pd.merge(df, df_item, on='itemno', how='left')
df['sale_alcohol'] = df['sale_liters']*df['proof']/200.0
df = df.drop(['proof','itemno'],axis=1).groupby('date',as_index=False).sum()
print(df)

# Saves data
df.to_csv('data_sets/Iowa_Liquor_Sales_data.csv',sep=",",index=False)

# Plots 
plt.plot(df['date'],df['sale_dollars'].ewm(90).mean(),'k')
plt.plot(df['date'],df['sale_liters'].ewm(90).mean(),'b')
plt.plot(df['date'],df['sale_alcohol'].ewm(90).mean(),'r')
plt.show()