# import the necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import datetime as dt
import seaborn as sns
import spacy
import yfinance as yf
from datetime import timedelta
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import timeit
import time
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

from pandas_datareader import data
# from pages.User import get_data
from forex_python.converter import CurrencyRates


from pages import User, Visualizations

# Create a dictionary of pages
# pages = {
#     "Page 1": User,
#     "Page 2": Visualizations,}

# Create a multiselect widget for selecting pages
# page = st.sidebar.multiselect("Select a page", list(pages.keys()))

# Display the selected page with the appropriate function
# for p in page:
#     pages[p]()


# st.subheader("Today' converting rates")
# st.write(' ')

# c = CurrencyRates()
# list_usd = c.get_rates('USD')
# list_euro = c.get_rates("EUR")
# list_inr = c.get_rates('INR')
# list = ["BITCOIN", 'USD', 'EUR', 'INR']

# option = st.selectbox(
#     'Choose the Currency',
#     list
# )

# if option is 'USD':
#     st.write(pd.DataFrame(list_usd, index=[1]))
    
#     st.line_chart(list_usd)

#     st.write('Trend:')

#     trend = data.DataReader('DEXUSEU', 'fred')
#     st.line_chart(trend)

# elif option is 'EUR':
#     st.write(pd.DataFrame(list_euro, index=[1]))
#     st.line_chart(list_euro)

#     st.write('Trend:')

#     trend = data.DataReader('DEXUSEU', 'fred')
#     st.line_chart(trend)

# elif option is 'INR':
#     st.write(pd.DataFrame(list_inr, index=[1]))
#     st.line_chart(list_inr)

#     st.write('Trend:')

#     trend = data.DataReader('DEXINUS', 'fred')
#     st.line_chart(trend)

# elif option is 'BITCOIN':
#     from forex_python.bitcoin import BtcConverter

#     b = BtcConverter()

#     st.write('Trend:')

#     trend = data.DataReader('CBBCHUSD', 'fred')

#     st.line_chart(trend)

#     st.write('Current price of Bitcoin is $', b.get_latest_price('USD'))


st.subheader('Stocks Today :zap:')
# import requests
# resp = requests.get("https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms")

# from bs4 import BeautifulSoup
# soup = BeautifulSoup(resp.content, features='xml')
# #st.write(soup.findAll('title'))

# nlp = spacy.load("en_core_web_sm")

# headlines =  soup.findAll('title')

# processed_hline = nlp(headlines[4].text)

# companies = []

# for title in headlines:
#     doc = nlp(title.text)
#     for token in doc.ents:
#         if token.label_ == 'ORG':
#             companies.append(token.text)
#         else:
#             pass

# #st.write(companies)

# ## collect various market attributes of a stock
# stock_dict = {
#     'Org': [],
#     'Symbol': [],
#     'currentPrice': [],
#     'dayHigh': [],
#     'dayLow': [],
#     'forwardPE': [],
#     'dividendYield': []
# }

# ## for each company look it up and gather all market data on it
# stocks_df = pd.read_csv("ind_nifty500list.csv")

# for company in companies:
#     try:
#         if stocks_df['Company Name'].str.contains(company).sum():
#             symbol = stocks_df[stocks_df['Company Name'].\
#                                 str.contains(company)]['Symbol'].values[0]
#             org_name = stocks_df[stocks_df['Company Name'].\
#                                 str.contains(company)]['Company Name'].values[0]
#             stock_dict['Org'].append(org_name)
#             stock_dict['Symbol'].append(symbol)
#             stock_info = yf.Ticker(symbol+".NS").info
#             stock_dict['currentPrice'].append(stock_info['currentPrice'])
#             stock_dict['dayHigh'].append(stock_info['dayHigh'])
#             stock_dict['dayLow'].append(stock_info['dayLow'])
#             stock_dict['forwardPE'].append(stock_info['forwardPE'])
#             stock_dict['dividendYield'].append(stock_info['dividendYield'])
#         else:
#             pass
#     except:
#         pass

# ## create a dataframe to display the buzzing stocks
# #pd.DataFrame(stock_dict)
# st.table(stock_dict)


# start_date = pd.datetime.today() - timedelta(days = 1)
# start_date = "2023-01-01"
# ticker = 'GOOGL'
# data = yf.download(ticker, start_date)
# data["Date"] = data.index

# data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]

# st.line_chart(data.Open)

# expander = st.expander("See Table")
# expander.write(
#     data
# )
url = 'https://www.dropbox.com/s/g25jiqpw539q2au/SP500.csv?dl=1'

snp500 = pd.read_csv(url, error_bad_lines=False)

symbols = snp500['Symbol'].sort_values().tolist()

# st.set_page_config(
#     page_title="Market Profile Chart (US S&P 500)",
#     layout="wide")

ticker, i, p = st.columns([5,5,5])

with ticker:
    ticker = st.selectbox(
        'Choose a S&P 500 Stock',
        symbols)

with i:
    i = st.selectbox(
            "Interval in minutes",
            ("1m", "5m", "15m", "30m")
        )
with p:
    p = st.number_input("How many days (1-30)", min_value=1, max_value=30, step=1)

stock = yf.Ticker(ticker)
history_data = stock.history(interval = i, period = str(p) + "d")

prices = history_data['Close']
volumes = history_data['Volume']

lower = prices.min()
upper = prices.max()

prices_ax = np.linspace(lower,upper, num=20)

vol_ax = np.zeros(20)

for i in range(0, len(volumes)):
    if(prices[i] >= prices_ax[0] and prices[i] < prices_ax[1]):
        vol_ax[0] += volumes[i]   
        
    elif(prices[i] >= prices_ax[1] and prices[i] < prices_ax[2]):
        vol_ax[1] += volumes[i]  
        
    elif(prices[i] >= prices_ax[2] and prices[i] < prices_ax[3]):
        vol_ax[2] += volumes[i] 
        
    elif(prices[i] >= prices_ax[3] and prices[i] < prices_ax[4]):
        vol_ax[3] += volumes[i]  
        
    elif(prices[i] >= prices_ax[4] and prices[i] < prices_ax[5]):
        vol_ax[4] += volumes[i]  
        
    elif(prices[i] >= prices_ax[5] and prices[i] < prices_ax[6]):
        vol_ax[5] += volumes[i] 
        
    elif(prices[i] >= prices_ax[6] and prices[i] < prices_ax[7]):
        vol_ax[6] += volumes[i] 

    elif(prices[i] >= prices_ax[7] and prices[i] < prices_ax[8]):
        vol_ax[7] += volumes[i] 

    elif(prices[i] >= prices_ax[8] and prices[i] < prices_ax[9]):
        vol_ax[8] += volumes[i] 

    elif(prices[i] >= prices_ax[9] and prices[i] < prices_ax[10]):
        vol_ax[9] += volumes[i] 

    elif(prices[i] >= prices_ax[10] and prices[i] < prices_ax[11]):
        vol_ax[10] += volumes[i] 

    elif(prices[i] >= prices_ax[11] and prices[i] < prices_ax[12]):
        vol_ax[11] += volumes[i] 

    elif(prices[i] >= prices_ax[12] and prices[i] < prices_ax[13]):
        vol_ax[12] += volumes[i] 

    elif(prices[i] >= prices_ax[13] and prices[i] < prices_ax[14]):
        vol_ax[13] += volumes[i] 

    elif(prices[i] >= prices_ax[14] and prices[i] < prices_ax[15]):
        vol_ax[14] += volumes[i]   
        
    elif(prices[i] >= prices_ax[15] and prices[i] < prices_ax[16]):
        vol_ax[15] += volumes[i] 
        
    elif(prices[i] >= prices_ax[16] and prices[i] < prices_ax[17]):
        vol_ax[16] += volumes[i]         
        
    elif(prices[i] >= prices_ax[17] and prices[i] < prices_ax[18]):
        vol_ax[17] += volumes[i]         
        
    elif(prices[i] >= prices_ax[18] and prices[i] < prices_ax[19]):
        vol_ax[18] += volumes[i] 
    
    else:
        vol_ax[19] += volumes[i]
        
fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.2, 0.8],
        specs=[[{}, {}]],
        horizontal_spacing = 0.01
    
    )

fig.add_trace(
        go.Bar(
                x = vol_ax, 
                y= prices_ax,
                text = np.around(prices_ax,2),
                textposition='auto',
                orientation = 'h'
            ),
        
        row = 1, col =1
    )


dateStr = history_data.index.strftime("%d-%m-%Y %H:%M:%S")

fig.add_trace(
    go.Candlestick(x=dateStr,
                open=history_data['Open'],
                high=history_data['High'],
                low=history_data['Low'],
                close=history_data['Close'],
                yaxis= "y2"
                
            ),
    
        row = 1, col=2
    )
        

fig.update_layout(
    title_text='Market Profile Chart (US S&P 500)', # title of plot
    bargap=0.01, # gap between bars of adjacent location coordinates,
    showlegend=False,
    
    xaxis = dict(
            showticklabels = False
        ),
    yaxis = dict(
            showticklabels = False
        ),
    
    yaxis2 = dict(
            title = "Price (USD)",
            side="right"
        
        )

)

fig.update_yaxes(nticks=20)
fig.update_yaxes(side="right")
fig.update_layout(height=800)

config={
        'modeBarButtonsToAdd': ['drawline']
    }

st.plotly_chart(fig, use_container_width=True, config=config)