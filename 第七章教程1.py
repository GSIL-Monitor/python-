# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
import json

#df1 = pd.DataFrame({'key1':['Ohio','Ohio','Ohio','Nevada','Nevada'],
#'key2':[2000,2001,2002,2001,2002],
#'data':np.arange(5)})

#df2 = pd.DataFrame(np.arange(12).reshape(6,2),
#index=[['Nevada','Nevada','Ohio','Ohio','Ohio','Ohio'],[2001,2000,2000,2000,2001,2002]],
#columns=['event1','event2'])

#s1 = pd.Series([0,1],index=['a','b'])
#s2 = pd.Series([2,3,4],index=['c','d','e'])
#s3 = pd.Series([5,6],index=['f','g'])

#s4 = pd.concat([s1*5,s3],axis=1)

#data = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/macrodata.csv','utf-8'))
#periods = pd.PeriodIndex(year=data.year,quarter=data.quarter,name='data')
#columns = pd.Index(['realgdp','infl','unemp'],name='item')
#data = data.reindex(columns=columns)
#data.index = periods.to_timestamp('D','end')
#ldata = data.stack().reset_index().rename(columns={0:'value'})

#pivoted = ldata.pivot(index='data',columns='item',values='value')

#print pivoted

#data = np.random.rand(20)

#print pd.cut(data,4,precision=4,right=False)

#db = json.load(open(unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets\usda_food/database.json','utf-8')))

nutrients = []

for rec in db:
    fnuts = pd.DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)
    
nutrients = pd.concat(nutrients,ignore_index=True)
