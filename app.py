#https://www.youtube.com/watch?v=0ESc1bh3eIg
#15:00

import streamlit as st
import pandas as pd
import requests
import tweepy

def main():
    st.title('XDashboard')

    st.sidebar.title('Navigation')
    option = st.sidebar.selectbox('Dashboard selection', ('News', 'Social', 'Trading'))

    st.header(option) #display dash name
    st.text("")
    st.text("")

    if option == 'News':

        st.title('Social Media Feed')
        st.header('Stocktwits')
        st.text("") # add blank line to help readability
        symbol = st.text_input('Symbol Search', value ='TSLA', max_chars=5)
        st.text("") # add blank line to help readability

        st.image(f'https://finviz.com/chart.ashx?t={symbol}')
        r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json') #call stocktwits api to fetch all snp500 mentions
        data = r.json() #store the result of fetch in var

        #sort data
        for message in data['messages']:
            st.write(message['created_at'], ': ', message['body'])
            st.text("") # add blank line to help readability
if __name__ =='__main__':
  main() #calling the main method
