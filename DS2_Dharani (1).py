#!/usr/bin/env python
# coding: utf-8

# # Library Import

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# # Function to Read Data and Preparing Dataframes

# In[3]:


# List of Countries Taken
taken_cntr=["India","China", "Brazil", "Afghanistan", "Germany", "Iraq", "United Arab Emirates","Russian Federation"]
# List of Indicators Taken
indic=["Electricity production from oil sources (% of total)", "CO2 emissions (metric tons per capita)"]
# List of Indicator Names Taken
names=["Electricity Production","CO2 Emission"]
print(*taken_cntr,sep=", ")
print(*indic,sep=", ")


# In[4]:


def colprep(df,f1,f2):   # function will take dataframe and two features and will calculate ration between indicators
    df['Ratio']=df[f1]/dtfrm[f2]   # calculate ratio between CO2 emissions and Electricity production
    return df   # return data


# In[5]:


def dataprep(ecfl):   # fucntion to prepare data
    fe1,fe2='Indicator Name','Country Name'     # column names for data preparation
    ecfl=ecfl[(ecfl[fe1]==indic[0])|((ecfl[fe1]==indic[1]))]    # filter data with the selecetd countries and indicators
    fltr=ecfl[fe2].isin(taken_cntr)     # check if the filtered data with countries exists in the collected world bank data
    ecfl=ecfl[fltr]     # apply filter to data
    cntr=ecfl[fe2].tolist()     # take indicators into list from data
    indx=ecfl[fe1].tolist()     # take contries into list  from data
    d1=[]   # take empty list
    for i in range(len(indx)):
        d1.append(cntr[i])      # store data regarding countries
    ecfl.insert(4,"Countries",d1)    # insert column 'Countries' in data at position 4th
    return ecfl   # return data


# In[6]:


def readdata(csv):    # fucntion to read data
    eco=pd.read_csv(csv,engine='python',skiprows=3)    # read data  
    eco=eco.fillna(eco.median())    # clean missing values of data using median
    yrcols=eco.columns.tolist()[4:-1]   # take years into list
    eco=dataprep(eco)    # call 'dataprep' fucntion
    eco1=eco.T.iloc[4:][:-1]    # Transpose data using '.T' attribute of pandas
    eco=eco.reset_index(drop=True).drop(['Unnamed: 65','Country Code','Indicator Code','Countries'],axis=1) # remove columns whcih are not required
    eco1.columns=eco1.iloc[0]   # take first row as it contain names of olumns
    eco1=eco1.iloc[1:] # skip 1 row as it has been taken for column names
    eco1['Year']=yrcols     # insert year column in data
    eco1=eco1.set_index("Year")    # set year as index
    return eco,eco1  


# In[7]:


csvfile="API_19_DS2_en_csv_v2_3931355.csv"
data,data1=readdata(csvfile)


# In[8]:


data.head()   # First Data with Year Column


# In[9]:


data1.head()   # second data with country column


# In[10]:


data.describe()


# In[24]:


data1.describe().T


# In[37]:


print("Data Skewness")
data1.skew()


# In[42]:


data1.skew().plot(kind='line',linestyle="--",marker="*",color="r",figsize=(7,4),title="Data Skewness")
plt.xticks(rotation=90)
plt.show()


# In[26]:


data1.kurtosis()


# In[44]:


data1.kurtosis().plot(kind='line',linestyle="dashdot",marker="D",color="g",figsize=(7,4),title="Data Kurtosis")
plt.xticks(rotation=90)
plt.show()


# # Data Analysis

# In[12]:


def tsviz(df,nm):  # function for time series plotting
    df.plot(kind='line',figsize=(9,5))    # plotting by features (nm) from dataframe by years
    plt.title("{} for Countries by Year".format(nm),fontsize=22,color="b")    # title
    plt.ylabel("{}".format(nm),fontsize=18,color="b")    # ylabel assignment
    plt.xlabel("Year",fontsize=18,color="b")      # xlabel assignment
    plt.grid()     # gridding the plot
    plt.show()    # show plot


# In[13]:


tsviz(data1.loc[:,~data1.columns.duplicated()],"Electricity Production")
tsviz(data1.loc[:,data1.columns.duplicated()],"CO2 Emission")


# In[14]:


val1,val2=[],[]    # take empty list for storing average values
print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
for i in range(len(taken_cntr)):
    dftmp=data[data['Country Name']==taken_cntr[i]]    # filter by countru na,es
    dftmp=dftmp.drop('Indicator Name',axis=1)    # remove Indicator Name 
    print("                           Statistics for {}".format(taken_cntr[i]))   # printing statsitics
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("{} (Average) for {} => {}".format(names[0],taken_cntr[i],round(dftmp.iloc[0,1:].mean(),2)))  # Print Average values for Electricity Production
    print("{} (Average) for {} => {}".format(names[1],taken_cntr[i],round(dftmp.iloc[1,1:].mean(),2)))  # Print Average values for CO2 Emission
    print("{} (Max) for {} => {}".format(names[0],taken_cntr[i],round(dftmp.iloc[0,1:].max(),2)))  # Print Max values for Electricity Production
    print("{} (Max) for {} => {}".format(names[1],taken_cntr[i],round(dftmp.iloc[1,1:].max(),2)))  # Print Max values for CO2 Emission
    print("{} (Min) for {} => {}".format(names[0],taken_cntr[i],round(dftmp.iloc[0,1:].min(),2)))  # Print Min values for Electricity Production
    print("{} (Min) for {} => {}".format(names[1],taken_cntr[i],round(dftmp.iloc[1,1:].min(),2)))  # Print Min values for CO2 Emission
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    val1.append(round(dftmp.iloc[0,1:].mean(),2))
    val2.append(round(dftmp.iloc[1,1:].mean(),2))
dtfrm=pd.DataFrame({"Country":taken_cntr,"{}".format(names[0]):val1,"{}".format(names[1]):val2})
dtfrm=dtfrm.sort_values(by="{}".format(names[0]))
dtfrm=dtfrm.set_index("Country")   # fiunalise data for countries with taken induicator value


# In[15]:


dtfrm=colprep(dtfrm,'CO2 Emission','Electricity Production')    # call 'colprep' function to calculatr ration between CO2 emission and electricity production
dtfrm


# In[16]:


def compplot(df):
    df.plot(kind='area',figsize=(8,4),color=["g","m","c"])
    plt.title("Comparison of Electricity Production and \nCO2 Emission by Countries",fontsize=22,color="b")    # title
    plt.xlabel("Countries",fontsize=18,color="b")    # ylabel assignment
    plt.xticks(rotation=90)    # rotating x axis
    plt.ylabel("Value",fontsize=18,color="b")      # xlabel assignment
    plt.grid()     # gridding the plot
    plt.show()    # show plot


# In[17]:


compplot(dtfrm)


# In[18]:


def corrplot(df,cmp):
    plt.figure(figsize=(8,4))
    plt.title("Correlation of Indicators",fontsize=22,color="b")    # title
    sns.heatmap(df.corr(),annot=True,fmt="0.4f",cmap=cmp)   # visulizijg heatmap of correlation using seaborn
    plt.yticks(rotation=-0)    # rotating x axis
    plt.show()  # show plotting


# In[19]:


corrplot(dtfrm.iloc[:,:2],"Blues")


# In[45]:


def fetplot(df,fet):
    plt.figure(figsize=(8,4))
    plt.plot(dtfrm[fet],"m--")
    plt.plot(dtfrm[fet],"Db")
    plt.title("{} by Country".format(fet),fontsize=22,color="b")    # title
    plt.xlabel("Country",fontsize=18,color="b")    # ylabel assignment
    plt.xticks(rotation=90)    # rotating x axis
    plt.ylabel("{}".format(fet),fontsize=18,color="b")      # xlabel assignment
    plt.grid()     # gridding the plot
    plt.show()    # show plot


# In[46]:


fetplot(dtfrm,"Electricity Production")
fetplot(dtfrm,"CO2 Emission")


# In[47]:


def topcntrviz(df,fet):
    df=df.sort_values(by=fet,ascending=False)
    plt.figure(figsize=(6,3))
    plt.bar(df[:3].index,df[:3][fet],color=["b","m","c"])
    plt.title("Top 3 Countries with {}".format(fet),fontsize=18,color="b")    # title
    plt.xlabel("Country",fontsize=14,color="b")    # ylabel assignment
    plt.ylabel("{}".format(fet),fontsize=14,color="b")      # xlabel assignment
    plt.grid()     # gridding the plot
    plt.show()    # show plot
    
    df=df.sort_values(by=fet,ascending=True)
    plt.figure(figsize=(6,3))
    plt.bar(df[:3].index,df[:3][fet],color=["b","m","c"])
    plt.title("Least 3 Countries with {}".format(fet),fontsize=18,color="b")    # title
    plt.xlabel("Country",fontsize=14,color="b")    # ylabel assignment
    plt.ylabel("{}".format(fet),fontsize=14,color="b")      # xlabel assignment
    plt.grid()     # gridding the plot
    plt.show()    # show plot


# In[48]:


topcntrviz(dtfrm,"Electricity Production")
topcntrviz(dtfrm,"CO2 Emission")


# In[ ]:




