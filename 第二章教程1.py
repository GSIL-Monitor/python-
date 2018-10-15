# -*- coding: utf-8 -*-
f = open(unicode('E:/SQL教程/python/pydata-book-2nd-edition/datasets/bitly_usagov/example.txt','utf-8'),'r')


#print i


import json
records = [json.loads(line) for line in f]

f.close()

from pandas import DataFrame,Series
import pandas as pd; import numpy as np
from matplotlib import pyplot 


frame = DataFrame(records)

results = Series([x.split()[0] for x in frame.a.dropna()])

#print results.value_counts()[:8]

cframe = frame[frame.a.notnull()]

#print cframe

operating_system = np.where(cframe['a'].str.contains('Windows'),'Windows','Not Windows')

#print operating_system

by_tz_os = cframe.groupby(['tz',operating_system])

agg_counts = by_tz_os.size().unstack().fillna(0)

#print agg_counts

indexer = agg_counts.sum(1).argsort()

#print indexer[:10]

count_subset = agg_counts.take(indexer)[-10:]

#print count_subset.plot(kind='barh',stacked=True).show()

normed_subset = count_subset.div(count_subset.sum(1),axis=0)

print normed_subset.plot(kind='barh',stacked=True)
show()