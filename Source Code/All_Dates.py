# coding: utf-8
"""
    This file is used to analyze tweets all dates from 10.15 - 11.30
    The result will show charts
"""

import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


#######################################################


# Read csv files into dataframe
df = pd.read_csv('Data/Dataset.csv')
virus_df = pd.read_csv('Data/COVID19.csv')


#######################################################


# Data to plot
labels = 'COVID-19', 'Others'
sizes = [len(virus_df.index), len(df.index)]
colors = ['yellow', 'springgreen']
explode = (0.1, 0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("COVID-19 Propotion 10.15 - 11.30")

plt.axis('equal')
plt.show()


#######################################################


#Following will utilize Model to test all tweets and get setiment analysis. 
import sys
sys.path.insert(1, 'Model')
from Model import *  

pos_tokens = []
neg_tokens = []

for index, row in virus_df.iterrows():
    texttokens = nltk.word_tokenize(row['Tweet'])
    inputfeatureset = SL_features(texttokens, word_features, SL)

    if classifier.classify(inputfeatureset) == 'pos':
        pos_tokens.append((row['Date'], texttokens))
    elif classifier.classify(inputfeatureset) == 'neg':
        neg_tokens.append((row['Date'], texttokens))


#######################################################


# Lists of Pos & Neg
pos = []
neg = []

for i in pos_tokens:
    pos.append(" ".join(i[1]))
    
for i in neg_tokens:
    neg.append(" ".join(i[1]))
    

#######################################################


# Propotional Sector Diagram
import matplotlib.pyplot as plt

# Data to plot
labels = 'Positive', 'Negative'
sizes = [len(pos), len(neg)]
colors = ['orange', 'lightblue']
explode = (0.1, 0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("All Sentiment Propotion 10.15 - 11.30")
plt.axis('equal')
plt.show()


#######################################################


import datetime

# Generate Date Range from 10.15-11.08
dates = []
start_date =  datetime.date(2020, 10, 15)

for i in range(47):
    date_rec = start_date + datetime.timedelta (days=i)
    dates.append(date_rec.strftime('%m/%d/%Y')[:8])


#######################################################


# Numeric Comments on each day
steps = []

for i in dates:
    count = 0
    
    for j in virus_df['Date'].tolist():
        if i in j:
            count += 1
    steps.append(count)


#######################################################


# Daily Sentiment Propotion
pos_daily = []
neg_daily = []

for i in range(len(dates)):
    pos_count = 0
    neg_count = 0
    
    for j in pos_tokens:
        if dates[i] in j[0]:
            pos_count += 1
            
    pos_daily.append(pos_count/steps[i])
    
    for j in neg_tokens:
        if dates[i] in j[0]:
            neg_count += 1
            
    neg_daily.append(neg_count/steps[i])
    

#######################################################


# Line Chart - Numeric 
from datetime import datetime

dates_list = []
for date in dates:
    dates_list.append(datetime.strptime(date+'20', '%m/%d/%Y'))

plt.figure(figsize=(20, 5))
plt.title('All Daily Sentiment Proportion from 10.15 - 11.30')
plt.plot(dates_list, pos_daily, label="Postive", color='blue');
plt.plot(dates_list, neg_daily, label="Negative", color='red');
plt.legend()
plt.show()




















