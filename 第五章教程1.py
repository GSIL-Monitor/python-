import pandas_datareader.data as web
from pandas import Series,DataFrame
import re

#all_data = {}
#for ticker in ['AAPL','IBM','MSFT','GOOG']:
    #all_data[ticker] = web.DataReader(ticker,data_source='yahoo')
    
#prince = DataFrame({tic:data['Adj Close']
                        #for tic,data in all_data.iteritems()})
                
#volume = DataFrame({tic:data['Volume']
                        #for tic,data in all_data.iteritems()})
                        
#text = "foo bar\t baz \tqux"

#print re.split('\s+',text)

text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
"""

pattern = r'[A-Z0-9+]+@[A-Z0-9+]+\.[A-Z]{2,4}'

regex = re.compile(pattern,flags=re.IGNORECASE)
