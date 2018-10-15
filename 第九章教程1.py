# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#df = pd.DataFrame({'key1':['a','a','b','b','a'],
                #'key2':['one','two','one','two','one'],
                #'data1':np.random.randn(5),
                #'data2':np.random.randn(5)})

#print df

#print df.groupby(['key1','key2']).size()

#people = pd.DataFrame(np.random.randn(5,5),
                        #columns=['a','b','c','d','e'],
                        #index=['Joe','Steve','Wes','Jim','Travis'])

df = pd.read_csv(unicode('E:\SQL教程\python\pydata-book-2nd-edition\examples/tips.csv','utf_8'))
#红桃(Hearts)/黑桃(Spades)/梅花(Clubs)/方片(Diamonds)
#suits = ['H','S','C','D']
#card_val = (range(1,11)+[10]*3)*4
#base_names = ['A']+range(2,11)+['J','K','Q']
#cards = []
#for suit in ['H','S','C','D']:
    #cards.extend(str(num) + suit for num in base_names)

#deck = pd.Series(card_val,index = cards)

#import statsmodels.api as sm

#def regress(data,yvar,xvars):
    #Y = data[yvar]
    #X = data[xvars]
    #X['intercept'] = 1.
    #a = sm.OLS(Y,X).fit()
    #return a.params
    
