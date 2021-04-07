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

IEX_API_KEY = "pk_18bf16c692c4487889b140e806463ed5"


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

    url = "https://thestockmarketwatch.com/markets/pre-market/today.aspx"
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)

    df_temp = pd.read_html(r.text) #fetch table from "thestockmarketwatch.com"
    df_pregainers = df_temp[1]

    df_pregainers["%Chg"] = df_pregainers["%Chg"].str.strip("%") #reformat all percent
    df_pregainers["%Chg"] = pd.to_numeric(df_pregainers["%Chg"])
    df_pregainers["Last"] = df_pregainers["Last"].str.strip("$")
    df_pregainers["Last"] = pd.to_numeric(df_pregainers["Last"])
    df_pregainers["Volume"] = pd.to_numeric(df_pregainers["Volume"])

    df_pregainers.rename(columns={"Last":"Last Price ($)", "%Chg":"Change (%)", "Symb":"Symbol"}, inplace=True) #rename columns

    df_eligible_candidates = pd.DataFrame(columns = ["Change (%)", "Last Price ($)", "Symbol", "Company", "Volume"])

    for index, row in df_pregainers.iterrows():
        if row["Change (%)"] > gain_percent and                row["Last Price ($)"] < max_last and                row["Volume"] > min_volume:
              df_eligible_candidates = df_eligible_candidates.append(row, ignore_index=True)
        else:
            pass

    return df_eligible_candidates




################################################
########## Candlestick Patterns ################
################################################
patterns = {
    'Two Crows': 'CDL2CROWS',
    'Three Black Crows': 'CDL3BLACKCROWS',
    'Three Inside Up/Down': 'CDL3INSIDE',
    'Three-Line Strike': 'CDL3LINESTRIKE',
    'Three Outside Up/Down': 'CDL3OUTSIDE',
    'Three Stars In The South': 'CDL3STARSINSOUTH',
    'Three Advancing White Soldiers': 'CDL3WHITESOLDIERS',
    'Abandoned Baby': 'CDLABANDONEDBABY',
    'Advance Block': 'CDLADVANCEBLOCK',
    'Belt-hold': 'CDLBELTHOLD',
    'Breakaway': 'CDLBREAKAWAY',
    'Closing Marubozu': 'CDLCLOSINGMARUBOZU',
    'Concealing Baby Swallow': 'CDLCONCEALBABYSWALL',
    'Counterattack': 'CDLCOUNTERATTACK',
    'Dark Cloud Cover': 'CDLDARKCLOUDCOVER',
    'Doji': 'CDLDOJI',
    'Doji Star': 'CDLDOJISTAR',
    'Dragonfly Doji': 'CDLDRAGONFLYDOJI',
    'Engulfing Pattern': 'CDLENGULFING',
    'Evening Doji Star': 'CDLEVENINGDOJISTAR',
    'Evening Star': 'CDLEVENINGSTAR',
    'Up/Down-gap side-by-side white lines': 'CDLGAPSIDESIDEWHITE',
    'Gravestone Doji': 'CDLGRAVESTONEDOJI',
    'Hammer': 'CDLHAMMER',
    'Hanging Man': 'CDLHANGINGMAN',
    'Harami Pattern': 'CDLHARAMI',
    'Harami Cross Pattern': 'CDLHARAMICROSS',
    'High-Wave Candle': 'CDLHIGHWAVE',
    'Hikkake Pattern': 'CDLHIKKAKE',
    'Modified Hikkake Pattern': 'CDLHIKKAKEMOD',
    'Homing Pigeon': 'CDLHOMINGPIGEON',
    'Identical Three Crows': 'CDLIDENTICAL3CROWS',
    'In-Neck Pattern': 'CDLINNECK',
    'Inverted Hammer': 'CDLINVERTEDHAMMER',
    'Kicking': 'CDLKICKING',
    'Kicking - bull/bear determined by the longer marubozu': 'CDLKICKINGBYLENGTH',
    'Ladder Bottom': 'CDLLADDERBOTTOM',
    'Long Legged Doji': 'CDLLONGLEGGEDDOJI',
    'Long Line Candle': 'CDLLONGLINE',
    'Marubozu': 'CDLMARUBOZU',
    'Matching Low': 'CDLMATCHINGLOW',
    'Mat Hold': 'CDLMATHOLD',
    'Morning Doji Star': 'CDLMORNINGDOJISTAR',
    'Morning Star': 'CDLMORNINGSTAR',
    'On-Neck Pattern': 'CDLONNECK',
    'Piercing Pattern': 'CDLPIERCING',
    'Rickshaw Man': 'CDLRICKSHAWMAN',
    'Rising/Falling Three Methods': 'CDLRISEFALL3METHODS',
    'Separating Lines': 'CDLSEPARATINGLINES',
    'Shooting Star': 'CDLSHOOTINGSTAR',
    'Short Line Candle': 'CDLSHORTLINE',
    'Spinning Top': 'CDLSPINNINGTOP',
    'Stalled Pattern': 'CDLSTALLEDPATTERN',
    'Stick Sandwich': 'CDLSTICKSANDWICH',
    'Takuri (Dragonfly Doji with very long lower shadow)': 'CDLTAKURI',
    'Tasuki Gap': 'CDLTASUKIGAP',
    'Thrusting Pattern': 'CDLTHRUSTING',
    'Tristar Pattern': 'CDLTRISTAR',
    'Unique 3 River': 'CDLUNIQUE3RIVER',
    'Upside Gap Two Crows': 'CDLUPSIDEGAP2CROWS',
    'Upside/Downside Gap Three Methods': 'CDLXSIDEGAP3METHODS'
}

patterns_swap = {
    "CDL2CROWS":"Two Crows",
    "CDL3BLACKCROWS":"Three Black Crows",
    "CDL3INSIDE":"Three Inside Up/Down",
    "CDL3LINESTRIKE":"Three-Line Strike",
    "CDL3OUTSIDE":"Three Outside Up/Down",
    "CDL3STARSINSOUTH":"Three Stars In The South",
    "CDL3WHITESOLDIERS":"Three Advancing White Soldiers",
    "CDLABANDONEDBABY":"Abandoned Baby",
    "CDLADVANCEBLOCK":"Advance Block",
    "CDLBELTHOLD":"Belt-hold",
    "CDLBREAKAWAY":"Breakaway",
    "CDLCLOSINGMARUBOZU":"Closing Marubozu",
    "CDLCONCEALBABYSWALL":"Concealing Baby Swallow",
    "CDLCOUNTERATTACK":"Counterattack",
    "CDLDARKCLOUDCOVER":"Dark Cloud Cover",
    "CDLDOJI":"Doji",
    "CDLDOJISTAR":"Doji Star",
    "CDLDRAGONFLYDOJI":"Dragonfly Doji",
    "CDLENGULFING":"Engulfing Pattern",
    "CDLEVENINGDOJISTAR":"Evening Doji Star",
    "CDLEVENINGSTAR":"Evening Star",
    "CDLGAPSIDESIDEWHITE":"Up/Down-gap side-by-side white lines",
    "CDLGRAVESTONEDOJI":"Gravestone Doji",
    "CDLHAMMER":"Hammer",
    "CDLHANGINGMAN":"Hanging Man",
    "CDLHARAMI":"Harami Pattern",
    "CDLHARAMICROSS":"Harami Cross Pattern",
    "CDLHIGHWAVE":"High-Wave Candle",
    "CDLHIKKAKE":"Hikkake Pattern",
    "CDLHIKKAKEMOD":"Modified Hikkake Pattern",
    "CDLHOMINGPIGEON":"Homing Pigeon",
    "CDLIDENTICAL3CROWS":"Identical Three Crows",
    "CDLINNECK":"In-Neck Pattern",
    "CDLINVERTEDHAMMER":"Inverted Hammer",
    "CDLKICKING":"Kicking",
    "CDLKICKINGBYLENGTH":"Kicking - bull/bear determined by the longer marubozu",
    "CDLLADDERBOTTOM":"Ladder Bottom",
    "CDLLONGLEGGEDDOJI":"Long Legged Doji",
    "CDLLONGLINE":"Long Line Candle",
    "CDLMARUBOZU":"Marubozu",
    "CDLMATCHINGLOW":"Matching Low",
    "CDLMATHOLD":"Mat Hold",
    "CDLMORNINGDOJISTAR":"Morning Doji Star",
    "CDLMORNINGSTAR":"Morning Star",
    "CDLONNECK":"On-Neck Pattern",
    "CDLPIERCING":"Piercing Pattern",
    "CDLRICKSHAWMAN":"Rickshaw Man",
    "CDLRISEFALL3METHODS":"Rising/Falling Three Methods",
    "CDLSEPARATINGLINES":"Separating Lines",
    "CDLSHOOTINGSTAR":"Shooting Star",
    "CDLSHORTLINE":"Short Line Candle",
    "CDLSPINNINGTOP":"Spinning Top",
    "CDLSTALLEDPATTERN":"Stalled Pattern",
    "CDLSTICKSANDWICH":"Stick Sandwich",
    "CDLTAKURI":"Takuri (Dragonfly Doji with very long lower shadow)",
    "CDLTASUKIGAP":"Tasuki Gap",
    "CDLTHRUSTING":"Thrusting Pattern",
    "CDLTRISTAR":"Tristar Pattern",
    "CDLUNIQUE3RIVER":"Unique 3 River",
    "CDLUPSIDEGAP2CROWS":"Upside Gap Two Crows",
    "CDLXSIDEGAP3METHODS":"Upside/Downside Gap Three Methods",
}



#https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html
#rising three, doji and three white soldiers

#def get_symbols_data(symbols):
