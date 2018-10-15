# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

years = range(1880,2011)
pieces = []
columns = ['name','sex','birth']

for year in years:
    path = unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets/babynames/yob%d.txt','utf-8')%year
    frame = pd.read_csv(path,names=columns)
    
    frame['year'] = year
    pieces.append(frame)


names = pd.concat(pieces,ignore_index=True)

#从name列取出最后一个字母
#get_last_letter = lambda x:x[-1]
#last_letters = names['name'].map(get_last_letter)
#print last_letters
#names['name'] = last_letters

#names.rename(columns={'name':'last_letter'},inplace=True)

#print names

#table = names.pivot_table('birth',index='last_letter',columns=['sex','year'],aggfunc=sum)

#subtable = table.reindex(columns=[1910,1960,2010],level='year')

#letter_prop = subtable / subtable.sum().astype(float)

#print letter_prop

#fig,axes = plt.subplots(2,1,figsize=(10,8))
#letter_prop['M'].plot(kind='bar',rot=0,ax=axes[0],title='Male')
#letter_prop['F'].plot(kind='bar',rot=0,ax=axes[1],title='Female',legend=False)
#plt.show()

#letter_prop = table / table.sum().astype(float)
#print letter_prop

#dny_ts = letter_prop.ix[['d','n','y'],'M'].T
#print dny_ts

#dny_ts.plot()

def get_top1000(group):
    return group.sort_index(by='birth',ascending=False)[:1000]

top1000 = names.groupby(['year','sex']).apply(get_top1000)

#print top1000

all_names = top1000.name.unique()

#print all_names

lesley_like = all_names[['lesl' in x.lower() for x in all_names]]
#print lesley_like

filtered = top1000[top1000['name'].isin(lesley_like)]

x = filtered.groupby(by='name')['birth'].sum()

#print x

table = filtered.pivot_table('birth',index='year',columns='sex',aggfunc=sum)

table = table.div(table.sum(1),axis=0)

table.plot(style={'M':'k-','F':'k--'})