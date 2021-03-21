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

    #if option == 'News':
        #pull global news from data file

    if option == 'Portfolio':

        # View Data
        portfolio_data_filename = get_filepath('portfolio_news_data')

        df_news = pd.read_csv(f'{portfolio_data_filename}')

        st.dataframe(df_news)

        unique_tickers = df_news['Ticker'].unique().tolist()
        news_dict = {name: df_news.loc[df_news['Ticker'] == name] for name in unique_ticker}

        values = []
        for ticker in unique_tickers:
            dataframe = news_dict[ticker]
            dataframe = dataframe.set_index('Ticker')
            dataframe = dataframe.drop(columns = ['Headline'])

            mean = round(dataframe['compound'].mean(), 2)
            values.append(mean)

        df_sentiment = pd.DataFrame(list(zip(tickers, values)), columns =['Ticker', 'Mean Sentiment'])
        df_sentiment = df_sentiment.set_index('Ticker')
        df_sentiment = df_sentiment.sort_values('Mean Sentiment', ascending=False)

        print ('\n')
        print (df_sentiment)

    #if  option == 'Trading':
    if  option == 'Search':
        symbol = st.text_input('Symbol Search', value ='TSLA', max_chars=5)
        st.text("") # add blank line to help readability
        st.image(f'https://finviz.com/chart.ashx?t={symbol}')


if __name__ =='__main__':
  main() #calling the main method
