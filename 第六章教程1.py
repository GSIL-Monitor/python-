# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#df = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex1.csv','utf-8'))

#print df

#print  pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex2.csv','utf-8'),header=None)

#print  pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex2.csv','utf-8'),
#names=['a','b','c','d','message'],index_col='message')

#parsed = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/csv_mindex.csv','utf-8'),
#index_col=['key1','key2'])

#print parsed

#result = pd.read_table(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex3.csv','utf-8'),sep='\s+')

#print result

#result = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex5.csv','utf-8'),na_values=['NULL'])

#print result.fillna(0)

#result = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex6.csv','utf-8'),chunksize=1000)

#tot = pd.Series([])

#for piece in result:
    #tot = tot.add(piece['key'].value_counts(),fill_value=0)

#print tot.sort_values(ascending=False)[:10]

#data = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex5.csv','utf-8'))

#data.to_csv(unicode('E:\SQL教程\python教程/selfrealop.csv','utf-8'),na_rep='Null',index=False,columns=['a','b','c'])

#print pd.read_csv(unicode('E:\SQL教程\python教程/selfrealop.csv','utf-8'))


#import csv

#f = open(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/ex7.csv','utf-8'),'r')
#reader = csv.reader(f)

#lines = list(reader)

#header,values = lines[0],lines[1:]

#data_dict = {h: v for h, v in zip(header, zip(*values))}

#print data_dict

from lxml.html import parse
from urllib2 import urlopen

parsed = parse(urlopen('http://finance.yahoo.com/q/op?s=AAPL+Options'))

#print parsed

doc = parsed.getroot()
links = doc.findall('.//a')
link = links[28]

print link.get('href')