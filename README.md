# Financial Dashboard

**Features**
- Automatic web scraping for news
- AI driven sentiment analysis (key companies discussed, bull/bear sentiment)

**Sources**
- (News Outlets): Google News, Finimize, StockTwits 
- (Social Media) Reddit: WallStreetBets, Twitter 

**ToDo**
- database file management: https://www.youtube.com/watch?v=xBbK2kvHXwE
- WSB integration
- trading bot

**File Structure**
- **Modules**: Contains back-end processing and data outputs
- **Procfile**: shell command to run app and setup file
- **ReaadMe**: Folder instructions
- **app.py**: streamlit python file to run
- **requirements.txt**: pip install requirements
- **setup.sh**: heroku config file

**Running App**
- portfolio_news.py: Line 19 download NLTK disabled for testing but will need to be enabled for implementation
- environment streamlit_only working but it is just requirements.txt
