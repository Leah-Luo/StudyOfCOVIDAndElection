# coding: utf-8
"""
	This file is used to extract tweets about Covid-19 based on all possible keywords from Dataset
	A new file with all data of covid-19 will be generated
"""


import time
import datetime
import matplotlib.pyplot as plt
import nltk
import pandas as pd

# Read csv file into dataframe
df = pd.read_csv ('Data/Dataset.csv')

# All possible keywords related to covid-19
keywords = ['coronavirus', 'COVID-19', 'Pandemic', 'epidemic', 'outbreak', 'COVID19', 'COVID 19', 'covid19', 'corona virus', 'COVID', 'virus', 'Virus', 'mask', 'ICU', 'vaccine','hospital', 'death', 'lung', 'stay safe', 'failure', 'wfh', 'work from home', 'WHO']

# DataFrame relevent to Virus
count = 0

time_lst = []
tweet_lst = []
state_lst = []

for index, row in df.iterrows():
    if any(data in row['tweet'] for data in keywords):
        
        time_lst.append(row['created_at'])
        tweet_lst.append(row['tweet'])
        state_lst.append(row['state'])
        count +=1
   

# DataFrame Relevent to COVID-19
col_name = ["Date", "Tweet", "State"]
virus_df = pd.DataFrame(columns = col_name)

virus_df["Date"] = time_lst
virus_df["Tweet"] = tweet_lst
virus_df["State"] = state_lst



def saveFile(df):
    csv_file = "Data/Covid19.csv"
    df.to_csv(csv_file, header=True, index=False, encoding = 'utf-8')
 
# Save csv file relevant to Covid-19
saveFile(virus_df)

