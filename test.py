#gnews is appending but also continues to repeat the same information

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
import gnews
import portfolio_news
