
"""Import libraries and set root links"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
from datetime import datetime

root = 'https://www.google.com/' #root query
link = 'https://www.google.com/search?q=stock+market&tbs=qdr:d,sbd:1&tbm=nws&sxsrf=ALeKk01Z7V8cfTmouyE_tD0qJd7e4vkpqQ:1615807067965&source=lnt&sa=X&ved=0ahUKEwiUzb6ylrLvAhWXQhUIHQseBL0QpwUIKA&biw=1536&bih=722&dpr=1.25'

"""Write recursive scrape page function"""

def news(link):
  req = Request(link, headers={'User-Agent': 'Edg/79.0.309.43'}) #set request link and browser info
  webpage = urlopen(req).read() #read webpage

  with requests.Session() as c: #while request is open
    soup = BeautifulSoup(webpage, 'html5lib') #use bs4 to read html
    #print(soup)

    for item in soup.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
      #find all items in webpage with html tag 'div' and class 'ZINbbc xpd O9g5cc uUPGi' as if you look at the BS4 html with print(soup)
      # that is the class that contains title, description and link. Use parent classes as more general

      #find links-------------------
      raw_link = (item.find('a', href=True)['href']) #find raw links by variable "a" and href = true and pull by column href
      first_split = raw_link.split('/url?q=')[1] #split out query string and only get the end item in list
      second_split = first_split.split('&sa=U')[0] #split out the junk in string tail and get first item in list
      link = second_split

      #find title-------------------
      #print(item)
      title = (item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).get_text()) #get title and convert to text so don't print the html
      title = title.replace(',', '') #commas will cause errors with csv

      description = (item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text())
      description = description.replace(',', '') #commas will cause errors with csv

      article_time = description.split('�')[0]
      bio = description.split('�')[1]
      date = datetime.now()

      #print('Title:', title)
      #print('Time:', time)
      #print('Dscription:', bio)
      #print(link)
      #print('-------------')

      #begin writing to CSV file
      #document = open('data.csv', 'a') #a = read and write
      document = open('gnews_data.csv', 'a') #a = read and write
      document.write('{}, {}, {}, {}, {} \n'.format(title, date, article_time, bio, link))
      document.close()

    #go to next page of results
    next = soup.find('a', attrs={'aria-label': 'Next page'}) #find the next page attribute
    next = (next['href']) #get the next page href for navigation

    link = root + next

    try: news(link) #run recursively
    except: print('Module run successfully') #until last webpage and then print warning


def main():
    news(link) #run function


"""Run function"""

if __name__ =='__main__':
  main() #calling the main method
