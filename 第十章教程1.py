from datetime import datetime
import numpy as np
import pandas as pd
now = datetime.now()
#print now
#print now.year, now.month, now.day
delta = datetime(2011,1,7) - datetime(2008,6,24,8,15)
#print delta, delta.days, delta.seconds

from datetime import timedelta
start = datetime(2011,1,7)
#print start + timedelta(12)
#print start - 2 * timedelta(12)

stamp = datetime(2011,1,3)
str(stamp), stamp.strftime('%Y-%m-%d')
value = '2011-01-03'
datetime.strptime(value,'%Y-%m-%d')
datestrs = [r'7/8/2013','8/6/2011']
[datetime.strptime(x,'%m/%d/%Y') for x in datestrs]

from dateutil.parser import parse
parse('2011-01-03')
parse('28/6/2018',dayfirst=True)

dates =[datetime(2011,1,2),datetime(2011,1,5),datetime(2011,1,7),datetime(2011,1,8),datetime(2011,1,10),datetime(2011,1,12)]
ts = pd.Series(np.random.randn(6),index=dates)

longer_ts = pd.Series(np.random.randn(1000),index=pd.date_range('1/1/2000',periods=1000))

from pandas.tseries.offsets import Hour,Minute,Day,MonthEnd
ts = pd.Series(np.random.randn(4),index=pd.date_range('1/1/2000',periods=4,freq='M'))
now = datetime.now()
ts = pd.Series(np.random.randn(20),index=pd.date_range(datetime.strftime(now,'%Y-%m-%d'),periods=20,freq='4D'))

import pytz
rng = pd.period_range('2000-1-1','2018-6-28',freq='A-DEC')
ts = pd.Series(np.random.randn(len(rng)),index=rng)

rng = pd.date_range('1/1/2018',periods=3,freq='M')
ts=pd.Series(np.random.randn(3),index=rng)

data = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples\macrodata.csv','utf-8'))
index = pd.PeriodIndex(year=data.year,quarter=data.quarter,freq='Q-DEC')

frame = pd.DataFrame(np.random.randn(2,4),
                    index=pd.date_range('1/1/2000',periods=2,freq='W-WED'),
                    columns=['Colorado','Texas','New York','Ohio'])

close_px_all = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples\stock_px.csv','utf-8'),parse_dates=True,index_col=0)