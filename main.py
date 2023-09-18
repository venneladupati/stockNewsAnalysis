from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
#import warnings
#from bs4 import GuessedAtParserWarning
#warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

finvizUrl = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'FB', 'AMD']

newsTables={}
for ticker in tickers:
    url = finvizUrl + ticker

    req =Request(url=url, headers={'user-agent': 'sentiment-app'})
    response = urlopen(req)
    
    html = BeautifulSoup(response,'html')
    newsTable = html.find(id='news-table')
    newsTables[ticker] = newsTable
    break

amznData = newsTables['AMZN']
amznRows = amznData.findAll('tr')

for index, row in enumerate(amznRows):
        if row.a is not None:
            title = row.a.text
            timestamp = row.td.text
            print(timestamp + " " + title)



