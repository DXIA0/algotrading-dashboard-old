#cd C:\Users\Xiao_D\Documents\GitHub\trading-dashboard

# https://python.plainenglish.io/building-a-simple-stock-screener-using-streamlit-and-python-plotly-library-a6f04a2e40f9

import streamlit as st
import pandas as pd
import requests
#import tweepy
import pandas as pd
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime
import datetime

import yfinance as yf # https://pypi.org/project/yfinance/
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator

#Assign root folders
root_dir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
mod_dir =  root_dir + '\modules'
data_dir =  root_dir + '\modules\data'

#sys.path.insert(0, f'{mod_dir}') #change directory to access the module file
#sys.path.insert(0, f'{root_dir}') #change back to root directory

def get_filepath(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    data_dir =  root_dir + '\modules\data'
    file_path = os.path.join(data_dir, f'{filename}.csv')
    return(file_path)

def pull_stocktwits():
    symbol = st.text_input('Symbol Search', value ='TSLA', max_chars=5)
    st.text("") # add blank line to help readability
    st.image(f'https://finviz.com/chart.ashx?t={symbol}')
    r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json') #call stocktwits api to fetch all snp500 mentions
    data = r.json() #store the result of fetch in var

    #sort data
    for message in data['messages']:
        st.write(message['created_at'], ': ', message['body'])
        st.text("") # add blank line to help readability

st.set_page_config(layout="wide")

def main():

    st.sidebar.title('Navigation')
    option = st.sidebar.selectbox('Dashboard selection', ('Trading Bot', 'News', 'Search'))

    col1, col2, col3, col4 = st.beta_columns(4)
    with col1:
        st.title('Mantis Trading DX BW  /')

    with col2:
        st.title(option) #display dash name

    with col4:
        st.text('')
        if st.button('Refresh'):
            sys.path.append('\modules') #access modules folder

            date = strftime("%H:%M:%S on %Y-%m-%d", gmtime())
            #import gnews
            #import portfolio_news
            st.text(f'Last refreshed: {date}')

    st.text("")
    st.text("")

    if option == 'News':
        #import gnews #pull global news from data file,  get s&p500, nasdaq, djia, vix

        #overall_body_score = gnews.view_gnews_sentiment()
        #st.text('Overall market sentiment score*: ', overall_body_score)
        #st.text('*Based on last 24hr news (GoogleNews)')

        st.text('To Do')

        #import portfolio_news #run module to ensure functions imported
        #run view data function from portfolio news module
        #df_news, df_sentiment = portfolio_news.view_porfolio_sentiment()
        #st.dataframe(df_news)
        #st.text('Finviz Headline Sentiment')
        #st.dataframe(df_sentiment)


    if  option == 'Trading Bot':
        import modules

        st.header("Momentum Scanner Configuration")
        st.text("*information delayed by 15 minutes")
        st.text("")

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            gain_percent = st.number_input('Percentage Change')
        with col2:
            max_last = st.number_input('Maximum Price')
        with col3:
            min_volume = st.number_input('Minimum Volume, Default 50000') # minimum volume

        df_eligible_candidates = modules.get_pregainers(gain_percent, max_last, min_volume)

        st.text("")
        st.text("Eligible Candidates")
        st.dataframe(df_eligible_candidates)

        ##############
        #   Inputs   #
        ##############
        st.text("")
        st.text("")
        st.header("Momentum Technical Analysis")

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            symbol = st.text_input('Symbol Search', value ='TSLA', max_chars=5)
            st.text("") # add blank line to help readability
            today = datetime.date.today()
            before = today - datetime.timedelta(days=700)

        with col2:
            start_date = st.date_input('Start date', before)

        with col3:
            end_date = st.date_input('End date', today)

        if start_date < end_date:
            pass
        else:
            st.error('Error: End date must fall after start date.')

        st.image(f'https://finviz.com/chart.ashx?t={symbol}')

        ##############
        # Stock data #
        ##############

        # Download data
        df_stock_price = yf.download(symbol,start= start_date,end= end_date, progress=False)

        # Bollinger Bands
        indicator_bb = BollingerBands(df_stock_price['Close']) #bollinger bands  are a type of price envelope relative to volatility, default  values are 20 for period, and 2 for s.d
        bb = df_stock_price
        bb['bb_h'] = indicator_bb.bollinger_hband()
        bb['bb_l'] = indicator_bb.bollinger_lband()
        bb = bb[['Close','bb_h','bb_l']]

        # Moving Average Convergence Divergence
        macd = MACD(df_stock_price['Close']).macd()
        # The MACD was developed by Gerald Appel and is probably the most popular price oscillator. It can be used as a generic oscillator for any univariate series, not only price. Typically MACD is set as the difference between the 12-period simple moving average (SMA) and 26-period simple moving average (MACD = 12-period SMA − 26-period SMA), or “fast SMA — slow SMA”. The MACD has a positive value whenever the 12-period SMA is above the 26-period SMA and a negative value when the 12-period SMA is below the 26-period SMA. The more distant the MACD is above or below its baseline indicates that the distance between the two SMAs is growing. Why are the 12-period SMA called the “fast SMA” and the 26-period SMA the “slow SMA”? This is because the 12-period SMA reacts faster to the more recent price changes, than the 26-period SMA.

        # Resistence Strength Indicator
        rsi = RSIIndicator(df_stock_price['Close']).rsi()
        #Introduced by Welles Wilder Jr. in his seminal 1978 book “New Concepts in Technical Trading Systems”, the relative strength index (RSI) becomes a popular momentum indicator. It measures the magnitude of recent price changes to evaluate overbought or oversold conditions. It is displayed as an oscillator and can have a reading from 0 to 100. The general rules are: RSI >= 70: a security is overbought or overvalued and may be primed for a trend reversal or corrective pullback in price. RSI <= 30: an oversold or undervalued condition.

        ###################
        #   Plot   Data   #
        ###################

        # Plot the prices and the bolinger bands

        col1, col2, col3 = st.beta_columns(3)

        with col1:
            col1.header('Bollinger Bands')
            st.line_chart(bb)
            #st.write('The Bollinger Bands are a type of price envelope developed by John Bollinger. They are envelopes plotted at a standard deviation level above and below a simple moving average of the price. Because the distance of the bands is based on standard deviation, they adjust to volatility swings in the underlying price. Bollinger bands help determine whether prices are high or low on a relative basis. They are used in pairs, both upper and lower bands and in conjunction with a moving average. Further, the pair of bands is not intended to be used on its own. Use the pair to confirm signals given with other indicators.')

        progress_bar = st.progress(0)

        with col2:
            # Plot MACD
            col2.header('MACD')
            st.area_chart(macd)

        with col3:
            # Plot RSI
            col3.header('RSI ')
            st.line_chart(rsi)

        # Data of recent days
        st.write('Recent data ')
        st.dataframe(df_stock_price.tail(10))

    if  option == 'Search':
        st.text("")


if __name__ =='__main__':

  main() #calling the main method
