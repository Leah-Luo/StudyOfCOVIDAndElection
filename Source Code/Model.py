# coding: utf-8
"""
    This file is used to train the model by nltk.corpus.
    We will use this model to test all tweets as sentiment analysis later
"""

import nltk
from nltk.corpus import sentence_polarity
from nltk.metrics import *
import random

# sentence_polarity Corpus
documents = [(sent, cat) for cat in sentence_polarity.categories() 
	for sent in sentence_polarity.sents(categories=cat)]

# Shuffle Documents
random.shuffle(documents)

# All Words List
all_words_list = [word for (sent,cat) in documents for word in sent]

# Check if words are alphabets 
alpha_words_list = [w for w in all_words_list if w.isalpha()]

# Define stopWords in English
stopwords = nltk.corpus.stopwords.words('english')
stop_words_list = [word for word in alpha_words_list if word not in stopwords]

# Most 2000 Frequency Words
all_words = nltk.FreqDist(stop_words_list)
word_items = all_words.most_common(2000)
word_features = [word for (word,count) in word_items]


SLpath = 'subjclueslen1-HLTEMNLP05.tff'
def readSubjectivity(path):
    flexicon = open(path, 'r')
    # initialize an empty dictionary
    sldict = { }
    for line in flexicon:
        fields = line.split()   # default is to split on whitespace
        # split each field on the '=' and keep the second part as the value
        strength = fields[0].split("=")[1]
        word = fields[2].split("=")[1]
        posTag = fields[3].split("=")[1]
        stemmed = fields[4].split("=")[1]
        polarity = fields[5].split("=")[1]
        if (stemmed == 'y'):
            isStemmed = True
        else:
            isStemmed = False
        # put a dictionary entry with the word as the keyword
        #     and a list of the other values
        sldict[word] = [strength, posTag, isStemmed, polarity]
    return sldict

SL = readSubjectivity(SLpath)

def SL_features(document, word_features, SL):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    # count variables for the 4 classes of subjectivity
    weakPos = 0
    strongPos = 0
    weakNeg = 0
    strongNeg = 0
    
    for word in document_words:
        if word in SL:
            strength, posTag, isStemmed, polarity = SL[word]
            if strength == 'weaksubj' and polarity == 'positive':
                weakPos += 1
            if strength == 'strongsubj' and polarity == 'positive':
                strongPos += 1
            if strength == 'weaksubj' and polarity == 'negative':
                weakNeg += 1
            if strength == 'strongsubj' and polarity == 'negative':
                strongNeg += 1
           
            features['positivecount'] = weakPos + (2 * strongPos)
            features['negativecount'] = weakNeg + (2 * strongNeg)      
    
    return features

SL_featuresets = [(SL_features(d, word_features, SL), c) for (d, c) in documents]

# Define train_data and test_data sets from SL_featuresets
train_data, test_data = SL_featuresets[3000:], SL_featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_data)

print('Accuracy: ', nltk.classify.accuracy(classifier, test_data))
print(classifier.show_most_informative_features(10))

# Cross-Validation
reflist = []
testlist = []
for (features, label) in test_data:
    reflist.append(label)
    testlist.append(classifier.classify(features))

reflist[:30] 
testlist[:30]

ref1 = set([i for i,label in enumerate(reflist) if label == 'pos']) 
ref2 = set([i for i,label in enumerate(reflist) if label == 'neg'])

test1 = set([i for i,label in enumerate(testlist) if label == 'pos']) 
test2 = set([i for i,label in enumerate(testlist) if label == 'neg'])


def printmeasures(label, refset, testset):
    print(label, 'precision:', precision(refset, testset))
    print(label, 'recall:', recall(refset, testset)) 
    print(label, 'F-measure:', f_measure(refset, testset))


print(printmeasures('pos', ref1, test1))
print(printmeasures('neg', ref2, test2))




