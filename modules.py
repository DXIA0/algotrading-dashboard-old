#to do
#1. implement another screener https://www.tradingview.com/screener/
# https://www.tradingview.com/screener/
# https://thestockmarketwatch.com/markets/topstocks/

#https://towardsdatascience.com/making-a-stock-screener-with-python-4f591b198261
# https://github.com/jacksonhorton/marketTrader
# pre and post market stats https://github.com/ivanstruk/Backtesting-Pre-Market-Price-Action
# source https://iexcloud.io/docs/api/#chart

import pandas as pd
import requests
import yfinance as yf
import talib


################################################
########## Premarket Gappers ###################
################################################

def get_pregainers(gain_percent, max_last, min_volume):
    #https://www.tradingview.com/screener/

    #gain_percent = 10 # at least how many percent gain
    #max_last = 10 # maximum price
    #min_volume = 50000 # minimum volume

    #float_range = [2000000,15000000] # size of float
    #  if flt > FLOAT_BTW[0] and flt < FLOAT_BTW[1]:
    #    return True
    #  else:
    #    return False

    url = 'https://thestockmarketwatch.com/markets/pre-market/today.aspx'
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)

    df_temp = pd.read_html(r.text) #fetch table from "thestockmarketwatch.com"
    df_pregainers = df_temp[1]

    df_pregainers['%Chg'] = df_pregainers['%Chg'].str.strip('%') #reformat all percent
    df_pregainers['%Chg'] = pd.to_numeric(df_pregainers['%Chg'])
    df_pregainers['Last'] = df_pregainers['Last'].str.strip('$')
    df_pregainers['Last'] = pd.to_numeric(df_pregainers['Last'])
    df_pregainers['Volume'] = pd.to_numeric(df_pregainers['Volume'])

    df_pregainers.rename(columns={"Last":"Last Price ($)", "%Chg":"Change (%)", "Symb":"Symbol"}, inplace=True) #rename columns

    df_eligible_candidates = pd.DataFrame(columns = ["Change (%)", "Last Price ($)", "Symbol", "Company", "Volume"])

    for index, row in df_pregainers.iterrows():
        if row['Change (%)'] > gain_percent and                row['Last Price ($)'] < max_last and                row['Volume'] > min_volume:
              df_eligible_candidates = df_eligible_candidates.append(row, ignore_index=True)
        else:
            pass

    return df_eligible_candidates




################################################
########## Candlestick Patterns ################
################################################

#https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html

yahoo_data = yf.download("SPY", start="2021-01-01", end="2021-04-06")

#num_engulf = talib.CDLENGULFING(open, high, low, close)
#num_morningstar = talib.CDLMORNINGSTAR(open, high, low, close, penetration=0) 
