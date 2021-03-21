#gnews is appending but also continues to repeat the same information
#C:\Users\danni\Documents\GitHub\trading-dashboard
# conda create --name myenv
# pip install -r requirements.txt
#conda create --name new --clone original

import os
import sys


def get_filepath(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    data_dir =  root_dir + '\modules\data'
    file_path = os.path.join(data_dir, f'{filename}.csv')
    return(file_path)


#get_filepath('testname')

root_dir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
mod_dir =  root_dir + '\modules'
data_dir =  root_dir + '\modules\data'

sys.path.insert(0, f'{mod_dir}') #change directory to access the module file

#import modules and autorun
#import gnews
#import portfolio_news

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
