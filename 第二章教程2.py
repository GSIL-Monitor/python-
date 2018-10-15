# -*- coding: utf-8 -*-
import pandas as pd

unames = ['user_id','gender','age','occupation','zip']

users = pd.read_table(unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets\movielens/users.dat','utf-8'),sep='::',header=None,names=unames)

rnames = ['user_id','movie_id','rating','timestamp']

ratings = pd.read_table(unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets\movielens/ratings.dat','utf-8'),sep='::',header=None,names=rnames)

mnames = ['movie_id','title','genres']

movies = pd.read_table(unicode('E:\SQL教程\python\pydata-book-2nd-edition\datasets\movielens/movies.dat','utf-8'),sep='::',header=None,names=mnames)

data = pd.merge(pd.merge(ratings,users),movies)

mean_ratings = data.pivot_table('rating',index='title',columns='gender',aggfunc='mean')

#print mean_ratings[:5]

ratings_by_title = data.groupby('title').size()

#print ratings_by_title[:10]

active_titles = ratings_by_title.index[ratings_by_title >= 250]

#print active_titles

mean_ratings = mean_ratings.ix[active_titles]

#print mean_ratings

top_female_ratings = mean_ratings.sort_index(by='F',ascending=False)

#print top_female_ratings[:10]

mean_ratings['diff'] = mean_ratings['F'] - mean_ratings['M']

sorted_by_diff = mean_ratings.sort_index(by='diff')

#print sorted_by_diff[:15]

rating_std_by_title = data.groupby('title')['rating'].std()

#print rating_std_by_title.sort_index(ascending=False)[:10]

