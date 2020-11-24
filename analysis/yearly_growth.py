'''
Created on Nov 24, 2020

This file will assume exponential growth for the cummulative sum from 2012 to 2019 and use this to 
project the values for 2020. This shows that 2020 had a much larger growth. Outputs are the rates
of growth and various plots,

@author: Douglas Wertepny
'''
# Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

########################################################################################
############# Does the ewm rolling mean on the data before plotting ####################
########################################################################################

dtype_dic = {'sale_dollars)':np.float64,'sale_liters':np.float64,'sale_alcohol':np.float64}
cols_list = ['date','sale_dollars','sale_liters','sale_alcohol']
cols_rename = {'date':'Date', 'sale_dollars':'Sale (Dollars)', 'sale_liters':'Volume Sold (Liters)','sale_alcohol':'Alcohol Sold (Liters)'}

# Imports reduced data set
df_total = pd.read_csv('data_sets\Iowa_Liquor_Sales_data.csv', sep= ",",usecols=cols_list,dtype=dtype_dic,date_parser=['date'])
df_total['date']=pd.to_datetime(df_total['date'])
df_total=df_total.rename(columns=cols_rename)

########################################################################################
############# Defines the functions used in the fitting and plotting ###################
########################################################################################

def cumsum_year(df):
    # Takes a data frame and creates a new data frame that does cumsum over various years
    df['year']=df['Date'].dt.year
    df['day']=df['Date'].dt.dayofyear
    df_temp=df[['year','Sale (Dollars)','Volume Sold (Liters)','Alcohol Sold (Liters)']]
    df_temp=df_temp.groupby('year').cumsum() #.groupby('year')
    df_temp=pd.concat((df[['day','year']],df_temp),axis=1)
    return df_temp

# Finds the exponential fit to the year 2012 to 2019
def exponential_fit(df,col,day):
    df = cumsum_year(df)
    y=[]
    for x in range(2012,2020):
        y.append(np.interp(day,df[df['year']==x]['day'],df[df['year']==x][col]))
    y=np.log(y)
    linfit, errorfit = np.polyfit(range(2012,2012+len(y)),y,1,cov=True)
    precent = 100*(np.interp(day,df[df['year']==2020]['day'],df[df['year']==2020][col])/np.exp(y[-1])-1)
    return linfit, errorfit, precent

# Projects exponential fit to the choosen year.
def projection_year(df,col,year):
    x_vec = list(range(250,330,5))
    y_vec = []
    for x in x_vec:
        z, _ , _= exponential_fit(df,col,x)
        y = np.exp(z[0]*year+z[1])
        y_vec.append(y)
    return x_vec, y_vec

########################################################################################
############# Does the exponential fitting and prints the results ######################
########################################################################################
# Prints precentage growth results for a given day
fitted_day = 300
linfit, _, precent_sal=exponential_fit(df_total,'Sale (Dollars)',fitted_day)
print('For day '+str(fitted_day)+":")
print('Sale (Dollars):')
print('2012-2019 yearly increase: '+str(round(linfit[0]*100,1))+'%')
print('2019 to 2020 precent increase: '+str(round(precent_sal))+'%')
linfit, _, precent_vol=exponential_fit(df_total,'Volume Sold (Liters)',fitted_day)
print('Volume Sold (Liters):')
print('2012-2019 yearly increase: '+str(round(linfit[0]*100,1))+'%')
print('2019 to 2020 precent increase: '+str(round(precent_vol))+'%')
linfit, _, precent_vol=exponential_fit(df_total,'Alcohol Sold (Liters)',fitted_day)
print('Alcohol Sold (Liters):')
print('2012-2019 yearly increase: '+str(round(linfit[0]*100,1))+'%')
print('2019 to 2020 precent increase: '+str(round(precent_vol))+'%')

########################################################################################
############# Defines the functions used for plotting the various graphs################
########################################################################################

# Start Plots
def plot_expfit(df,col,day):
    # Creates exponential fit graphs
    # chooses name
    if col == 'Sale (Dollars)':
        name = 'sale_'
    elif col == 'Volume Sold (Liters)':
        name = 'vol_'
    elif col == 'Alcohol Sold (Liters)':
        name = 'alc_'
    else:
        pass
    linfit, _, _=exponential_fit(df,col,day)
    df = cumsum_year(df)
    x_axis = list(range(2012,2021))
    y=[]
    for x in x_axis:
        y.append(np.interp(day,df[df['year']==x]['day'],df[df['year']==x][col]))
    y_fit = [(linfit[0]*x+linfit[1]) for x in x_axis]
    plt.plot(x_axis,np.exp(y_fit),color=cm.viridis(.6))
    plt.plot(x_axis,y,'ko')
    plt.title('Exponential Fit of '+col)
    plt.xlabel('Years')
    plt.ylabel(col)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('./images/' + name+'log_fit.png')
    plt.show()
    return

# Plots rest of data
def plot_data(df,col):
    # Creates the cummulative sum plots
    # chooses name
    if col == 'Sale (Dollars)':
        name = 'sale_'
    elif col == 'Volume Sold (Liters)':
        name = 'vol_'
    elif col == 'Alcohol Sold (Liters)':
        name = 'alc_'
    else:
        pass
    # Starts Data analysis
    df = cumsum_year(df)
    # Folded years plot
    year=list(range(2012,2020))
    color=[9.9]+list(range(9,2,-1))
    i=0
    while i < len(year):
        dft=df[df['year']==year[i]]
        plt.plot(dft['day'],dft[col],color=cm.viridis(.1*color[i]),label=str(year[i]))
        i+=1
    dft=df[df['year']==2020]
    plt.plot(dft['day'],dft[col],'k',label=str(2020))
    plt.title('Cumulative Sum of Volume Sold')
    plt.xlabel('Day of Year')
    plt.ylabel(col)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.legend(bbox_to_anchor=(1, .5), loc='center left', ncol=1) # 'upper right'
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.savefig('./images/' + name+'cumsum.png')
    plt.show()
    return

def plot_proj(df,col):
    # Creates the cummulative sum plots
    # chooses name
    if col == 'Sale (Dollars)':
        name = 'sale_'
    elif col == 'Volume Sold (Liters)':
        name = 'vol_'
    elif col == 'Alcohol Sold (Liters)':
        name = 'alc_'
    else:
        pass
    # Starts Data analysis
    vec1 = projection_year(df, col, 2020)
    vec2 = projection_year(df, col, 2017)
    df = cumsum_year(df)
    # Folded years plot
    year=list(range(2012,2020))
    color=[9.9]+list(range(9,2,-1))
    i=0
    while i < len(year):
        dft=df[df['year']==year[i]]
        plt.plot(dft['day'],dft[col],color=cm.viridis(.1*color[i]),label=str(year[i]),alpha=0.5)
        i+=1
    dft=df[df['year']==2020]
    plt.plot(dft['day'],dft[col],'k',label=str(2020),alpha=0.5)
    plt.plot(vec1[:][0],vec1[:][1],'k--',label='2020 - projection')
    plt.plot(vec2[:][0],vec2[:][1],'k--',label='2017 - projection')
    plt.title('Cumulative Sum of Volume Sold (Fits)')
    plt.xlabel('Day of Year')
    plt.xlim(250,330)
    plt.ylabel(col)
    plt.ylim(1*10**7,2.2*10**7) # For Volume Sold
    #plt.ylim(1.2*10**8,3.5*10**8) # For Sale in dollars
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.legend(bbox_to_anchor=(1, .5), loc='center left', ncol=1) # 'upper right'
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.savefig('./images/' + name+'proj.png')
    plt.show()
    return

########################################################################################
############# Does the actual plotting #################################################
########################################################################################

for x in ['Volume Sold (Liters)']:# 'Sale (Dollars)', 'Volume Sold (Liters)'
    plot_expfit(df_total,x,fitted_day)
    plot_data(df_total,x)
    plot_proj(df_total,x)
    