#gnews is appending but also continues to repeat the same information
#C:\Users\danni\Documents\GitHub\trading-dashboard
# conda create --name myenv
# pip install -r requirements.txt
#conda create --name new --clone original

'''https://stackoverflow.com/questions/66588446/python-web-scraping-how-do-i-avoid-scraping-duplicates-for-my-database

https://stackoverflow.com/questions/62306020/prevent-duplicate-rows-in-mysql-database

https://stackoverflow.com/questions/41860250/scraping-dynamic-data-and-avoiding-duplicates-with-bs4-selenium-in-python

https://stackoverflow.com/questions/61079969/when-storing-scrapy-results-to-database-how-to-avoid-storing-duplicates
'''


import requests
from bs4 import BeautifulSoup

url = "https://uk.finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch"
r = requests.get(url)

web_content = BeautifulSoup(r.text, "lxlm")
web_content = web_content.find("div", class_ = "")
