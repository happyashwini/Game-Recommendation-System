
# coding: utf-8

# In[36]:

import pandas as pd
import numpy as np
import os


# In[37]:

games = pd.read_csv('games.csv')
ratings = pd.read_csv('ratings.csv')


# In[38]:

games.head()


# In[40]:

ratings.head()


# In[41]:

def replace_name(x):
    return games[games['gameId']==x].title.values[0]

ratings.gameId = ratings.gameId.map(replace_name)


# In[42]:

ratings.head()


# In[43]:

M = ratings.pivot_table(index=['userId'],columns=['gameId'],values='rating')


# In[44]:

M.shape


# In[45]:

M


# In[46]:

def pearson(s1, s2):
    """this takes object of two pd.series and returns pearson correlation"""
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c*s2_c) / np.sqrt(np.sum(s1_c ** 2) *np.sum(s2_c ** 2))


# In[47]:

'''pearson(M['\'burbs, The (1989)'], M['10 Things I Hate About You (1999)'])


# In[48]:

pearson(M['Mission: Impossible II (2000)'], M['Erin Brockovich (2000)'])


# In[49]:

pearson(M['Clerks (1994)'],M['Mallrats (1995)'] )'''


# In[54]:

def get_recs(game_name, M, num):

    import numpy as np

    reviews = []
    for title in M.columns:
        if title == game_name:
            continue
        cor = pearson(M[game_name], M[title])
        if np.isnan(cor):
            continue
        else:
            reviews.append((title, cor))

    reviews.sort(key=lambda tup: tup[1], reverse=True)
    return reviews[:num]


# In[59]:

recs = get_recs('COUNTER-STRIKE', M, 5)


# In[60]:

print(recs[:5])


# In[61]:

'''anti_recs = get_recs('Clerks (1994)', M, 8551)


# In[62]:

anti_recs[-10:]'''



