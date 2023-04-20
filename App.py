import pandas as pd
import numpy as np
import pickle as pk
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import datetime as datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import time 

# title  
st.title('Welcome to Forecastor')

# getting input from user
stocks_name=["RELIANCE.NS","AAPL", "GOOG", "MSFT", "TSLA", "AMZN"]

# created select box so user can choose from it and also it will updated in user_data variable
user_data=st.selectbox('Stocks Name',stocks_name,index=0)

# get stock data from yfinance api
ticker_data=yf.Ticker(user_data)

# then we are taking date time input from user 
start_date=st.date_input('Enter start date',datetime.date.today())
end_date=st.date_input('Enter end date',datetime.date.today())

# after geting user dates then i given to yfinance so it can import the data user want
data=ticker_data.history(period='1d', start=start_date, end=end_date)

data=data.reset_index()

# we keep the main columns
data=data[['Date','Open','High','Low','Close','Volume']]

def get_data(data):
    x=st.write(data.describe(),data.shape)
    return x
   

if st.button('Get Details'):
    with st.spinner('Fetching Data.. '):
        time.sleep(3)
    st.write(data.describe(),data.shape)
    fig=plt.figure(figsize=(12,6))
    plt.plot(data['Volume'])
    st.pyplot(fig)
   
   
def get_50_ma(data):
    st.subheader('50 Days Moving Average' )

    fig = plt.figure(figsize=(12,6))
    data['MA50'] = data['Close'].rolling(50).mean()
    plt.plot(data['Close'], label='Close',)
    plt.plot(data['MA50'], label='MA50')
    plt.legend() 
    plt.xlabel('Date',fontsize=10)
    plt.ylabel('Close',fontsize=10)
   
    return fig

def get_200_ma(data):
    st.subheader('200 Days Moving Average')
  
    fig = plt.figure(figsize=(12,6))
    data['MA200'] = data['Close'].rolling(200).mean()
    plt.plot(data['Close'], label='Close',)
    plt.plot(data['MA200'], label='MA200')
    plt.legend()
    plt.xlabel('Date',fontsize=10)
    plt.ylabel('Close',fontsize=10)
   
    return fig
    
def get_ma(data):
    st.subheader('50 And 200 Days Moving Average' )

    fig = plt.figure(figsize=(12,6))
    data['MA50'] = data['Close'].rolling(50).mean()
    data['MA200'] = data['Close'].rolling(200).mean()
    plt.plot(data['Close'], label='Close')
    plt.plot(data['MA50'], label='MA50')
    plt.plot(data['MA200'], label='MA200')
    plt.legend() 
    plt.xlabel('Date',fontsize=10)
    plt.ylabel('Close',fontsize=10)
   
    return fig


if st.button('Apply'):
    with st.spinner('Creating Visualization...'):
        time.sleep(5)
    st.pyplot(get_50_ma(data))
    st.pyplot(get_200_ma(data))
    st.pyplot(get_ma(data))
    st.subheader('Volume')
    fig= plt.figure(figsize=(12,6))
    plt.plot(data['Volume'], label='Volume')
    plt.xlabel('Volume', fontsize=10)
    plt.xlabel('Date', fontsize=10)
    st.pyplot(fig)
   

def forecast(data):
    try:
        
        model=ExponentialSmoothing(data['Close'],trend='add',seasonal='mul',seasonal_periods=144).fit()
        y=model.forecast(30)
    

        st.subheader('30 Day Forecast')
        fig= plt.figure(figsize=(12,6))
        plt.plot(data['Close'], label='Actual')
        plt.plot(y, label='Forecast')
        plt.legend()
        z=st.pyplot(fig)# display plot in Streamlit
        return z
    
    except ValueError:
        pass
        st.error('Does Not Work With Less Than Two Full Seasonal Cycles In The Data')
    
if st.button('Forecast'):
    with st.spinner('Forcasting......'):
        time.sleep(5)
        forecast(data)

    


    
