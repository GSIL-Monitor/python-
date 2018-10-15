# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#fig = plt.figure()
#ax1 = fig.add_subplot(2,2,1)
#ax2 = fig.add_subplot(2,2,2)
#ax3 = fig.add_subplot(2,2,3)

fig , axes = plt.subplots(2,3,sharex=True,sharey=True)
for i in range(2):
    for j in range(3):
        axes[i,j].hist(np.random.randn(500),bins=50,color='lightseagreen',alpha=0.5)
plt.subplots_adjust(wspace=0,hspace=0)

data = np.random.randn(30).cumsum()
plt.plot(data,color='lightseagreen',linestyle='dashdot',marker='o')

fig = plt.figure();ax = fig.add_subplot(1,1,1)
ax.plot(np.random.randn(1000).cumsum())
ticks = ax.set_xticks([0,250,500,750,1000])

from datetime import datetime
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

data = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples\spx.csv','utf-8'),parse_dates=True,index_col=0)
spx = data['SPX']

spx.plot(ax=ax,color='orange',linestyle='dotted',marker='o')

crisis_data = [
    (datetime(2007,10,11),'Peak of bull market'),
    (datetime(2008,3,12),'Bear Stearns Fails'),
    (datetime(2008,9,15),'Lehman Bankruptcy')]
    
for date, label in crisis_data:
    ax.annotate(label,xy=(date,spx.asof(date)+50),
                xytext=(date,spx.asof(date)+200),
                arrowprops=dict(facecolor='black'),
                horizontalalignment='left',verticalalignment='top')

ax.set_xlim(['1/1/2007','1/1/2011'])
ax.set_ylim([600,1800])

ax.set_title('Important dates in 2008-2009 financial crisis')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

rect = plt.Rectangle((0.2,0.75),0.4,0.15,color='blue',alpha=0.3)
circ = plt.Circle((0.7,0.2),0.15,color='darkgreen',alpha=0.3)
pgon = plt.Polygon([[0.15,0.15],[0.35,0.4],[0.2,0.6]],color='navajowhite',alpha=0.5)

ax.add_patch(rect)
ax.add_patch(circ)
ax.add_patch(pgon)

df = pd.DataFrame(np.random.randn(10,4).cumsum(0),
                  columns=['A','B','C','D'],
                  index=np.arange(0,100,10))
                  
fig,axes = plt.subplots(2,1)
data = pd.Series(np.random.randn(16),index=list('abcdefghijklmnop'))
data.plot(kind='bar',ax=axes[0],color='orangered',alpha=0.7)
data.plot(kind='barh',ax=axes[1],color='lawngreen',alpha=0.7)

df = pd.DataFrame(np.random.rand(6,4),
                  index=['one','two','three','four','five','six'],
                  columns=['A','B','C','D'])
df.columns = df.columns.rename('Genus')
df.plot(kind='bar')

tips = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/tips.csv','utf_8'))
party_counts = pd.crosstab(tips['day'],tips['size'])
party_counts = party_counts.loc[:,2:5]

tips['tip_pct'] = tips.tip / tips.total_bill
tips.tip_pct.hist(bins=50)
tips.tip_pct.plot(kind='KDE',color='orangered')

data = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets\haiti\Haiti.csv','utf-8'))
data = data[(data.LATITUDE > 18)&(data.LATITUDE < 20)&(data.LONGITUDE > -75)&(data.LONGITUDE < -70)&data.CATEGORY.notnull()]
