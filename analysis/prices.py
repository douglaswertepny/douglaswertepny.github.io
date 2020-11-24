'''
Created on Nov 24, 2020

Finds the change in preferences by splitting the items into two parts: the expensive and cheap brands
as measured by dpa. It splits them equally by total sales in dollars. Then it plots them as a function
of time in an interactive altair plot. 

@author: Douglas Wertepny
'''
# Import
import pandas as pd
import numpy as np
import altair as alt

########################################################################################
############# Downloads the needed data ################################################
########################################################################################

# File: Sales in dollars
dtype_dic1 = {'date':'str', 'itemno':'str', 'sale_dollars':np.float64}
cols_list1 = ['date','itemno','sale_dollars']
# Imports reduced data set
df_sale = pd.read_csv('data_sets\Iowa_Liquor_Sales.csv', sep= ",",usecols=cols_list1,dtype=dtype_dic1,date_parser=['date'])
df_sale['date']=pd.to_datetime(df_sale['date'])

# File: Items with dpa
dtype_dic2 = {'itemno':'str','im_desc':'str','dpa':np.float64}
cols_list2 = ['itemno','im_desc','dpa']
# Imports reduced data set
df_item = pd.read_csv('data_sets\Iowa_Liquor_Items_dpa.csv', sep= ",",usecols=cols_list2,dtype=dtype_dic2,date_parser=['date'])
df_item = df_item[df_item['dpa']<10**10]

df_total = pd.merge(df_sale,df_item, how='left', left_on='itemno', right_on='itemno')

########################################################################################
############# Sorts into two halves, expensive and cheap, based on dpa #################
########################################################################################

def quartiles(df, number):
    # df has 'itemno', 'sale_dollars', 'dpa'
    seg = df['sale_dollars'].sum()/number
    df = df.sort_values('dpa')
    df['cs']=df['sale_dollars'].cumsum()
    quarts = []
    for i in range(number):
        dft = df[(df['cs'] >= i*seg) & (df['cs'] < (i+1)*seg)]
        quarts.append(dft['itemno'])
    return quarts

def df_quarts(df, quarts):
    # df has at least 'itemno', 'sale_dollars', 'date'
    n = len(quarts)
    dfs = []
    for i in range(n):
        dft = pd.merge(df,quarts[i], how='inner', on='itemno')
        dft = dft.drop('itemno',axis=1).groupby('date',as_index=False).sum()
        dfs.append(dft)
    return dfs

df_quart = df_total.drop(['date','im_desc'],axis=1).groupby(['itemno','dpa'],as_index=False).sum().sort_values('dpa')
quart = quartiles(df_quart, 2)
dfs = df_quarts(df_sale, quart)

########################################################################################
############# Creates the Altair plots #################################################
########################################################################################

days = 90 # halflife of ewm used in plots

dft1 = dfs[0].rename(columns={'sale_dollars':'cheap'}).set_index('date')
dft2 = dfs[1].rename(columns={'sale_dollars':'expensive'}).set_index('date')
df_halves = dft1.join(dft2)
df_diff =df_halves

###################################### Difference Graph ###########################################

df_diff['difference'] = df_diff['expensive'] - df_diff['cheap']
df_diff['difference'] = df_diff['difference'].ewm(days).mean()
df_diff = df_halves.drop(['cheap','expensive'],axis=1)

graph1 = alt.Chart(df_diff.reset_index(), title = 'Change of Preferences').transform_calculate(
    negative='datum.difference < 0'
).mark_area().encode(
    x=alt.X('date', title = 'Date'),
    y=alt.Y('difference', impute={'value': 1}, title = 'Difference (Dollars)'),
    color=alt.Color('negative:N', legend=None, scale=alt.Scale(scheme='set1'),sort='descending')
).interactive()

###################################### Graph plotting both curves ##################################

df_halves['cheap'] = df_halves['cheap'].ewm(days).mean()
df_halves['expensive'] = df_halves['expensive'].ewm(days).mean()
dft1 = df_halves['cheap'].reset_index().rename(columns={'cheap':'data'})
dft1['type'] = 'cheap'
dft2 = df_halves['expensive'].reset_index().rename(columns = {'expensive':'data'})
dft2['type'] = 'expensive'
df_data = pd.concat([dft2,dft1])

graph2 = alt.Chart(df_data.reset_index(), title = 'Expansive and Cheap Liquor Sales').mark_line().encode(
    x=alt.X('date', title = 'Date'),
    y=alt.Y('data', title = 'Sales (Dollars)'),
    color=alt.Color('type', legend=alt.Legend(title="Price of Liquor"), scale=alt.Scale(scheme='set1'))
).interactive()

###################################### Combining the graphs ##########################################

graph3 = alt.hconcat(
    graph1, graph2
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
).configure_axis(
    labelFontSize=14,
    titleFontSize=16
).configure_legend(
    labelFontSize=14,
    titleFontSize=16
).configure_title(
    fontSize=18
)

graph3.save('html/prices.html')

