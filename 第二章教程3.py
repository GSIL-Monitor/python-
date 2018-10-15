# -*- coding: utf-8 -*-
f = open(unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets/babynames/yob1880.txt','utf-8'),'r')
x = f.readlines()
f.close()

#print x[:10]

import pandas as pd

import numpy as np 

import matplotlib.pyplot as plt

names1880 = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets/babynames/yob1880.txt','utf-8'),names=[
'name','sex','birth'])

#print names1880

#print names1880.groupby('sex').sum()

years = range(1880,2011)
pieces = []
columns = ['name','sex','birth']

for year in years:
    path = unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets/babynames/yob%d.txt','utf-8')%year
    frame = pd.read_csv(path,names=columns)
    
    frame['year'] = year
    pieces.append(frame)


names = pd.concat(pieces,ignore_index=True)

#print names

total_births = names.pivot_table('birth',index='year',columns='sex',aggfunc=sum)

#print total_births

def add_prop(group):
    birth = group['birth'].astype(float)
    
    group['prop'] = birth / birth.sum()
    return group


x = names.groupby(['year','sex']).apply(add_prop)

#print x

def get_top1000(group):
    return group.sort_index(by='birth',ascending=False)[:1000]
grouped = x.groupby(['year','sex'])
top1000 = grouped.apply(get_top1000)

#print top1000

boys = top1000[top1000['sex']=='M']
girls = top1000[top1000['sex']=='F']

df = boys[boys['year']==2010]

prop_cumsum = df.sort_index(by='prop',ascending=False).prop.cumsum()

prop_sear = prop_cumsum.searchsorted(0.5)

print prop_sear[0]

#total_births = top1000.pivot_table('birth',index='year',columns='name',aggfunc=sum)

#subset = total_births[['John','Harry','Mary','Marilyn']]

#print subset

#subset.plot(subplots=True,figsize=(12,10),grid=False,title='Number of births per year')

#table = top1000.pivot_table('prop',index='year',columns='sex',aggfunc=sum)

#table.plot(title='Sum of table1000.prop by year and sex',yticks=np.linspace(0,1.2,13),xticks=range(1880,2020,10))

#plt.show()


def get_quantile_count(group,q=0.5):
    group = group.sort_index(by='prop',ascending=False)
    return group.prop.cumsum().searchsorted(q)[0] + 1
    
diversity  = top1000.groupby(['year','sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

print diversity



diversity.plot(title='Number of popular names in top 50%')
plt.show()
