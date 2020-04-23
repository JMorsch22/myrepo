#!/usr/bin/env python
# coding: utf-8

# In[31]:


import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
#import datetime as dt
import numpy as np
#from itertools import islice
#import urllib
#import dateutil
#import matplotlib.pyplot as plt


# In[2]:


yf.pdr_override()


# In[3]:


sp500_filepath = ('../GA-projects/sp_500.csv')
sp_500_data = pd.read_csv(sp500_filepath)


# In[4]:


sp_500_data.head()


# In[5]:


sp_500_data.info()


# In[6]:


#sp_500_data.Symbol


# In[7]:


s_set = set(sp_500_data.Symbol)


# In[10]:


healthcare_tickers = 'EW BSX ABMD ABT ALGN ZBH SYK MDT HSIC HOLX ISRG BAX BDX COO MTD STE RMD XRAY WAT TFX VAR TMO PKI DGX A IQV LH REGN AMGN ALXN ILMN INCY GILD'


# In[11]:


asset_manager_tickers = 'AMG AMP BEN BK BLK IVZ LM NTRS STT'


# In[13]:


ohlc = pdr.get_data_yahoo(asset_manager_tickers, start="2017-01-01" )


# In[19]:


ohlc['Adj Close'].head()


# In[20]:


ohlc['Adj Close'].tail()


# In[22]:


ohlc['Adj Close'].info()


# In[23]:


ohlc['Adj Close'].describe()


# In[24]:


type(ohlc['Adj Close'])


# In[25]:


am_df = ohlc['Adj Close']


# In[27]:


pd.rolling_corr(am_df['BLK'],am_df['AMG'])


# In[38]:


am_df.plot()


# In[41]:


ROLLING_PERIOD = 22


# In[43]:


returns = np.log(am_df)-np.log(am_df.shift(ROLLING_PERIOD))


# In[82]:


#returns.iloc[ROLLING_PERIOD:].corr()['BLK']


# In[110]:


returns.rolling(ROLLING_PERIOD).corr()


# In[117]:


def multi_period_return(period_returns):
    return np.prod(period_returns + 1) - 1


# In[208]:


pr = am_df.pct_change()


# In[204]:


r = pr.rolling('30D').apply(multi_period_return)


# In[241]:


r[["BLK",'IVZ','AMG','BK','NTRS']].iloc[21:51].corr()


# In[226]:





# In[214]:


r[["BLK",'IVZ','AMG','BK','NTRS']].plot()


# In[138]:


df_corrs = pr['BLK']        .rolling(window=22, min_periods=22)        .corr(other=pr['AMG'])        .dropna()
df_corrs.plot()

# In[142]:


type(df_corrs)


# In[139]:


df_corrs.plot()


# In[155]:


mask = pr.columns!='BLK'
mask = pr.columns[mask]


# In[243]:


(am_df[['BLK','IVZ','AMG','BK','NTRS']]/am_df[['BLK','IVZ','AMG','BK','NTRS']].iloc[-252])[-252:].plot(title="Relative returns")


# In[230]:


df_corrs = pd.DataFrame()
for ticker in ["BLK",'IVZ','AMG','BK','NTRS']:
    temp = r['BLK']        .rolling(window=30, min_periods=30)        .corr(other=r[ticker])        .dropna()
    df_corrs[ticker]=temp
    
df_corrs.head()

# In[220]:


df_corrs.iloc[-252:].plot(title ='Correlation of Blackrock with other Asset Managers is volatile')


# In[195]:


(am_df[['BLK','IVZ','AMG','BK','NTRS']]/am_df[['BLK','IVZ','AMG','BK','NTRS']].iloc[-365])[-365:].plot()#,'IVZ','AMG','BK','NTRS'


# In[ ]:





# In[ ]:




