#gnews is appending but also continues to repeat the same information

import os
import sys

def get_filepath(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    data_dir =  root_dir + '\modules\data'
    file_path = os.path.join(data_dir, f'{filename}.csv')
    return(file_path)


#get_filepath('testname')

mod_dir =  os.path.dirname(os.path.abspath(__file__)) + '\modules'
sys.path.insert(0, f'{mod_dir}')


#import modules and autorun
import gnews
import portfolio_news
