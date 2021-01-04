# coding: utf-8
"""
    This file is used to analyze tweets before the date of the election
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


election_date = '11/08/20'
# Retrieve data between 10/15/2020 and 11/08/2020
df = df.loc[df['created_at'] <= election_date]
virus_df = virus_df[virus_df['Date'] <= election_date]


#######################################################


# Data to plot
labels = 'COVID-19', 'Others'
sizes = [len(virus_df.index), len(df.index)]
colors = ['yellow', 'springgreen']
explode = (0.1, 0)  # explode 1st slice


#######################################################


# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("COVID-19 Propotion 10.15 - 11.08")
plt.axis('equal')
plt.show()


#######################################################


# Generate Date Range from 10.15-11.08
import datetime

dates = []
start_date =  datetime.date(2020, 10, 15)

for i in range(25):
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


# Line Chart - Numeric 
from datetime import datetime

dates_list = []
for date in dates:
    dates_list.append(datetime.strptime(date+'20', '%m/%d/%Y'))

plt.figure(figsize=(15, 5))
plt.title('Number of Tweets related to COVID-19')
plt.plot(dates_list, steps);
plt.show()


#######################################################


# Draw Word Cloud based on lists
def word_cloud(lists):
    comment_words = '' 
    stopwords = set(STOPWORDS) 

    # iterate through the csv file 
    for val in lists: 
        # typecaste each val to string 
        val = str(val) 
        # split the value 
        tokens = val.split() 

        # Converts each token into lowercase 
        for i in range(len(tokens)): 
            tokens[i] = tokens[i].lower() 

            tokens[i] = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                           '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', tokens[i])
            tokens[i] = re.sub("(@[A-Za-z0-9_]+)","", tokens[i])

        comment_words += " ".join(tokens)+" "

    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(comment_words) 

    # plot the WordCloud image                        
    plt.figure(figsize = (6, 6), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show()


#######################################################


word_cloud(virus_df['Tweet'])


#######################################################


#Following will utilize Model to test all tweets and get setiment analysis. 
import sys
sys.path.insert(1, 'Model')
from Model import *  

# Extract Positive tokens and Negative tokens
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
    
# Word Cloud for Positive
word_cloud(pos)
# Word Cloud for Negative
word_cloud(neg)


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
plt.title("Sentiment Propotion 10.15 - 11.08")
plt.axis('equal')
plt.show()


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
plt.title('Daily Sentiment Proportion')
plt.plot(dates_list, pos_daily, label="Postive", color='blue');
plt.plot(dates_list, neg_daily, label="Negative", color='red');
plt.legend()
plt.show()


#######################################################


# Line Chart - Variation Trend    ---- Positive
from datetime import datetime

pos_trend_lst = []
for i in range(1, len(pos_daily)):
    gnumbers = ((pos_daily[i] - pos_daily[i-1]) * 100.0 / pos_daily[i-1])
    pos_trend_lst.append(gnumbers)

dates_list = []
for date in range(1, len(dates)):
    dates_list.append(datetime.strptime(dates[date]+'20', '%m/%d/%Y'))

plt.figure(figsize=(15, 5))
plt.title('Growth Rate of Positive attitue on Covid-19')
plt.plot(dates_list, pos_trend_lst, color='blue');
plt.show()


#######################################################


# Line Chart - Variation Trend    ---- Negative
from datetime import datetime

neg_trend_lst = []
for i in range(1, len(neg_daily)):
    gnumbers = ((neg_daily[i] - neg_daily[i-1]) * 100.0 / neg_daily[i-1])
    neg_trend_lst.append(gnumbers)

dates_list = []
for date in range(1, len(dates)):
    dates_list.append(datetime.strptime(dates[date]+'20', '%m/%d/%Y'))

plt.figure(figsize=(15, 5))
plt.title('Growth Rate of Negative attitue on Covid-19')
plt.plot(dates_list, neg_trend_lst, color='red');
plt.show()



