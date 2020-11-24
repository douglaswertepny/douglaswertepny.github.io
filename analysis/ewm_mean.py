'''
Created on Nov 24, 2020

This file shows the ewm means associated with years 2012 to 2020. This file will consider the end of the previous
year when calculating this. First off it does the rolling mean by day and will plot the years 2012 to 2019 in various
shades of blue while plotting the year 2020 black and bold. The output is a .

@author: Douglas Wertepny
'''
# Import
import pandas as pd
import numpy as np
import altair as alt

########################################################################################
############# Loads needed datafiles ###################################################
########################################################################################

dtype_dic = {'sale_dollars)':np.float64,'sale_liters':np.float64,'sale_alcohol':np.float64}
cols_list = ['date','sale_dollars','sale_liters','sale_alcohol']
cols_rename = {'date':'Date', 'sale_dollars':'Sales (Dollars)', 'sale_liters':'Volume Sold (Liters)','sale_alcohol':'Alcohol Sold (Liters)'}

# Imports reduced data set
df_total = pd.read_csv('data_sets\Iowa_Liquor_Sales_data.csv', sep= ",",usecols=cols_list,dtype=dtype_dic,date_parser=['date'])
df_total['date']=pd.to_datetime(df_total['date'])
df_total=df_total.rename(columns=cols_rename)

########################################################################################
############# Does the ewm rolling mean on the data before plotting ####################
########################################################################################

# Puts the data in the proper format
def rolling_mean_year(df,days):
    # Takes a data frame and creates a new data frame that does an overall rolling mean.
    # It then separates the years and combines them by day of the year.
    df_temp = df.ewm(halflife=days).mean()
    df_temp = pd.concat([df_total['Date'],df_temp],axis=1)
    df_temp['year']=df_temp['Date'].dt.year.astype(str)
    df_temp['day']=df_temp['Date'].dt.dayofyear
    return df_temp

df_sale = rolling_mean_year(df_total.drop('Volume Sold (Liters)',axis=1),90)
df_volume = rolling_mean_year(df_total.drop('Sales (Dollars)',axis=1),90)

df_days = rolling_mean_year(df_total,90).drop('Date',axis=1)
df_sale_days = df_days.drop('Volume Sold (Liters)',axis=1)
df_volume_days = df_days.drop('Sales (Dollars)',axis=1)

########################################################################################
############# Creates the Altair graph #################################################
########################################################################################

graph1 = alt.Chart(df_sale_days, title = 'Daily Sales').mark_line().encode(
    x=alt.X('day', title = 'Day'),
    y=alt.Y('Sales (Dollars)', title = 'Sales (Dollars)'),
    color=alt.Color('year', legend=alt.Legend(title="Year"), scale=alt.Scale(scheme='viridis'),sort='descending')
).interactive()

graph2 = alt.Chart(df_volume_days, title = 'Daily Volume Sold').mark_line().encode(
    x=alt.X('day', title = 'Day'),
    y=alt.Y('Volume Sold (Liters)', title = 'Volume Sold (Liters)'),
    color=alt.Color('year', legend=alt.Legend(title="Year"), scale=alt.Scale(scheme='viridis'),sort='descending')
).interactive()

graph3 = graph1 | graph2

graph4 = alt.Chart(df_sale.reset_index(), title = 'Daily Sales (Overall Trend)').mark_line().encode(
    x=alt.X('Date', title = 'Date'),
    y=alt.Y('Sales (Dollars)', title = 'Sales (Dollars)'),
).interactive()

graph5 = alt.Chart(df_volume.reset_index(), title = 'Daily Volume Sold (Overall Trend)').mark_line().encode(
    x=alt.X('Date', title = 'Date'),
    y=alt.Y('Volume Sold (Liters)', title = 'Volume Sold (Liters)'),
).interactive()

graph6 = graph4 | graph5

graph7 = alt.vconcat(graph3, graph6).configure_axis(
    labelFontSize=14,
    titleFontSize=16
).configure_legend(
    labelFontSize=14,
    titleFontSize=16
).configure_title(
    fontSize=18
)

graph7.save('html/yearly_graph.html')
