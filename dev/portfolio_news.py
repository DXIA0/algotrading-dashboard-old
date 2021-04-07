# -*- coding: utf-8 -*-

# Import libraries------------------------
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from urllib.request import urlopen
from urllib.request import Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_filepath(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    data_dir =  root_dir + '\data'
    file_path = os.path.join(data_dir, f'{filename}.csv')
    return(file_path)

import nltk
#nltk.download('vader_lexicon')

def view_porfolio_sentiment():
    # View Data
    portfolio_data_filename = get_filepath('portfolio_news_data')
    df_news = pd.read_csv(f'{portfolio_data_filename}')

    unique_tickers = df_news['Ticker'].unique().tolist()
    news_dict = {name: df_news.loc[df_news['Ticker'] == name] for name in unique_tickers}

    values = []
    for ticker in unique_tickers:
        dataframe = news_dict[ticker]
        dataframe = dataframe.set_index('Ticker')
        dataframe = dataframe.drop(columns = ['Headline'])

        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)

    df_sentiment = pd.DataFrame(list(zip(unique_tickers, values)), columns =['Ticker', 'Mean Sentiment'])
    df_sentiment = df_sentiment.set_index('Ticker')
    df_sentiment = df_sentiment.sort_values('Mean Sentiment', ascending=False)
    return(df_news, df_sentiment)

def main():
    # Parameters------------------------
    n = 3 #the # of article headlines displayed per ticker to get a flavour
    tickers = ['NIO', 'TSLA', 'PLTR', 'SQ', 'SPLK']

    # Get Data
    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    #News Fetch------------------------

    for ticker in tickers:
        url = finviz_url + ticker
        req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'})
        resp = urlopen(req)
        html = BeautifulSoup(resp, features="lxml")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table


    #Iterate through the news------------------------
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])

    # Sentiment Analysis------------------------
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Date', 'Time', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    news.Headline = news.Headline.str.replace(',', '') #commas will cause errors with csv

    filepath = get_filepath('portfolio_news_data')

    pd.read_csv(f'{filepath}').append(news).drop_duplicates().to_csv(f'{filepath}', index=False) #append new lines to file
    #news.to_csv(f'{filepath}', index=False)

    print('Headlines module run successfully ')

"""Run function"""

if __name__ =='__main__' or '__init__': #if called or initialised as a package
  main() #calling the main method
