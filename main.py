from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import dateutil.parser as parser
import datetime as dt
from bs4 import GuessedAtParserWarning
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)


finvizUrl = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'AAPL', 'TSLA']

newsTables={}
for ticker in tickers:
    url = finvizUrl + ticker

    req =Request(url=url, headers={'user-agent': 'sentiment-app'})
    response = urlopen(req)
    
    html = BeautifulSoup(response,'html')
    newsTable = html.find(id='news-table')
    newsTables[ticker] = newsTable

parsedData= []

for ticker, newsTable in newsTables.items():

    for row in newsTable.findAll('tr'):

        if row.a != None:
            title = row.a.text

            dateData = row.td.text.strip().split(" ")


            if len(dateData) == 1:
                time = dateData[0]
            else:
                date = dateData[0]
                time = dateData[1]

            parsedData.append([ticker,date,time,title])
        
    df = pd.DataFrame(parsedData, columns = ['ticker', 'date', 'time', 'title'])
    vader = SentimentIntensityAnalyzer()
    
    f = lambda title: vader.polarity_scores(title)['compound']
    df['compound'] = df['title'].apply(f)
    df['date'] = pd.to_datetime(df.date).dt.date


    print(df)

    '''plt.figure(figsize=(10,8))

    meanDf = df.groupby(['ticker', 'date']).mean(numeric_only=True)
    meanDf = meanDf.unstack()
    
    meanDf = meanDf.xs('compound', axis="columns").transpose()
    meanDf.plot(kind='bar')
    plt.show()'''
    


