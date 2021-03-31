#cd C:\Users\Xiao_D\Documents\GitHub\trading-dashboard

#https://www.youtube.com/watch?v=0ESc1bh3eIg
#15:00

import streamlit as st
import pandas as pd
import requests
import tweepy
import pandas as pd
import sys
import os

from time import gmtime, strftime

#Assign root folders
root_dir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
mod_dir =  root_dir + '\modules'
data_dir =  root_dir + '\modules\data'

sys.path.insert(0, f'{mod_dir}') #change directory to access the module file

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
    st.title('XDashboard')

    st.sidebar.title('Navigation')
    option = st.sidebar.selectbox('Dashboard selection', ('News', 'Portfolio', 'Trading', 'Search'))

    st.header(option) #display dash name
    st.text("")
    st.text("")

    if st.button('Refresh'):
        date = strftime("%H:%M:%S on %Y-%m-%d", gmtime())
        import gnews
        import portfolio_news
        st.text(f'Last refreshed: {date}')

    if option == 'News':
        #import gnews
        #pull global news from data file

        st.text('S&P 500 Map Weekly')
        st.image(f'https://finviz.com/futures_charts.ashx?t=ES')
        #https://finviz.com/map.ashx?t=sec&st= #dail;y
        st.text("")

        st.text('Nasdaq')
        st.image(f'https://finviz.com/futures_charts.ashx?t=NQ')
        st.text("") # add blank line to help readability

        st.text('Dow Jones Industrial Average')
        st.image(f'https://finviz.com/futures_charts.ashx?t=YM')
        st.text("") # add blank line to help readability

        st.text('Volatility VIX')
        st.image(f'https://finviz.com/futures_charts.ashx?p=d1&t=VX')
        st.text("") # add blank line to help readability

        #overall_body_score = gnews.view_gnews_sentiment()
        #st.text('Overall market sentiment score*: ', overall_body_score)
        #st.text('*Based on last 24hr news (GoogleNews)')

    if option == 'Portfolio':
        import portfolio_news #run module to ensure functions imported
        #run view data function from portfolio news module
        df_news, df_sentiment = portfolio_news.view_porfolio_sentiment()
        #st.dataframe(df_news)
        st.text('Finviz Headline Sentiment')
        st.dataframe(df_sentiment)

    #if  option == 'Trading':
    if  option == 'Search':
        symbol = st.text_input('Symbol Search', value ='TSLA', max_chars=5)
        st.text("") # add blank line to help readability
        st.image(f'https://finviz.com/chart.ashx?t={symbol}')


if __name__ =='__main__':
  main() #calling the main method
